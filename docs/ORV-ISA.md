# Instruction set architecture for ORV
Based on the base instructions on RISCV-32I

This implementation has **32** general purpose registers

## Types of instructions:
1. R-type: All register-only integer computation instructions
2. I-type: All register-immediate integer computation instructions
3. S-type: All store instructions
4. B-type: All branch instructions
5. U-type: Special instructions (e.g. LUI, AUIPC)
6. J-type: All jump instructions

## ORV ISA: 
### Pseudo-instructions:
1. .equ
2. .org
3. .dw

### R-type:
#### Instruction format:
| funct7 | rs2  | rs1  | funct3 | rd   | opcode |
|--------|------|------|--------|------|--------|
| 7 bits | 5 bits| 5 bits| 3 bits | 5 bits| 7 bits |

- All R-type instructions share the same opcodes: `0110011`
- funct3 and funct7 values define the specific instruction.

1. add
Format: `add rd, rs1, rs2`
Description: `rd = rs1 + rs2`
Op-codes: funct3 = `000`, funct7 = `0000000`

2. sub
Format: `sub rd, rs1, rs2`
Description: `rd = rs1 - rs2`
Op-codes: funct3 = `000`, funct7 = `0100000`

3. sll
Format: `sll rd, rs1, rs2`
Description: `rd = rs1 << rs2`
Op-codes: funct3 = `001`, funct7 = `0000000`

4. slt
Format: `slt rd, rs1, rs2`
Description: `rd = rs1 < rs2 ? 1 : 0`
Op-codes: funct3 = `010`, funct7 = `0000000`

5. sltu
Format: `sltu rd, rs1, rs2`
Description: `rd = rs1 < rs2 (unsigned) ? 1 : 0`
Op-codes: funct3 = `011`, funct7 = `0000000`

6. xor
Format: `xor rd, rs1, rs2`
Description: `rd = rs1 ^ rs2`
Op-codes: funct3 = `100`, funct7 = `0000000`

7. srl
Format: `srl rd, rs1, rs2`
Description: `rd = rs1 >> rs2 (logical)`
Op-codes: funct3 = `101`, funct7 = `0000000`

8. sra
Format: `sra rd, rs1, rs2`
Description: `rd = rs1 >> rs2 (arithmetic)`
Op-codes: funct3 = `101`, funct7 = `0100000`

9. or
Format: `or rd, rs1, rs2`
Description: `rd = rs1 | rs2`
Op-codes: funct3 = `110`, funct7 = `0000000`

10. and
Format: `and rd, rs1, rs2`
Description: `rd = rs1 & rs2`
Op-codes: funct3 = `111`, funct7 = `0000000`

### I-type:
#### Instruction format:
| imm[11:0] | rs1  | funct3 | rd   | opcode |
|------------|------|--------|------|--------|
| 12 bits    | 5 bits| 3 bits | 5 bits| 7 bits |

- All I-type instructions share the same opcodes: `0010011` (for arithmetic immediate), `0000011` (for load instructions) and `1100111` (for jalr)
- funct3 values define the specific instruction.
- slli, srli and srai use imm[4:0] as shamt (shift amount) and have specific funct7 values.

1. addi
Format: `addi rd, rs1, imm`
Description: `rd = rs1 + imm`
Op-codes: funct3 = `000`

2. slti
Format: `slti rd, rs1, imm`
Description: `rd = rs1 < imm ? 1 : 0`
Op-codes: funct3 = `010`

3. sltiu
Format: `sltiu rd, rs1, imm`
Description: `rd = rs1 < imm (unsigned) ? 1 : 0`
Op-codes: funct3 = `011`

4. xori
Format: `xori rd, rs1, imm`
Description: `rd = rs1 ^ imm`
Op-codes: funct3 = `100`

5. ori
Format: `ori rd, rs1, imm`
Description: `rd = rs1 | imm`
Op-codes: funct3 = `110`

6. andi
Format: `andi rd, rs1, imm`
Description: `rd = rs1 & imm`
Op-codes: funct3 = `111`

##### Sub-I type | Shamt instructions:

###### Format:
| funct7 | shamt | rs1  | funct3 | rd   | opcode |
|--------|-------|------|--------|------|--------|
| 7 bits | 5 bits| 5 bits| 3 bits | 5 bits| 7 bits |

- shamt is the shift amount, encoded in imm[4:0]
- opcode: `0010011`

7. slli
Format: `slli rd, rs1, shamt`
Description: `rd = rs1 << shamt`
Op-codes: funct3 = `001`, funct7 = `0000000`

8. srli 
Format: `srli rd, rs1, shamt`
Description: `rd = rs1 >> shamt (logical)`
Op-codes: funct3 = `101`, funct7 = `0000000`

9. srai 
Format: `srai rd, rs1, shamt`
Description: `rd = rs1 >> shamt (arithmetic)`
Op-codes: funct3 = `101`, funct7 = `0100000`

##### Sub-I type | Load instructions:

###### Format:
| offset | rs1  | funct3 | rd   | opcode |
|------------|------|--------|------|--------|
| 12 bits    | 5 bits| 3 bits | 5 bits| 7 bits |

- offset is the immediate value for memory addressing, encoded in imm[11:0]
- opcode: `0000011`

10. lb
Format: `lb rd, offset(rs1)`
Description: `rd = sign-extend(Mem[rs1 + offset][7:0])`
Op-codes: funct3 = `000`

