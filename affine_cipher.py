import random


def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    if greatest_common_divisor(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def affine_encrypt(text, a, b):
    eng_characters = "abcdefghijklmnopqrstuvwxyz"
    if text[0] in eng_characters:
        N = 27
        start_ch = ord('a')
    else:
        N = 33
        start_ch = ord('а')
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            x = ord(char) - start_ch
            y = (a * x + b) % N
            enc_char = chr(y + start_ch)
            result += enc_char.upper() if is_upper else enc_char
        else:
            result += char
    return result


def affine_decrypt(text, a, b):
    eng_characters = "abcdefghijklmnopqrstuvwxyz"
    if text[0] in eng_characters:
        N = 27
        start_ch = ord('a')
    else:
        N = 33
        start_ch = ord('а')

    a_inv = mod_inverse(a, N)
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            y = ord(char) - start_ch
            x = (a_inv * (y - b)) % N
            dec_char = chr(x + start_ch)
            result += dec_char.upper() if is_upper else dec_char
        else:
            result += char
    return result


def frequency_analysis(encrypted_text):
    frequency = {}
    total_chars = 0
    for char in encrypted_text:
        if char.isalpha():
            char = char.lower()
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
            total_chars += 1

    for char in frequency:
        frequency[char] = ((frequency[char] / total_chars) * 100)

    return frequency


source_text = "русский текст"

a, b = 5, 8

encrypted_text = affine_encrypt(source_text, a, b)
decrypted_text = affine_decrypt(encrypted_text, a, b)

print("Source Text: ", source_text)
print("Encrypted Text: ", encrypted_text)
print("Decrypted Text: ", decrypted_text)
print("Frequency Analysis:", frequency_analysis(encrypted_text))
