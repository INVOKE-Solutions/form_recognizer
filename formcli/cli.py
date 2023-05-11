# NOTE 
"""
CLI has the following functionality:
- To execute the model parsing 
"""
import typer
from typing import Optional
from main_project import __appname__, __version__

app = typer.Typer()


@app.callback()
def main(version:Optional[bool] = typer.Option(
    None, "--version", "-v", help="Show project version and exit"
)):
    print(f"{__appname__}: v_{__version__}")