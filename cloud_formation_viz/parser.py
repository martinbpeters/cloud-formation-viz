#!/usr/bin/env python

import sys
import json
import yaml
import datetime
from numbers import Number
from .utils import flatten, pseudo_parameters


class CfnParserError(Exception):
    pass


class cfn_parser(object):

    def __init__(self, parameters_bool, outputs_bool, pseudo_bool, globals_bool):
        self.parameters_bool = parameters_bool
        self.outputs_bool = outputs_bool
        self.pseudo_bool = pseudo_bool
        self.globals_bool = globals_bool
        self.sam_globals = None

    def read_input(self, input_file):
        try:
            template_text = input_file.read()
        except ValueError:
            raise CfnParserError

        input_type = 'undefined'
        if any(extension in input_file.name for extension in ['.yml', '.yaml']):
            input_type = 'yaml'
        elif any(extension in input_file.name for extension in ['.json']):
            input_type = 'json'

        template = None
        if input_type == 'yaml':
            template = self.read_yaml(template_text)
        elif input_type == 'json':
            template = json.loads(template_text)
        else:
            try:
                template = json.loads(template_text)
            except ValueError:
                try:
                    template = self.read_yaml(template_text)
                except:
                    raise CfnParserError

        if self.globals_bool and 'Globals' in template:
            self.sam_globals = template['Globals']

        graph, edges = self.extract_graph(
            template.get('Description', ''),
            template['Resources'])

        graph['edges'].extend(edges)

        if self.parameters_bool:
            self.handle_terminals(template, graph, 'Parameters', 'source')

        if self.outputs_bool:
            self.handle_terminals(template, graph, 'Outputs', 'sink')

        if self.pseudo_bool:
            graph['subgraphs'].append(self.handle_pseudo_params(graph['edges']))

        return graph

    def read_yaml(self, template_text):
        cfn_intrinsic_functions = ['!GetAtt', '!Ref', '!Sub']
        for f in cfn_intrinsic_functions:
            template_text = template_text.replace(f, ' ')
        template = yaml.load(template_text, Loader=yaml.FullLoader)
        return template

    def handle_terminals(self, template, graph, name, rank):
        if name in template:
            subgraph, edges = self.extract_graph(name, template[name])
            subgraph['rank'] = rank
            subgraph['style'] = 'filled,rounded'
            graph['subgraphs'].append(subgraph)
            graph['edges'].extend(edges)

    def handle_pseudo_params(self, edges):
        """
        Pseudo parameters include:
            AWS::AccountId
            AWS::NotificationARNs
            AWS::NoValue
            AWS::Partition
            AWS::Region
            AWS::StackId
            AWS::StackName
            AWS::URLSuffix

        More details can be found here:
            https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html

        :param edges:
        :return:
        """
        graph = {
            'name': 'Pseudo Parameters', 
            'nodes': [], 
            'edges': [], 
            'subgraphs': [],
            'shape': 'ellipse'
        }

        params = set()
        for e in edges:
            if e['from'].startswith(u'AWS::'):
                params.add(e['from'])
        graph['nodes'].extend({'name': n} for n in params)
        return graph

    def extract_graph(self, name, elem):
        graph = {'name': name, 'nodes': [], 'edges': [], 'subgraphs': []}
        edges = []
        for item, details in elem.items():
            # Outputs don't have a type so setting it as default
            node_type = 'Output'
            if 'Type' in details:
                node_type = details['Type']

            graph['nodes'].append({'name': item, 'type': node_type})

            if self.sam_globals:
                if node_type in ['AWS::Serverless::Function', 'AWS::Serverless::Api', 'AWS::Serverless::SimpleTable']:
                    details['Properties'] = {**details['Properties'], **self.sam_globals['Function']}

            edges.extend(flatten(self.find_refs(item, details)))
        return graph, edges

    def find_refs(self, context, elem):
        if isinstance(elem, dict):
            refs = []
            for k, v in elem.items():
                if not self.pseudo_bool and v in pseudo_parameters:
                    continue
                if k == 'Ref':
                    assert isinstance(v, str), 'Expected a string: %s' % v
                    refs.append({'from': v, 'to': context})
                elif k == 'Fn::GetAtt':
                    assert isinstance(v, list), 'Expected a list: %s' % v
                    refs.append({'from': v[0], 'to': context})
                else:
                    refs.extend(self.find_refs(context, v))
            return refs
        elif isinstance(elem, list):
            return map(lambda e: self.find_refs(context, e), elem)
        elif isinstance(elem, str):
            return []
        elif isinstance(elem, bool):
            return []
        elif isinstance(elem, Number):
            return []
        elif isinstance(elem, datetime.date):
            return []
        else:
            raise AssertionError('Unexpected type: %s' % elem)

    def node_type(self, graph, node_name):
        for n in graph['nodes']:
            if n['name'] == node_name:
                return n['type']
