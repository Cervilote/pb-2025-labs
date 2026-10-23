# tinycpu.py — учебный процессор TinyCPU-8
# Реализованы HLT и LDI. Остальные команды — задание.

MEM_SIZE = 256

HLT, LDA, STA, LDI, ADD, SUB, JMP, JZ, PUSH, POP, CALL, RET = range(12)

MNEMONICS = {
    HLT: "HLT", LDA: "LDA", STA: "STA", LDI: "LDI",
    ADD: "ADD", SUB: "SUB", JMP: "JMP", JZ: "JZ",
    PUSH: "PUSH", POP: "POP", CALL: "CALL", RET: "RET",
}


class TinyCPU:
    def __init__(self, memory=None):
        self.memory = list(memory or [0] * MEM_SIZE)
        self.memory += [0] * (MEM_SIZE - len(self.memory))
        self.pc = 0
        self.a = 0
        self.sp = 0xFF
        self.zero = False
        self.halted = False

    def fetch(self):
        """Прочитать байт по адресу PC и сдвинуть PC."""
        value = self.memory[self.pc]
        self.pc = (self.pc + 1) & 0xFF
        return value

    def set_a(self, value):
        self.a = value & 0xFF
        self.zero = (self.a == 0)

    def step(self):
        """Выполнить одну команду."""
        if self.halted:
            return
        opcode = self.fetch()

        if opcode == HLT:
            self.halted = True

        elif opcode == LDI:
            self.set_a(self.fetch())

        elif opcode == LDA:
            val = self.fetch()
            self.set_a(self.memory[val])
            #raise NotImplementedError("TODO: A = memory[addr]")

        elif opcode == STA:
            raise NotImplementedError("TODO: memory[addr] = A")

        elif opcode == ADD:
            raise NotImplementedError("TODO: A = A + memory[addr], обрезать до 8 бит")

        elif opcode == SUB:
            raise NotImplementedError("TODO: A = A - memory[addr], обрезать до 8 бит")

        elif opcode == JMP:
            val = self.fetch()
            self.pc = val
            # raise NotImplementedError("TODO: PC = addr")

        elif opcode == JZ:
            raise NotImplementedError("TODO: если A == 0, то PC = addr")

        elif opcode == PUSH:
            raise NotImplementedError("TODO: SP -= 1; memory[SP] = A")

        elif opcode == POP:
            raise NotImplementedError("TODO: A = memory[SP]; SP += 1")

        elif opcode == CALL:
            raise NotImplementedError("TODO: адрес СЛЕДУЮЩЕЙ команды на стек, PC = addr")

        elif opcode == RET:
            raise NotImplementedError("TODO: снять адрес со стека в PC")

        else:
            raise ValueError(f"неизвестный код операции: {opcode:02X} на адресе {self.pc - 1:02X}")

    def run(self, max_steps=10000):
        """Выполнять до остановки. Ограничитель спасает от вечного цикла."""
        steps = 0
        while not self.halted and steps < max_steps:
            self.step()
            steps += 1
        if steps >= max_steps:
            raise RuntimeError(f"превышено {max_steps} шагов — вероятно, бесконечный цикл")
        return steps

    def state(self):
        """Состояние машины наружу. Печатать здесь ничего нельзя."""
        return {
            "pc": self.pc, "a": self.a, "sp": self.sp,
            "zero": self.zero, "halted": self.halted,
            "memory": list(self.memory),
        }


if __name__ == "__main__":
    # LDI 7 / ADD 8 / STA 20 / HLT, в ячейке 8 лежит 5
    # program = [0x03, 0x07, 0x04, 0x08, 0x02, 0x14, 0x00, 0x00, 0x05]

    # LDI 7 / HLT
    program = [0x03, 0x07, 0x00]

    cpu = TinyCPU(program)

    print(cpu.state())
    cpu.run()
    print(cpu.state())
