# Instruction set architecture for ORV
Based on the base instructions on RISCV-32I

Types of instructions:
1. R-type: All register-only integer computation instructions
2. I-type: All register-immediate integer computatio instructions
3. S-type: All store instructions
4. B-type: All branch instructions
5. U-type: Special instructions (e.g. LUI, AUIPC)
6. J-type: All jump instructions

ORV ISA: 
1. lui
Format: `lui rd, imm`
Type: U-type
Description: Moves top 20 bits of imm and 12 low bits with zeros into rd.

2. auipc
Format: `auipc rd, imm`
Type: 

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
22. lb
23. lh
24. lw
25. lbu
26. lhu
27. sb
28. sh
29. sw
30. jal
31. jalr
32. beq
33. bne
34. blt
35. bge
36. bltu
37. bgeu


Full RV32I instruction list: 
1. lui
Format: `lui rd, imm`
Type: U-type
Description: Moves top 20 bits of imm and 12 low bits with zeros into rd.

2. auipc
Format: `auipc rd, imm`
Type: 

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

