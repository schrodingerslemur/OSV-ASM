import typer 
from typing import Annotated

import logging

app = typer.Typer(add_completion=False)

@app.command()
def main(
    file_name: Annotated[str, typer.argument(help="Name of the file to assemble")]
):
    """
    Assembles the specified file.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting assembly for file: {file_name}")
    
    # Open file and check it exists
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            logger.info("File exists")
    except FileNotFoundError:
        logger.error(f"File not found: {file_name}")
        return
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return
    