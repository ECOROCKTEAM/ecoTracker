import click

from src.cli.cmd.develop import develop
from src.cli.cmd.translate import translate


@click.group()
def entry_point():
    pass


entry_point.add_command(translate)
entry_point.add_command(develop)

if __name__ == "__main__":
    entry_point()