11. lh
Format: `lh rd, offset(rs1)`
Description: `rd = sign-extend(Mem[rs1 + offset][15:0])`
Op-codes: funct3 = `001`

12. lw
Format: `lw rd, offset(rs1)`
Description: `rd = Mem[rs1 + offset][31:0]`
Op-codes: funct3 = `010`

13. lbu
Format: `lbu rd, offset(rs1)`
Description: `rd = zero-extend(Mem[rs1 + offset][7:0])`
Op-codes: funct3 = `100`

14. lhu
Format: `lhu rd, offset(rs1)`
Description: `rd = zero-extend(Mem[rs1 + offset][15:0])`
Op-codes: funct3 = `101`

###### Sub-I type | jalr instruction:
15. jalr
Format: `jalr rd, rs1, offset`
Description: `temp = pc + 4; pc = (rs1 + offset) & ~1; rd = temp`
Op-codes: funct3 = `000`, opcode = `1100111`


### S-type:
#### Instruction format:    
| offset[11:5] | rs2  | rs1  | funct3 | offset[4:0] | opcode |
|------------|------|------|--------|----------|--------|
| 7 bits     | 5 bits| 5 bits| 3 bits | 5 bits   | 7 bits |

- All S-type instructions share the same opcodes: `0100011`
- funct3 values define the specific instruction.
- offset is formed by concatenating imm[11:5] and imm[4:0]

1. sb
Format: `sb rs2, offset(rs1)`
Description: `Mem[rs1 + offset] = rs2[7:0]`
Op-codes: funct3 = `000`

2. sh
Format: `sh rs2, offset(rs1)`
Description: `Mem[rs1 + offset] = rs2[15:0]`
Op-codes: funct3 = `001`

3. sw
Format: `sw rs2, offset(rs1)`
Description: `Mem[rs1 + offset] = rs2[31:0]`
Op-codes: funct3 = `010`

### B-type:
#### Instruction format:
| imm[12/10:5] | rs2  | rs1  | funct3 | imm[4:1/11] | opcode |
|---------------|------|------|--------|--------------|--------|
| 7 bits        | 5 bits| 5 bits| 3 bits | 5 bits       | 7 bits |

- All B-type instructions share the same opcodes: `1100011`
- funct3 values define the specific instruction.

1. beq
Format: `beq rs1, rs2, offset`
Description: `if (rs1 == rs2) pc += offset`
Op-codes: funct3 = `000`

2. bne
Format: `bne rs1, rs2, offset`
Description: `if (rs1 != rs2) pc += offset`
Op-codes: funct3 = `001`

3. blt
Format: `blt rs1, rs2, offset`
Description: `if (rs1 < rs2) pc += offset`
Op-codes: funct3 = `100`

4. bge
Format: `bge rs1, rs2, offset`
Description: `if (rs1 >= rs2) pc += offset`
Op-codes: funct3 = `101`

5. bltu
Format: `bltu rs1, rs2, offset`
Description: `if (rs1 < rs2) pc += offset` (unsigned)
Op-codes: funct3 = `110`

6. bgeu
Format: `bgeu rs1, rs2, offset`
Description: `if (rs1 >= rs2) pc += offset` (unsigned)
Op-codes: funct3 = `111`

### U-type:
#### Instruction format:
| imm[31:12] | rd   | opcode |
|------------|------|--------|
| 20 bits    | 5 bits| 7 bits |

- Different opcodes

1. lui
Format: `lui rd, imm`
Description: `rd = imm[31:12] << 12`
Opcode: `0110111`

2. auipc
Format: `auipc rd, imm`
Description: `rd = pc + (imm[31:12] << 12)`
Opcode: `0010111`

### J-type:
#### Instruction format:
| imm[20/10:1/11/19:12] | rd   | opcode |
|-----------------------|------|--------|
| 20 bits               | 5 bits| 7 bits |

- All J-type instructions share the same opcodes: `1101111`

1. jal
Format: `jal rd, offset`
Description: `rd = pc + 4; pc += offset`


### Pseudo-instructions:
1. nop
Format: `nop`
Description: `addi x0, x0, 0`

2. mv
Format: `mv rd, rs`
Description: `addi rd, rs, 0`

3. li
Format: `li rd, imm`
Descripption: 
If imm fits in 12 bits: `addi rd, x0, imm`  
Else:  
```asm
lui rd, imm[31:12]
addi rd, rd, imm[11:0]
```

4. la
Format: `la rd, label`
Description:  
```asm
lui rd, %hi(label)
addi rd, rd, %lo(label)
```

5. not
Format: `not rd, rs`
Description: `xori rd, rs, -1`

6. neg
Format: `neg rd, rs`
Description: `sub rd, x0, rs`

7. negw
Format: `negw rd, rs`
Description: `subw rd, x0, rs`s


## For reference:

### Full RV32I instruction list: 
1. lui
2. auipc
3. addi
4. slti
5. sltiu
6. xori
7. ori
8. andi
9. slli
10. srli
11. srai
12. add
13. sub
14. sll
15. slt
16. sltu
17. xor
18. srl
19. sra
20. or
21. and
22. fence
23. fence.i
24. csrrw
25. csrrs
26. csrrc
27. csrrwi
28. csrrsi
29. csrrci
30. ecall
31. ebreak
32. uret
33. sret
34. mret
35. wfi
36. sfence.vma
37. lb
38. lh
39. lw
40. lbu
41. lhu
42. sb
43. sh
44. sw
45. jal
46. jalr
47. beq
48. bne
49. blt
50. bge
51. bltu
52. bgeu

