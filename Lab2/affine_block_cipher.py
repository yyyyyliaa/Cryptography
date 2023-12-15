import random


class Affine_block_cipher:
    def __init__(self, keys, block_size=16, difference=4, round_count=16):
        self.keys = keys.copy()
        self.difference = difference
        self.round_count = round_count
        self.block_size = block_size

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def mod_inverse(self, a, m):
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def decrypt_block(self, block_origin):
        block = bytearray(block_origin)
        for i in range(self.round_count):
            for j, byte_element in enumerate(block):
                key = self.keys[j % len(self.keys)]
                a = key[1]
                b = key[2]
                a_inv = self.mod_inverse(a, 256)
                y = key[0].find(byte_element)
                x = (a_inv * (y - b)) % 256
                block[j] = key[0][x]
        return block

    def decrypt_ecb(self, data):
        decrypted_data = bytearray()

        for i in range(0, len(data) - self.block_size, self.block_size):
            block = data[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block)
            decrypted_data.extend(decrypted_block)

        padding_size = int.from_bytes(data[-self.block_size:], byteorder='big')
        last_block = data[-self.block_size * 2:-self.block_size]
        print(len(last_block))
        decrypted_block = self.decrypt_block(last_block)
        print(len(decrypted_block))
        tmp = decrypted_block[:-padding_size]
        print(len(tmp))
        if padding_size != 0:
            decrypted_data.extend(decrypted_block[:-(padding_size)])
        return decrypted_data


    def encrypt_block(self, block_origin):
        block = bytearray(block_origin)
        for i in range(self.round_count):
            for j, byte_element in enumerate(block):
                key = self.keys[j % len(self.keys)]
                x = key[0].find(byte_element)
                a = key[1]
                b = key[2]
                y = (a * x + b) % 256
                block[j] = key[0][y]
        return block

    def encrypt_ecb(self, data):
        encrypted_data = bytearray()
        padding_size = 0
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            if len(block) < self.block_size:
                print(len(block))
                padding_size = self.block_size - len(block)
                block = block + b'\x00' * padding_size
                print(len(block))
            encrypted_block = self.encrypt_block(block)
            encrypted_data.extend(encrypted_block)

        encrypted_data.extend(padding_size.to_bytes(self.block_size, byteorder='big'))
        return encrypted_data



    def encrypt_cbc(self, data, iv):
        encrypted_data = bytearray()
        padding_size = 0
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            if len(block) < self.block_size:
                padding_size = self.block_size - len(block)
                block = block + b'\x00' * padding_size
            block = bytes([a ^ b for a, b in zip(block, iv)])
            encrypted_block = self.encrypt_block(block)
            encrypted_data.extend(encrypted_block)
            iv = encrypted_block
        encrypted_data.extend(padding_size.to_bytes(self.block_size, byteorder='big'))

        return encrypted_data

    def decrypt_cbc(self, data, iv):
        decrypted_data = bytearray()
        for i in range(0, len(data) - self.block_size, self.block_size):
            block = data[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block)
            decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, iv)])
            decrypted_data.extend(decrypted_block)
            iv = block

        padding_size = int.from_bytes(data[-self.block_size:], byteorder='big')
        last_block = data[-self.block_size * 2:-self.block_size]
        decrypted_block = self.decrypt_block(last_block)
        decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, iv)])
        if padding_size != 0:
            decrypted_data.extend(decrypted_block[:-(padding_size-1)])
        return decrypted_data


    @staticmethod
    def generate_affine_keys(alphabet_size):
        a = random.choice([n for n in range(2, alphabet_size) if all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))])
        b = random.randint(1, alphabet_size - 1)
        return a, b

    @staticmethod
    def generate_key(keys_count=16, alphabet_size=256):
        all_bytes = bytearray(range(alphabet_size))
        mixed_universal_keys = [
            (bytes(random.sample(all_bytes, len(all_bytes))),
             *Affine_block_cipher.generate_affine_keys(alphabet_size)) for _ in range(keys_count)
        ]
        return mixed_universal_keys

    @staticmethod
    def save_keys(keys, filename='keys.txt'):
        with open(filename, 'wb') as f:
            f.write(len(keys).to_bytes(1, byteorder='big'))
            for key in keys:
                f.write(key[0])
                f.write(key[1].to_bytes(1, byteorder='big'))
                f.write(key[2].to_bytes(1, byteorder='big'))

    @staticmethod
    def load_keys(filename='keys.txt'):
        keys = []
        with open(filename, 'rb') as f:
            disk_count = int.from_bytes(f.read(1), byteorder='big')
            for _ in range(disk_count):
                keys_data = f.read(256)
                a = int.from_bytes(f.read(1), byteorder='big')
                b = int.from_bytes(f.read(1), byteorder='big')
                keys.append((keys_data, a, b))

        return keys
