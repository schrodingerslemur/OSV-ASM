import re

from src.constants import opcode, funct_3, funct_7

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
    assembled_lines = []
    lines = content.splitlines()

    for idx in range(len(lines)):
        line = lines[idx].strip()

        # Comments or empty lines
        if line == '' or line.startswith('#'):
            continue 

        # Instructions
        # parse instruction
        tokens = re.split(r'[,\s()]+', line)
        instr = tokens[0]
        args = tokens[1:]

        # opcode
        if instr not in opcode:
            raise ValueError(f"Unknown instruction: {instr}")
        instr_opcode = opcode[instr]

        # handle different types
        # handle pseudo instructions
        pass

    return '\n'.join(assembled_lines)