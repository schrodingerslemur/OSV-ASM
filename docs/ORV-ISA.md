# Instruction set architecture for ORV
Based on RISCV-32I

1. lui
Format: `lui rd, imm`
Type: U-type
Description: Moves top 20 bits of imm and 12 low bits with zeros into rd.

2. auipc
Format: `auipc rd, imm`
