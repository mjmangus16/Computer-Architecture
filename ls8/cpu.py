"""CPU functionality."""

import sys

# python3 file.py filename


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.running = False
        self.sp = 7
        self.equal = 0
        self.lesser = 0
        self.greater = 0
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JNE = 0b01010110
        self.JEQ = 0b01010101
        self.PUSH = 0b01000101
        self.POP = 0b01000110

    def load(self):
        """Load a program into self.ram."""

        address = 0
        # program = []
        # For now, we've just hardcoded a program:

        if len(sys.argv) != 2:
            print("Usage: file.py filename", file=sys.stderr)
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                container = []
                for line in f:
                    # ignore comments
                    comment_split = line.split("#")

                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    container.append(num)
                    program = [int(c, 2) for c in container]

        except FileNotFoundError:
            print(f"{sys.argv[0]}! {sys.argv[1]} not found")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        self.run_start()

        while self.running:
            command = self.ram_read(self.pc)

            if command == self.HLT:
                self.run_HLT()

            elif command == self.LDI:
                self.run_LDI()

            elif command == self.PRN:
                self.run_PRN()

            elif command == self.MUL:
                self.run_MUL()

            elif command == self.PUSH:
                self.run_PUSH()

            elif command == self.POP:
                self.run_POP()

            elif command == self.CMP:
                self.run_CMP()

            elif command == self.JMP:
                self.run_JMP()

            elif command == self.JEQ:
                self.run_JEQ()

            elif command == self.JNE:
                self.run_JNE()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return

    def run_start(self):
        print("Program Started")
        self.running = True

    def run_HLT(self):
        # print(self.register)
        print("Program Ended")
        self.running = False
        self.pc = 0

    def run_LDI(self):
        self.register[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3

    def run_PRN(self):
        print(self.register[self.ram_read(self.pc+1)])
        self.pc += 2

    def run_MUL(self):
        print(self.register)
        self.register[self.ram_read(self.pc+1)] = self.register[
            self.ram_read(self.pc+1)] * self.register[self.ram_read(self.pc+2)]
        self.pc += 3

    def run_PUSH(self):
        reg = self.ram[self.pc + 1]
        val = self.register[reg]
        self.register[self.sp] -= 1
        self.ram[self.register[self.sp]] = val
        self.pc += 2

    def run_POP(self):
        reg = self.ram[self.pc + 1]
        val = self.ram[self.register[self.sp]]
        self.register[reg] = val
        self.register[self.sp] += 1
        self.pc += 2

    def run_CMP(self):
        if self.register[self.ram_read(self.pc+1)] > self.register[self.ram_read(self.pc+2)]:
            self.greater = 1
            self.equal = 0
            self.lesser = 0
        elif self.register[self.ram_read(self.pc+1)] == self.register[self.ram_read(self.pc+2)]:
            self.greater = 0
            self.equal = 1
            self.lesser = 0
        elif self.register[self.ram_read(self.pc+1)] < self.register[self.ram_read(self.pc+2)]:
            self.greater = 0
            self.equal = 0
            self.lesser = 1
        self.pc += 3

    def run_JMP(self):
        self.pc = self.register[self.ram_read(self.pc+1)]

    def run_JEQ(self):
        if self.equal == 1:
            self.pc = self.register[self.ram_read(self.pc+1)]
        else:
            self.pc += 2

    def run_JNE(self):
        if self.equal == 0:
            self.pc = self.register[self.ram_read(self.pc+1)]
        else:
            self.pc += 2


cpu = CPU()

cpu.run()
