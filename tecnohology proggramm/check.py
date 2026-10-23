# check.py — проверка эмулятора студента
import sys
from tinycpu import TinyCPU

# (имя, программа в байтах, {адрес: ожидаемое значение}, ожидаемый A)
TESTS = [
    ("LDI",        [0x03, 0x07, 0x00],                                  {},          7),
    ("LDA",        [0x01, 0x05, 0x00, 0x00, 0x00, 0x2A],                {},         42),
    ("STA",        [0x03, 0x09, 0x02, 0x20, 0x00],                      {0x20: 9},   9),
    ("ADD",        [0x03, 0x07, 0x04, 0x06, 0x00, 0x00, 0x05],          {},         12),
    ("SUB",        [0x03, 0x0A, 0x05, 0x06, 0x00, 0x00, 0x03],          {},          7),
    ("переполнение",[0x03, 0xC8, 0x04, 0x06, 0x00, 0x00, 0x64],         {},         44),
    ("JMP",        [0x06, 0x04, 0x00, 0x00, 0x03, 0x01, 0x00],          {},          1),
    ("JZ взят",    [0x03, 0x00, 0x07, 0x06, 0x00, 0x00, 0x03, 0x05, 0x00], {},       5),
    ("JZ не взят", [0x03, 0x01, 0x07, 0x06, 0x00, 0x00, 0x03, 0x05, 0x00], {},       1),
    ("PUSH/POP",   [0x03, 0x0F, 0x08, 0x03, 0x01, 0x09, 0x00],          {},         15),
    ("CALL/RET",   [0x0A, 0x05, 0x02, 0x30, 0x00, 0x03, 0x63, 0x0B],    {0x30: 99}, 99),
]


def run_tests():
    passed = failed = 0
    for name, program, expected_mem, expected_a in TESTS:
        try:
            cpu = TinyCPU(program)
            cpu.run()
            problems = []
            if cpu.a != expected_a:
                problems.append(f"A = {cpu.a}, ожидалось {expected_a}")
            for addr, value in expected_mem.items():
                if cpu.memory[addr] != value:
                    problems.append(f"memory[{addr:02X}] = {cpu.memory[addr]}, ожидалось {value}")
            if problems:
                print(f"[ПАДЕНИЕ] {name}: {'; '.join(problems)}")
                failed += 1
            else:
                print(f"[ok]      {name}")
                passed += 1
        except NotImplementedError as e:
            print(f"[НЕ СДЕЛАНО] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ОШИБКА]  {name}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\nпройдено {passed}, провалено {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
