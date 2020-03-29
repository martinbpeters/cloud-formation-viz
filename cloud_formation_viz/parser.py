#!/usr/bin/env python

import sys
import json
import yaml
import datetime
from numbers import Number
from .utils import flatten


class CfnParserError(Exception):
    pass


def read_input(input_file):
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
        template = read_yaml(template_text)
    elif input_type == 'json':
        template = json.loads(template_text)
    else:
        try:
            template = json.loads(template_text)
        except ValueError:
            try:
                template = read_yaml(template_text)
            except:
                raise CfnParserError

    (graph, edges) = extract_graph(
        template.get('Description', ''), 
        template['Resources'])

    graph['edges'].extend(edges)

    handle_terminals(template, graph, 'Parameters', 'source')

    handle_terminals(template, graph, 'Outputs', 'sink')

    graph['subgraphs'].append(handle_psuedo_params(graph['edges']))

    return graph


def read_yaml(template_text):
    cfn_intrinsic_functions = ['!GetAtt', '!Ref', '!Sub']
    for f in cfn_intrinsic_functions:
        template_text = template_text.replace(f, ' ')
    template = yaml.load(template_text, Loader=yaml.FullLoader)
    return template


def handle_terminals(template, graph, name, rank):
    if name in template:
        (subgraph, edges) = extract_graph(name, template[name])
        subgraph['rank'] = rank
        subgraph['style'] = 'filled,rounded'
        graph['subgraphs'].append(subgraph)
        graph['edges'].extend(edges)


def handle_psuedo_params(edges):
    graph = {'name': 'Psuedo Parameters', 'nodes': [], 'edges': [], 'subgraphs': []}
    graph['shape'] = 'ellipse'
    params = set()
    for e in edges:
        if e['from'].startswith(u'AWS::'):
            params.add(e['from'])
    graph['nodes'].extend({'name': n} for n in params)
    return graph


def extract_graph(name, elem):
    graph = {'name': name, 'nodes': [], 'edges': [], 'subgraphs': []}
    edges = []
    for item, details in elem.items():
        graph['nodes'].append({'name': item})
        edges.extend(flatten(find_refs(item, details)))
    return (graph, edges)


def find_refs(context, elem):
    if isinstance(elem, dict):
        refs = []
        for k, v in elem.items():
            if k == 'Ref':
                assert isinstance(v, str), 'Expected a string: %s' % v
                refs.append({'from': v, 'to': context})
            elif k == 'Fn::GetAtt':
                assert isinstance(v, list), 'Expected a list: %s' % v
                refs.append({'from': v[0], 'to': context})
            else:
                refs.extend(find_refs(context, v))
        return refs
    elif isinstance(elem, list):
        return map(lambda e: find_refs(context, e), elem)
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


