import struct
from decimal import Decimal, getcontext
getcontext().prec = 50

def decompose(x):
    bits = struct.unpack('Q', struct.pack('d', x))[0]
    bits_str = f'{bits:064b}'
    sign_bin = bits_str[0]
    exp_bin = bits_str[1:12]
    mant_bin = bits_str[12:]
    sign_dec = int(sign_bin)
    exp_dec = int(exp_bin, 2)
    mant_dec = int(mant_bin, 2)
    real_exp = exp_dec - 1023
    frac = mant_dec / (1 << 52)
    full_mant = 1 + frac
    return (sign_bin, exp_bin, mant_bin,
            sign_dec, exp_dec, mant_dec,
            real_exp, frac, full_mant)

def restore(sign, exp, mant):
    s = int(sign)
    e = int(exp, 2)
    m = int(mant, 2)
    return (-1) ** s * (1 + m / (1 << 52)) * 2 ** (e - 1023)

# --- 1 + 1/(10^n) ---
print("=== 1 + 1/(10^n) ===")
print("Показываем ошибку: разница между точным и тем, что в памяти\n")
n = 0
while True:
    # Точное значение через Decimal (без потери точности)
    exact = Decimal(1) + Decimal(1) / (Decimal(10) ** n)
    # Значение в памяти (float)
    x = 1 + 1 / (10 ** n)
    # Ошибка = то что в памяти минус точное
    error = Decimal(str(x)) - exact

    sb, eb, mb, sd, ed, md, re, frac, full = decompose(x)
    r = restore(sb, eb, mb)

    print(f"n={n}")
    print(f"  точное (Decimal):  {exact}")
    print(f"  в памяти (float):  {x}")
    print(f"  ошибка:             {error}")
    print(f"  двоичное:  {sb}|{eb}|{mb}")
    print(f"  знак={sd}  экспонента={ed} (степень 2^{re})  мантисса(целое)={md}")
    print(f"  перевод: {md} / 2^52 = {frac}")
    print(f"  полная мантисса: 1 + {frac} = {full}")
    print(f"  формула: (-1)^{sd} × {full} × 2^{re} = {r}")
    print()

    if x == 1.0:
        print(f"СТОП при n={n} — добавка слишком мала, потерялась при округлении")
        break
    n += 1

# --- 1 + 1/(2^k) ---
print("\n=== 1 + 1/(2^k) ===")
print("Показываем ошибку: разница между точным и тем, что в памяти\n")
k = 0
while True:
    exact = Decimal(1) + Decimal(1) / (Decimal(2) ** k)
    x = 1 + 1 / (2 ** k)
    error = Decimal(str(x)) - exact

    sb, eb, mb, sd, ed, md, re, frac, full = decompose(x)
    r = restore(sb, eb, mb)

    print(f"k={k}")
    print(f"  точное (Decimal):  {exact}")
    print(f"  в памяти (float):  {x}")
    print(f"  ошибка:             {error}")
    print(f"  двоичное:  {sb}|{eb}|{mb}")
    print(f"  знак={sd}  экспонента={ed} (степень 2^{re})  мантисса(целое)={md}")
    print(f"  перевод: {md} / 2^52 = {frac}")
    print(f"  полная мантисса: 1 + {frac} = {full}")
    print(f"  формула: (-1)^{sd} × {full} × 2^{re} = {r}")
    print()

    if x == 1.0:
        print(f"СТОП при k={k} — добавка слишком мала, потерялась при округлении")
        break
    k += 1
