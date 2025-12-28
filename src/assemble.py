import re
import sys

from src.constants import opcode, pseudo
from src.errors import *
from src.helpers import *

def assemble(
        content: str
) -> str:
    """
    The function takes plain text RISCV 32I ISA instructions and assembles it into binary machine code.
    
    :param content: .asm file content
    :type content: str
    :return: assembled content in binary
    :rtype: str
    """
    metadata = {
        'labels': {},
        'address': 0,
    }

    assembled_lines = []

    for line in content.splitlines():
        # Comments or empty lines
        if line == '' or line.startswith('#'):
            continue 
        
        assembled_line = assemble_line(line, metadata)

        if assembled_line:
            if isinstance(assembled_line, list):
                assembled_lines.extend(assembled_line)
            else:
                assembled_lines.append(assembled_line)

    return '\n'.join(assembled_lines)

def assemble_line(
        line: str,
        metadata: dict
) -> str:
    """
    Assembles a single line of RISCV 32I ISA instruction into binary machine code.
    
    :param line: single line of .asm file content
    :type line: str
    :param metadata: dictionary containing labels and address
    :type metadata: dict
    :return: assembled line in binary
    :rtype: str
    """
    labels = metadata['labels']

    # Operation-handling ----------------------------
    op, non_op = parse_op(line)            # Extract operation and non-operation parts

    # Label-handling ----------------
    handle_address_and_label(op, metadata) # Updates metadata with labels and address

    # Instruction-handling --------------------------
    opcode_type = get_opcode_type(op)

    if opcode_type == 'PSEUDO':
        # TODO: Handle pseudo-instructions (and everything in this block)
        args = get_pseudo_args(op, non_op, metadata)
        for pseudo_inst in pseudo[op]:
            pseudo_op, pseudo_non_op = parse_op(pseudo_inst)
            pseudo_opcode, pseudo_opcode_type = get_opcode_and_type(pseudo_op)
            instructions = get_instruction(pseudo_op, pseudo_non_op, pseudo_opcode, pseudo_opcode_type, metadata)
            return instructions # list of instructions
    else:
        # Normal instruction
        args = get_args(op, non_op, opcode_type, metadata)
        instruction = get_instruction(op, opcode_type, args)
        return instruction


if __name__ == "__main__":
    assemble(sys.argv[1])