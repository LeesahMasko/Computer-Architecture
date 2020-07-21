"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    LDI = 0b10000010
    PRN = 0b01000111
    HLT = 0b00000001
    MUL = 0b10100010

    def __init__(self):
       self.ram = [0] * 256
       self.reg = [0] * 8
       self.pc = 0
       self.running = True

    def load(self, program = None):
        """Load a program into memory."""
        memory = [0] * 256
        address = 0
        with open(program) as file:
            for line in file:
                try:
                    line = line.split("#", 1)[0]
                    line = int(line, 2)
                    memory[address] = line
                    address += 1
                except ValueError


        # For now, we've just hardcoded a program:

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

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

# LDI = 0b10000010
# PRN = 0b01000111
# HLT = 0b00000001
    def run(self):
        """Run the CPU."""
        while self.running:
            # instructions register = inst_reg
            inst_reg = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # register number = reg_num
            if inst_reg == self.PRN:
                print(self.reg[operand_a])
            if inst_reg == self.HLT:
                self.running = False
            if inst_reg == self.LDI:
                self.reg[operand_a] = operand_b
            if inst_reg == self.MUL:
                self.reg[operand_a] *= self.reg[operand_b]


            offset = inst_reg >> 6
            self.pc += offset + 1
