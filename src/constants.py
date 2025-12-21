opcode = {
    # R-type
    "add":   0b0110011,
    "sub":   0b0110011,
    "sll":   0b0110011,
    "slt":   0b0110011,
    "sltu":  0b0110011,
    "xor":   0b0110011,
    "srl":   0b0110011,
    "sra":   0b0110011,
    "or":    0b0110011,
    "and":   0b0110011,

    # I-type (ALU)
    "addi":  0b0010011,
    "slti":  0b0010011,
    "sltiu": 0b0010011,
    "xori":  0b0010011,
    "ori":   0b0010011,
    "andi":  0b0010011,
    "slli":  0b0010011,
    "srli":  0b0010011,
    "srai":  0b0010011,

    # Loads (I-type)
    "lb":    0b0000011,
    "lh":    0b0000011,
    "lw":    0b0000011,
    "lbu":   0b0000011,
    "lhu":   0b0000011,

    # Stores (S-type)
    "sb":    0b0100011,
    "sh":    0b0100011,
    "sw":    0b0100011,

    # Branches (B-type)
    "beq":   0b1100011,
    "bne":   0b1100011,
    "blt":   0b1100011,
    "bge":   0b1100011,
    "bltu":  0b1100011,
    "bgeu":  0b1100011,

    # U-type
    "lui":   0b0110111,
    "auipc": 0b0010111,

    # J-type
    "jal":   0b1101111,
    "jalr":  0b1100111,
}

funct_3 = {
    # R-type
    "add":   0b000,
    "sub":   0b000,
    "sll":   0b001,
    "slt":   0b010,
    "sltu":  0b011,
    "xor":   0b100,
    "srl":   0b101,
    "sra":   0b101,
    "or":    0b110,
    "and":   0b111,

    # I-type (ALU)
    "addi":  0b000,
    "slti":  0b010,
    "sltiu": 0b011,
    "xori":  0b100,
    "ori":   0b110,
    "andi":  0b111,
    "slli":  0b001,
    "srli":  0b101,
    "srai":  0b101,

    # Loads
    "lb":    0b000,
    "lh":    0b001,
    "lw":    0b010,
    "lbu":   0b100,
    "lhu":   0b101,

    # Stores
    "sb":    0b000,
    "sh":    0b001,
    "sw":    0b010,

    # Branches
    "beq":   0b000,
    "bne":   0b001,
    "blt":   0b100,
    "bge":   0b101,
    "bltu":  0b110,
    "bgeu":  0b111,

    # J-type / special
    "jalr":  0b000,
}

funct_7 = {
    # R-type
    "add":   0b0000000,
    "sub":   0b0100000,
    "sll":   0b0000000,
    "slt":   0b0000000,
    "sltu":  0b0000000,
    "xor":   0b0000000,
    "srl":   0b0000000,
    "sra":   0b0100000,
    "or":    0b0000000,
    "and":   0b0000000,

    # I-type shifts (encoded in imm[11:5])
    "slli":  0b0000000,
    "srli":  0b0000000,
    "srai":  0b0100000,
}
