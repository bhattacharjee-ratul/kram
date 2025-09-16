"""Console script for pykram."""

import typer
from rich.console import Console

from pykram import utils

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for pykram."""
    console.print("Replace this message by putting your code into "
               "pykram.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
