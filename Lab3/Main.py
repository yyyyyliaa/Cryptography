import random

from Lab3.affine_block_cipher import Affine_block_cipher as afbc
from Lab3.ReaderWriter import ReaderWriter as RW

def series_test(data):
    print("Последовательностей разрывов")
    bits = int.from_bytes(data, byteorder='big')
    # print(bits)
    entry_nul = ""
    nul = ""
    one = ""

    for k in range(63, -1, -1):
        nul += "0"
        one += "1"
        entry_nul += "1" if bits & (1 << k) else "0"

    entry_one = entry_nul
    X = 0

    for i in range(63, -1, -1):
        count = entry_nul.count(nul)
        entry_nul = entry_nul.replace(nul, "")
        nul = nul[:-1]

        if count != 0:
            print(f"длиной {i + 1} = {count}")
            e = (64 - i + 4) / (2 ** (i + 3))
            X += (count - e) ** 2 / e

    print("Последовательностей блоков")
    for i in range(63, -1, -1):
        count = entry_one.count(one)
        entry_one = entry_one.replace(one, "")
        one = one[:-1]

        if count != 0:
            print(f"длиной {i + 1} = {count}")
            e = (64 - i + 4) / (2 ** (i + 4))
            X += (count - e) ** 2 / e

    print(f"Статистика Х = {X}")


def frequency_test(data):
    test = data
    sum0 = 0
    sum1 = 0
    bites = int.from_bytes(test, byteorder='big')

    for k in range(63, -1, -1):
        if bites & (1 << k):
            sum1 += 1
        else:
            sum0 += 1

    res0 = sum0 / 64
    res1 = sum1 / 64
    print(f"Частотный тест 0: {res0}\nЧастотный тест 1: {res1}")


def auto_corr_test(data, file_name):
    print("Автокорреляционный тест")
    bits = int.from_bytes(data, byteorder='big')
    entry_bytes = [1 if bits & (1 << k) else -1 for k in range(127, -1, -1)]

    D_list = []
    X_list = []
    for D in range(1, 64):
        A = 0
        for i in range(128 - D):
            A += entry_bytes[i] * entry_bytes[i + D]

        X = A / (128 - D)
        print(f"для D = {D}: {X}")
        D_list.append(D)
        X_list.append(X)

    import altair as alt
    import pandas as pd

    source = pd.DataFrame({
        'x': D_list,
        'y': X_list
    })

    temp = alt.Chart(source).mark_bar().encode(
        x='x',
        y='y'
    )

    temp.save(file_name)


if __name__ == '__main__':
    block_size = 8
    round_count = 8
    # key = afbc.generate_key(block_size)
    # afbc.save_keys(key)
    key = afbc.load_keys()
    test = afbc(key, block_size, round_count=round_count)
    rw = RW(test)

    data = bytearray()
    for i in range(block_size):
        data.append(random.randint(0, 255))


    print("Инвертируем четные биты")
    res = rw.encrypt_one(data)
    series_test(res)
    frequency_test(res)
    print()
    auto_corr_test(res, 'test1.html')

    print()
    print("------------------------------------------------------------------------------------")
    print()

    print("Инвертируем каждый восьмой бит")
    res = rw.encrypt_two(data)
    series_test(res)
    frequency_test(res)
    print()
    auto_corr_test(res, 'test2.html')
