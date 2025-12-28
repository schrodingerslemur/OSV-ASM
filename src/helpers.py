import re

from src.constants import *
from src.errors import *

def get_instruction(
    op: str,
    opcode_type: str,
    args: list[str],    
) -> str:
    """Generates the binary instruction based on opcode type and arguments."""
    # fix imm parsing (resolved)
    if opcode_type == 'R':
        funct7 = opcode[op][2]
        funct3 = opcode[op][3]
        rd, rs1, rs2 = args[1], args[2], args[3]
        instruction = funct7 + rs2 + rs1 + funct3 + rd + opcode[op][0]
    
    elif opcode_type == 'I':
        funct3 = opcode[op][2]
        rd, rs1, imm = args[1], args[2], args[3]
        assert len(imm) == 12, "Immediate must be 12 bits for I-type"
        instruction = imm + rs1 + funct3 + rd + opcode[op][0]
    
    elif opcode_type == 'SI':
        funct7 = opcode[op][2]
        funct3 = opcode[op][3]
        rd, rs1, imm = args[1], args[2], args[3][-5:] # shamt
        assert len(imm) == 5, "Shift amount must be 5 bits for SI-type"
        instruction = funct7 + imm + rs1 + funct3 + rd + opcode[op][0]
    
    elif opcode_type in ['LI', 'JI']: # add JI-type too (resolved)
        funct3 = opcode[op][2]
        rd, rs1, imm = args[1], args[2], args[3]
        instruction = imm + rs1 + funct3 + rd + opcode[op][0]
    
    elif opcode_type == 'S':
        funct3 = opcode[op][2]
        rs2, rs1, imm = args[1], args[2], args[3]
        imm_high = imm[:7] # imm[11:5]
        imm_low = imm[7:] # imm[4:0]
        instruction = imm_high + rs2 + rs1 + funct3 + imm_low + opcode[op][0]
    
    elif opcode_type == 'B':
        funct3 = opcode[op][2]
        rs1, rs2, imm = args[1], args[2], args[3]
        imm_bits = imm
        imm_12 = imm_bits[0]          # imm[12]
        imm_10_5 = imm_bits[1:7]      # imm[10:5]
        imm_4_1 = imm_bits[7:11]      # imm[4:1]
        imm_11 = imm_bits[11]         # imm[11]
        instruction = imm_12 + imm_10_5 + rs2 + rs1 + funct3 + imm_4_1 + imm_11 + opcode[op][0]

    elif opcode_type == 'U':
        rd, imm = args[1], args[2]
        instruction = imm + rd + opcode[op][0]
    
    elif opcode_type == 'J':
        rd, imm = args[1], args[2]
        instruction = imm + rd + opcode[op][0]
    
    else:
        raise InvalidOperationError(f"Invalid opcode type: {opcode_type}")

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

    # handling for labels and using metadata (resolved using get_imm)
    # completely wrong, handle funct7, funct3, opcode properly (resolved, do this in get_instruction)

    # Modify for S-type and LI-type
    if opcode_type in ['S', 'LI']:
        # args: rs2, offset(rs1)
        match = re.match(r'(-?\d+)\s*\(\s*(r[0-9]|1[0-9]|2[0-9]|3[0-1])\s*\)', args[1])
        if not match:
            raise InvalidArgumentError(f"Invalid S-type or LI-type argument format: {args[1]}")
        offset = match.group(1)
        rs1 = match.group(2)
        args = [args[0], rs1, offset]  # rs2, rs1, offset

        return [opcode[op][0]] + [get_register(args[0]), get_register(args[1]), get_imm(args[2], metadata, type=opcode_type)]
    
    elif opcode_type in ['J']:
        # args: rd, label
        return [opcode[op][0]] + [get_register(args[0]), get_imm(args[1], metadata, type=opcode_type)]
    
    elif opcode_type in ['R']:
        # args: rd, rs1, rs2
        return [opcode[op][0]] + [get_register(args[0]), get_register(args[1]), get_register(args[2])]

    elif opcode_type in ['I', 'SI', 'JI']:
        # args: rd, rs1, imm
        return [opcode[op][0]] + [get_register(args[0]), get_register(args[1]), get_imm(args[2], metadata, type=opcode_type)]
    
    else:
        raise InvalidOperationError(f"Invalid opcode type: {opcode_type}")
    

def get_imm(
    imm_str: str,
    metadata: dict,
    type: str = 'I'
) -> str:
    """Validates an immediate value"""
    # handle different bit-widths based on instruction type (resolved)
    # I-type: 12 bits, S-type: 12 bits, B-type: 12 bits, U-type: 20 bits, J-type: 20 bits
    try:
        imm = int(imm_str)
    except ValueError:
        if imm_str in metadata['labels']:
            return format(metadata['labels'][imm_str], '012b')
        else:
            raise InvalidArgumentError(f"Invalid immediate value: {imm_str}")
    
    if type in ['I', 'S', 'B', 'LI', 'SI']: # handle splitting in two parts in get_instruction
        # 12-bit immediate
        bits = 12
    elif type in ['U', 'J']:
        # 20-bit immediate
        bits = 20
    else:
        raise InvalidOperationError(f"Invalid immediate type: {type}")

    imm = imm & ((1 << bits) - 1)  # Mask to required bits
    return format(imm, f'0{bits}b')

def get_register(
    reg_str: str
) -> int:
    """Converts a register string to its integer representation."""
    if not re.match(r'r[0-9]|1[0-9]|2[0-9]|3[0-1]', reg_str):
        raise InvalidRegisterError(f"Invalid register: {reg_str}")
    return format(int(reg_str[1:]), '05b')

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