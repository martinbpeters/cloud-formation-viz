#!/usr/bin/env python

import sys
import click
from .parser import read_input
from .render import write_output

@click.command()
@click.argument("input", type=click.File("r"), default=sys.stdin)
@click.argument('output', type=click.File('w'), default=sys.stdout)
@click.version_option(message='Visualise AWS Cloudformation Templates, Version %(version)s')
@click.pass_context
def main(ctx, **kwargs):
    """

    INPUT input filename [default: stdin]
    
    OUTPUT output filename [default: stdout]
    """

    input_file = kwargs.pop('input')
    output_file = kwargs.pop('output')

    if input_file.name == "<stdin>" and sys.stdin.isatty():
        click.echo(ctx.get_help())
        ctx.exit()

    try:
        graph = read_input(input_file)
    except Exception as e:
        raise click.ClickException("{}".format(e))

    try:
        write_output(output_file, graph)
    except Exception as e:
        raise click.ClickException("{}".format(e))


if __name__ == '__main__':
    main()
