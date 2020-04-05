#!/usr/bin/env python

from .aws import resource_type_image
from .render_settings import settings
from .aws import groups

def write_output(output_file, graph, unique_edges_bool, icons_path):
    dot_text = render(
        graph=graph, node_set=set(), 
        subgraph=False, 
        unique_edges_bool=unique_edges_bool,
        icons_path=icons_path
    )
    
    output_file.write(dot_text)
    
    
def render(graph, node_set, subgraph, unique_edges_bool, icons_path):
    indent = '    ' if subgraph else '  '
    dot_text = '%s "%s" {\n' % ('\n  subgraph' if subgraph else 'digraph', graph['name'].strip())

    if subgraph is False:
        dot_text += 'compound={};\n'.format(settings['default']['compound'])
        dot_text += 'ranksep={};\n'.format(settings['default']['ranksep'])
        dot_text += 'splines={};\n'.format(settings['default']['splines'])
        if 'bgcolour' in settings['default']:
            dot_text += 'bgcolor={};\n'.format(settings['default']['bgcolor'])
        if 'rankdir' in settings['default']:
            dot_text += 'rankdir={};\n'.format(settings['default']['rankdir'])

        dot_text += '{}labeljust=l;\n'.format(indent)

    dot_text += '{}node [shape={}];\n'.format(
        indent,
        graph.get('shape', 'box, style=\"setlinewidth(0)\"')
    )
    dot_text += '{}edge [arrowhead="{}"];\n'.format(
        indent,
        settings['default']['arrowType']
    )

    # if 'style' in graph:
    #     dot_text += '{}node [style="{}"]\n'.format(indent, graph['style'])

    if 'rank' in graph:
        dot_text += '{}rank={}\n'.format(indent, graph['rank'])

    if subgraph is False:
        dot_text += '\nsubgraph cluster_aws_cloud {\n'
        dot_text += 'style="setlinewidth(1)";\n'#\nstyle=filled;\ncolor=lightgrey;\n'

        if icons_path:
            dot_text += 'label=' + '< <table border="0" cellborder="0" cellspacing="0"><tr>\n'
            node_image = node_image = icons_path + 'AWS-Cloud-alt_light-bg@4x.png'
            dot_text += '<td fixedsize="true" height="100" width="100" valign="top" align="left">\n'
            dot_text += f'<img src="{node_image}"/>\n'
            dot_text += '</td>\n'

            dot_text += '<td><font color="black" point-size="20">'
            dot_text += '{}</font></td></tr></table> >\n'.format('AWS Cloud')
            dot_text += ';\n'
        else:
            dot_text += 'label="AWS Cloud";\n'

    for n in graph['nodes']:
        #node_type = n['type']
        #node_level = groups[n['type']] if node_type in groups else groups['Default']
        #print("name:{} type:{} level:{}".format(n['name'], node_type, node_level))
        node_set.add(n['name'])

        if icons_path:
            node_image = ''
            if n['type'] in resource_type_image:
                node_image = icons_path + resource_type_image[n['type']]

            dot_text += '{}"{}"[\n'.format(indent, n['name'])
            dot_text += 'URL=\"' + "" + '\", \n'

            if graph['name'] in ['Parameters', 'Outputs']:
                dot_text += 'style=\"filled,rounded\",\n'
            else:
                if node_image == "":
                    dot_text += 'style=\"setlinewidth(1)\",\n'

            dot_text += 'label=' + '< <table border="0" cellborder="0" cellspacing="0"><tr>\n'
            if node_image != "":
                dot_text += '<td fixedsize="true" height="100" width="100" valign="bottom" align="center">\n'
                dot_text += f'<img src="{node_image}"/>\n'
                dot_text += '</td></tr><tr>\n'

            dot_text += '<td><font color="black" point-size="20">'
            dot_text += '{}</font></td></tr></table> >\n'.format(n['name'])
            dot_text += '];\n'
        else:
            dot_text += '{}"{}"\n'.format(indent, n['name'])

    for s in graph['subgraphs']:
        dot_text += render(s, node_set, True, unique_edges_bool, icons_path) + '\n'

    def clean_edge(edge):
        return edge.split('.')[0]

    edges = []
    if unique_edges_bool:
        edges = set()

    for e in graph['edges']:
        e_from = clean_edge(e['from'])
        e_to = clean_edge(e['to'])
        e_type = clean_edge(e['type'])
        e_type_str = ''
        if e_type == 'DependsOn':
            e_type_str = '[color="red";]'

        if e_from in node_set and e_to in node_set:
            if unique_edges_bool:
                edges.add('{}"{}" -> "{}" {};\n'.format(indent, e_from, e_to, e_type_str))
            else:
                edges.append('{}"{}" -> "{}" {};\n'.format(indent, e_from, e_to, e_type_str))

    for edge in edges:
        dot_text += edge

    dot_text += '  }' if subgraph else '}'

    if subgraph is False:
        dot_text += '}'

    return dot_text
