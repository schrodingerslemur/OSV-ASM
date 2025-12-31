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

    # Parse labels first
    for line in content.splitlines():
        # Comments or empty lines
        if line == '' or line.startswith('#'):
            continue 
        
        op, non_op = parse_op(line)
        handle_address_and_label(op, metadata)
    
    # Reset address
    metadata['address'] = 0

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
    # Operation-handling ----------------------------
    op, non_op = parse_op(line)            # Extract operation and non-operation parts

    if op.endswith(':'):
        return None  # Label-only line, no instruction to assemble

    # Label-handling ----------------
    # handle_address_and_label(op, metadata) # Updates metadata with labels and address

    # Instruction-handling --------------------------
    opcode_type = get_opcode_type(op)

    if opcode_type == 'PSEUDO':
        # Handle pseudo-instructions (and everything in this block) (resolved)
        args = get_pseudo_args(op, non_op, metadata) # # includes actual registers and immediates
        instructions = []
        for pseudo_inst in pseudo[op]:                  # does not include actual registers and immediates
            pseudo_inst = replace_args_in_pseudo(pseudo_inst, args)
            pseudo_op, pseudo_non_op = parse_op(pseudo_inst)
            pseudo_opcode_type = get_opcode_type(pseudo_op)
            normal_args = get_args(pseudo_op, pseudo_non_op, pseudo_opcode_type, metadata)
            instructions.append(get_instruction(pseudo_op, pseudo_opcode_type, normal_args))
        return instructions # list of instructions
    else:
        # Normal instruction
        args = get_args(op, non_op, opcode_type, metadata)
        instruction = get_instruction(op, opcode_type, args)
        return instruction

def replace_args_in_pseudo(
    pseudo_inst: str,
    args: list
) -> str:
    """Replaces placeholders in pseudo-instruction with actual arguments."""
    if len(args) == 0:
        return pseudo_inst
    elif len(args) == 1:
        rd = args[0]
        pseudo_inst = pseudo_inst.replace('x0', rd)
        return pseudo_inst
    elif len(args) == 2:
        rd, imm_or_rs = args[0], args[1]
        pseudo_inst = pseudo_inst.replace('x0', f'r{(int(rd,2))}').replace('IMM', f'{int(imm_or_rs, 2)}').replace('x1', f'r{(int(imm_or_rs,2))}')
        print(pseudo_inst)
        return pseudo_inst
    else:
        raise InvalidArgumentError(f"Invalid number of arguments for pseudo-instruction: {pseudo_inst} with args {args}")

def get_pseudo_args(
    op: str,
    non_op: str,
    metadata: dict
) -> dict:
    """Extracts arguments for pseudo-instructions."""
    args = [args.strip() for args in non_op.split(',')]
    if op in ['nop']:
       print(args)
       assert len(args) == 1 and args[0] == ''
       args = []
    elif op in ['not', 'neg']:
       assert len(args) == 1
       args = [get_register(args[0])]  # rd
    elif op in ['li']:
        assert len(args) == 2
        args = [get_register(args[0]), get_imm(args[1], metadata)]  # rd, imm
    elif op in ['mv']:
        assert len(args) == 2
        args = [get_register(args[0]), get_register(args[1])]  # rd, rs
    return args

if __name__ == "__main__":
    assemble(sys.argv[1])