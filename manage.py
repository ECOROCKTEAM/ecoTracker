import click
from src.cli.cmd.translate.cmd import translate


@click.group()
def entry_point():
    pass


entry_point.add_command(translate)

if __name__ == "__main__":
    entry_point()
