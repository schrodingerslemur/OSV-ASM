import re
import sys

from src.constants import opcode, pseudo
from src.errors import *

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
        instruction = get_instruction(opcode_type, args)
        return instruction

def get_args(
    op: str,
    non_op: str,
    opcode_type: str,
    metadata: dict,
) -> list[str]: # include opcode too
    """Parses the all the parts into arguments based on opcode type."""
    args = [arg.strip() for arg in non_op.split(',')]

    # Valid number of arguments
    if opcode_type in ['R', 'I', 'SI', 'JI', 'B']:
        if len(args) != 3:
            raise InvalidArgumentError(f"Invalid number of arguments for {opcode_type}-type instruction: {op} {non_op}")

    elif opcode_type in ['LI', 'S', 'J']:
        if len(args) != 2:
            raise InvalidArgumentError(f"Invalid number of arguments for {opcode_type}-type instruction: {op} {non_op}")

    # Modify for S-type and LI-type
    if opcode_type in ['S', 'LI']:
        # args: rs2, offset(rs1)
        match = re.match(r'(-?\d+)\s*\(\s*(r[0-9]|1[0-9]|2[0-9]|3[0-1])\s*\)', args[1])
        if not match:
            raise InvalidArgumentError(f"Invalid S-type or LI-type argument format: {args[1]}")
        offset = match.group(1)
        rs1 = match.group(2)
        args = [args[0], rs1, offset]  # rs2, rs1, offset

        return [opcode[op][0]] + [get_register(args[0]), get_register(args[1]), check_imm(args[2])]
    
    elif opcode_type in ['J']:
        # args: rd, label
        return [opcode[op][0]] + [get_register(args[0]), args[1]]
    
    elif opcode_type in ['R']:
        # args: rd, rs1, rs2
        return [opcode[op][0]] + [get_register(args[0]), get_register(args[1]), get_register(args[2])]

    elif opcode_type in ['I', 'SI', 'JI']:
        # args: rd, rs1, imm
        return [opcode[op][0]] + [get_register(args[0]), get_register(args[1]), check_imm(args[2])]
    
    else:
        raise InvalidOperationError(f"Invalid opcode type: {opcode_type}")
    

def check_imm(
    imm_str: str
) -> str:
    """Validates an immediate value"""
    try:
        _ = int(imm_str)
    except ValueError:
        raise InvalidArgumentError(f"Invalid immediate value: {imm_str}")
    
    # TODO: ensure imm is within valid range based on instruction type
    return imm_str

def get_register(
    reg_str: str
) -> int:
    """Converts a register string to its integer representation."""
    if not re.match(r'r[0-9]|1[0-9]|2[0-9]|3[0-1]', reg_str):
        raise InvalidRegisterError(f"Invalid register: {reg_str}")
    return int(reg_str[1:])

def get_opcode_type(
    op: str
) -> str:
    """Retrieves the opcode and type for a given operation."""
    if op in pseudo:
        return 'PSEUDO'
    elif op in opcode:
        opcode_info = opcode[op]
        return opcode_info[1]
    else:
        raise InvalidOperationError(f"Invalid operation: {op}")
    
def parse_op(
    line: str
) -> tuple[str, str]:
    """Parses a line into operation and non-operation parts."""

    line = line.strip()
    match = re.search(r'\s*(\w+)\s+(.*)', line)
    if not match:
        raise MissingOperationError(f"Missing operation in line: {line}")
    return match.group(1).lower(), match.group(2).lower()

def handle_address_and_label(
    op: str,
    metadata: dict,
) -> None:
    """Handles label definitions in the assembly code."""
    labels = metadata['labels']
    if op.endswith(':'):
        labels[op[:-1]] = metadata['address']
    else:
        metadata['address'] += 4
    return

if __name__ == "__main__":
    assemble(sys.argv[1])