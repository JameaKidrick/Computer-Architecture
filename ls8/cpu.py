"""CPU functionality."""

import sys

# Parse the command line

# print(sys.argv[1])

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 9
        self.hlt = int('00000001', 2)
        self.ldi = int('10000010', 2)
        self.prn = int('01000111', 2)
        self.mul = int('10100010', 2)
        # LDI - load "immediate", store a value in a register, or "set this register to this value".
        # 10000010 00000rrr iiiiiiii
        # 82 0r ii
        # PRN - a pseudo-instruction that prints the numeric value stored in a register.
        # 01000111 00000rrr
        # 47 0r
        # HLT - halt the CPU and exit the emulator.
        # 00000001 
        # 01

    def ram_read(self, mar):
        '''
        Accepts the address to read and return the value stored there
        Memory Address Register (mar) - contains the address that is being read or written to.
        '''
        return self.reg[mar]

    def ram_write(self, mdr, mar):
        '''
        Accepts a value to write, and the address to write it to
        Memory Data Register (mdr) - contains the data that was read or the data to write
        '''
        # print(f'BEFORE WRITING {mdr}: {self.reg[mar]}')
        self.reg[mar] = mdr
        # print(f'AFTER WRITING {mdr}: {self.reg[mar]}')

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        # OPEN FILE
        if len(sys.argv) == 2:
            program_filename = sys.argv[1]
            with open(program_filename) as f:
                # LOOP THROUGH EACH LINE IN THE FILE
                for line in f:
                    # SPLIT AT ANY POINT THERE IS A #
                    line = line.split('#')
                    # REMOVE THE FIRST PART OF THE SPLIT (EVERYTHING BEFORE THE #)
                    line = line[0].strip()

                    # IF THE LINE IS EMPTY, CONTINUE
                    if line == '':
                        continue

                    # CONVERT LINE TO INTEGER AND ADD LINE TO ADDRESS
                    self.ram[address] = (int(line, 2))
                    address += 1
        else:
            print('File undefined: Please input `cpu.py [file_name].py` to define the file you want to run.')
            exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        '''
        Run the CPU.
        Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them.
        Then, depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec.
        After running code for any particular instruction, the `PC` needs to be updated to point to the next instruction for the next iteration of the loop in `run()`.
        '''
        pc = 0

        while True:
            operand_a = self.ram[pc + 1]
            operand_b = self.ram[pc + 2]
            if self.ram[pc] == self.ldi: # LDI
                '''
                Set the value of a register to an integer.
                '''
                # pc += 0b10
                self.ram_write(operand_b, operand_a)
                pc += 3
            elif self.ram[pc] == self.mul: # MUL
                '''
                Multiply the values in two registers together and store the result in registerA
                '''
                self.ram_write(self.ram_read(operand_a) * self.ram_read(operand_b), operand_a)
                pc += 3
            elif self.ram[pc] == self.prn: # PRN
                '''
                Print numeric value stored in the given register.

                Print to the console the decimal integer value that is stored in the given register.
                '''
                print(self.ram_read(operand_a))
                pc += 2
            elif self.ram[pc] == self.hlt: # HLT
                '''
                Halt the CPU (and exit the emulator).
                '''
                return False
