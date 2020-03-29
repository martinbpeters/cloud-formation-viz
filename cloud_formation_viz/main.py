#!/usr/bin/env python

import sys
import click
from .parser import cfn_parser
from .render import write_output

@click.command()
@click.argument("input", type=click.File("r"), default=sys.stdin)
@click.argument('output', type=click.File('w'), default=sys.stdout)
@click.option('--unique-edges/--no-unique-edges', default=True)
@click.option('--parameters/--no-parameters', default=True)
@click.option('--outputs/--no-outputs', default=True)
@click.option('--pseudo/--no-pseudo', default=True)
@click.option('--globals/--no-globals', default=True)
@click.version_option(message='Visualise AWS Cloudformation Templates, Version %(version)s')
@click.pass_context
def main(ctx, **kwargs):
    """

    INPUT input filename [default: stdin]
    
    OUTPUT output filename [default: stdout]
    """
    input_file = kwargs.pop('input')
    output_file = kwargs.pop('output')
    parameters_bool = kwargs.pop('parameters')
    outputs_bool = kwargs.pop('outputs')
    pseudo_bool = kwargs.pop('pseudo')
    globals_bool = kwargs.pop('globals')
    unique_edges_bool = kwargs.pop('unique_edges')

    if input_file.name == "<stdin>" and sys.stdin.isatty():
        click.echo(ctx.get_help())
        ctx.exit()

    try:
        cfn_parser_obj = cfn_parser(
            parameters_bool, outputs_bool, 
            pseudo_bool, globals_bool
        )
        graph = cfn_parser_obj.read_input(input_file)
    except Exception as e:
        raise click.ClickException("{}".format(e))

    try:
        write_output(output_file, graph, unique_edges_bool)
    except Exception as e:
        raise click.ClickException("{}".format(e))


if __name__ == '__main__':
    main()
