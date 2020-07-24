"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    LDI = 0b10000010
    PRN = 0b01000111
    HLT = 0b00000001
    MUL = 0b10100010
    PUSH = 0b01000101
    POP = 0b01000110
    CALL = 0b01010000
    RET = 0b00010001
    ADD = 0b10100000
    CMP = 0b10100111
    JMP = 0b01010100
    JEQ = 0b01010101
    JNE = 0b01010110
    AND = 0b10101000
    OR = 0b10101010
    XOR = 0b10101011
    NOT = 0b01101001
    SHL = 0b10101100
    SHR = 0b10101101
    MOD = 0b10100100
    NOP = 0b00000000

    def __init__(self):
       self.ram = [0] * 256
       self.reg = [0] * 7 + [0xF4]
       self.pc = 0
       self.sp = 7 #(R7 is reserved for the SP)
       self.running = True

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py + filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    try:
                        # print("Line", line)
                        line = line.split("#", 1)[0]
                        line = int(line, 2)

                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Could not find file: {sys.argv[1]}")
            sys.exit(1)

        for instruction in self.reg:
            self.ram[address] = instruction
            address += 1


        # For now, we've just hardcoded a program:



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
            elif inst_reg == self.HLT:
                self.running = False
            elif inst_reg == self.LDI:
                self.reg[operand_a] = operand_b
            elif inst_reg == self.MUL:
                self.alu('MUL', operand_a, operand_b)
            elif inst_reg == self.PUSH:
                # sp = stack pointer
                self.reg[self.sp] -= 1
                self.reg[self.sp] &= 0xFF
                self.ram_write(self.reg[self.sp], self.reg[operand_a])

            elif inst_reg == self.POP:
                self.reg[operand_a] = self.ram_read(self.reg[self.sp])
                self.reg[self.sp] += 1

            elif inst_reg == self.CALL:
                return_address = self.pc + 2
                self.reg[self.sp] -= 1
                address_to_push_to = self.reg[self.sp]
                self.ram[address_to_push_to] = return_address
                subroutine_address = self.reg[operand_a]

                self.pc = subroutine_address

            elif inst_reg == self.RET:
                address_to_pop_from = self.reg[self.sp]
                return_addr = self.ram[address_to_pop_from]
                self.reg[self.sp] += 1

                # Set the PC to the return address
                self.pc = return_addr
            elif inst_reg == self.ADD:
                self.alu('ADD', operand_a, operand_b)



            # elif inst_reg == self.NOP:
            #     continue
            else:
                print(f"Unknown instruction {inst_reg} at {self.pc}")

            # print("REG", self.reg)
            # print("RAM", self.ram)

            if inst_reg != self.CALL and inst_reg != self.RET:
                offset = inst_reg >> 6
                self.pc += offset + 1
