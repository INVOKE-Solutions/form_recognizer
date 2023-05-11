# NOTE 
"""
CLI has the following functionality:
- To execute the model parsing 
"""
import typer
from typing import Optional
from formcli import __appname__, __version__
from main_project.form_recog import analyze_document

from main_project.form_recog import analyze_document, \
                        key_val_extraction, \
                        display_basic_info, \
                        display_item_description

app = typer.Typer()

def __version_callback(value:bool)-> None:
    if value:
        typer.echo(f"{__appname__}: v {__version__}")
        raise typer.Exit()


@app.callback()
def main(version:Optional[bool] = typer.Option(
    None, "--version", "-v", help="Show project version and exit", 
    callback=__version_callback, 
    is_eager=True
)):
    return

@app.command(name="parse")
def parse_document(
                docURL:str=typer.Option(
                    False, 
                    "--link", 
                    help="URL link of document"
                ),
                docPath:str=typer.Option(
                    False, 
                    "--locpath", 
                    help="Document local path"
                ), 
                doc_is_url:bool=typer.Option(
                    False, 
                    "--URLdoc", 
                    help="Document URL link"
                )
                
                ):
    document_result = analyze_document(
                    docPath=docPath, 
                    docURL=docURL, 
                    doc_is_url=doc_is_url,
                    prebuilt_model="prebuilt-invoice")
    basic_information = display_basic_info(document_result)
    desc_information = display_item_description(document_result)

    typer.secho(
        f"Basic Information: {basic_information}", 
        fg=typer.colors.GREEN
    )
    typer.secho(
        f"Desc Information: {desc_information}", 
        fg=typer.colors.BLUE
    )

