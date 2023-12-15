import struct
from PIL import Image, ImageDraw, ImageFont
from bitarray import bitarray


class ReaderWriter:
    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt_one(self, data):
        return self.cipher.encrypt_one(data)

    def encrypt_two(self, data):
        return self.cipher.encrypt_two(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)

    def encrypt_file(self, filename, output_filename, bmp=False, mode='ECB'):

        with open(filename, 'rb') as f:
            if bmp:
                f.seek(10)
                offset = struct.unpack('I', f.read(4))[0]
                f.seek(0)
                bmp_header = f.read(offset)
            data = f.read()

        # encrypted_data = self.encrypt(data)
        if mode == 'ECB':
            encrypted_data = self.cipher.encrypt_ecb(data)
        elif mode == 'CBC':
            encrypted_data = self.cipher.encrypt_cbc(data, b'\x00' * self.cipher.block_size)
        else:
            raise ValueError('Unknown mode')

        with open(output_filename, 'wb') as f:
            with open("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab3/source.txt", 'w') as fl:
                if bmp:
                    f.write(bmp_header)
                bits = bitarray()
                bits.frombytes(encrypted_data)
                fl.write(bits.to01())
                f.write(encrypted_data)

    def decrypt_file(self, filename, output_filename, bmp=False, mode='ECB'):

        with open(filename, 'rb') as f:

            if bmp:
                f.seek(10)
                offset = struct.unpack('I', f.read(4))[0]
                f.seek(0)
                bmp_header = f.read(offset)

            data = f.read()

        if mode == 'ECB':
            decrypted_data = self.cipher.decrypt_ecb(data)
        elif mode == 'CBC':
            decrypted_data = self.cipher.decrypt_cbc(data, b'\x00' * self.cipher.block_size)
        else:
            raise ValueError('Unknown mode')

        with open(output_filename, 'wb') as f:
            with open("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab3/inv.txt", 'w') as fl:
                if bmp:
                    f.write(bmp_header)
                bits = bitarray()
                bits.frombytes(decrypted_data)
                fl.write(bits.to01())
                f.write(decrypted_data)
