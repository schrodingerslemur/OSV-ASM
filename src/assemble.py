import re

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
            # handle different types
            # handle pseudo instructions
            pass

    return '\n'.join(assembled_lines)