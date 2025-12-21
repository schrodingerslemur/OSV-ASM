import typer 
from typing import Annotated

import logging

from assemble import assemble

app = typer.Typer(add_completion=False)

@app.command()
def main(
    file_name: Annotated[str, typer.Argument(help="Name of the file to assemble")]
) -> None:
    """
    This functions takes in a '.asm' file name as input and writes the assembled machine code into a file of same name but with extension 'list'
    
    :param file_name: '.asm' file path to be assembled
    :type file_name: str
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting assembly for file: {file_name}...")

    # Check extension
    logger.info("Checking file extension...")
    if not file_name.endswith('.asm'):
        logger.error("File must have a .asm extension")
        return
    
    # Open file and check it exists
    logger.info("Checking file exists...")
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
    
    # Assemble file
    logger.info("Assembling file...")
    try:
        assembled_content = assemble(content)
        output_file_name = file_name.replace('.asm', '.list')
        with open(output_file_name, 'w') as output_file:
            output_file.write(assembled_content)
        logger.info(f"Assembly complete. Output written to {output_file_name}")
    except Exception as e:
        logger.error(f"An error occurred during assembly: {e}")
    
    return

if __name__ == "__main__":  
    app()
    
