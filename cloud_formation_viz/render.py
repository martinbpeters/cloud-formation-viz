#!/usr/bin/env python


def write_output(output_file, graph, unique_edges_bool):
    dot_text = render(
        graph=graph, node_set=set(), 
        subgraph=False, 
        unique_edges_bool=unique_edges_bool
    )
    
    output_file.write(dot_text)
    
    
def render(graph, node_set, subgraph, unique_edges_bool):
    indent = '    ' if subgraph else '  '
    dot_text = '%s "%s" {\n' % ('  subgraph' if subgraph else 'digraph', graph['name'].strip())
    dot_text += '{}labeljust=l;\n'.format(indent)
    dot_text += '{}node [shape={}];\n'.format(indent, graph.get('shape', 'box'))

    if 'style' in graph:
        dot_text += '{}node [style="{}"]\n'.format(indent, graph['style'])

    if 'rank' in graph:
        dot_text += '{}rank={}\n'.format(indent, graph['rank'])

    for n in graph['nodes']:
        node_set.add(n['name'])
        dot_text += '{}"{}"\n'.format(indent, n['name'])

    for s in graph['subgraphs']:
        dot_text += render(s, node_set, True, unique_edges_bool) + '\n'

    def clean_edge(edge):
        return edge.split('.')[0]

    edges = []
    if unique_edges_bool:
        edges = set()

    for e in graph['edges']:        
        e_from = clean_edge(e['from'])
        e_to = clean_edge(e['to'])
        if e_from in node_set and e_to in node_set:
            if unique_edges_bool:
                edges.add('{}"{}" -> "{}";\n'.format(indent, e_from, e_to))
            else:
                edges.append('{}"{}" -> "{}";\n'.format(indent, e_from, e_to))

    for edge in edges:
        dot_text += edge

    dot_text += '  }' if subgraph else '}'
    
    return dot_text
