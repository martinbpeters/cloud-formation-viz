#!/usr/bin/env python


def write_output(output_file, graph):
    dot_text = render(graph)
    
    output_file.write(dot_text)
    
    
def render(graph, subgraph=False):
    indent = '    ' if subgraph else '  '
    dot_text = '%s "%s" {\n' % ('  subgraph' if subgraph else 'digraph', graph['name'].strip())
    dot_text += '{}labeljust=l;\n'.format(indent)
    dot_text += '{}node [shape={}];\n'.format(indent, graph.get('shape', 'box'))

    if 'style' in graph:
        dot_text += '{}node [style="{}"]\n'.format(indent, graph['style'])

    if 'rank' in graph:
        dot_text += '{}rank={}\n'.format(indent, graph['rank'])

    for n in graph['nodes']:
        dot_text += '{}"{}"\n'.format(indent, n['name'])

    for s in graph['subgraphs']:
        dot_text += render(s, True) + '\n'

    for e in graph['edges']:
        dot_text += '{}"{}" -> "{}";\n'.format(indent, e['from'], e['to'])

    dot_text += '  }' if subgraph else '}'
    
    return dot_text
