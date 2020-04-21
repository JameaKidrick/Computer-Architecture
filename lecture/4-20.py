# Write a program in Python that runs programs

print_mea = 1
halt = 2
save_reg = 3 # Store a value in a register (in the LS8 called LDI)
print_reg = 4 # Corresponds to PRN in LS8

memory = [
  print_mea,
  save_reg, #SAVE R0, 37       store 37 in R0        the opcode
  0,  # R0     operand ('argument')
  37, # 37     operand ('argument')
  print_mea,
  print_reg, # Print R0
  0,
  halt

]

register = [0] * 8

pc = 0 # Program Counter, the address of the current instruction
running = True

while running:
  inst = memory[pc]
  for inst in memory:
    if inst == print_mea:
      print('MEA!')
      pc += 1
    elif inst == save_reg:
      reg_number = memory[pc + 1]
      reg_value = memory[pc + 2]
      register[reg_number] = reg_value
      pc += 3
    elif inst == print_reg:
      reg_number = memory[pc + 1]
      print(register[reg_number])
      pc += 2
    elif inst == halt:
      running = False
