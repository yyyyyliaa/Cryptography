import struct
from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(input_image_path, output_image_path, text_to_add):
    # copy file to new file
    # with open(input_image_path, 'rb') as f:
    #     with open(output_image_path, 'wb') as f2:
    #         f2.write(f.read())
    try:
        # Открытие изображения
        image = Image.open(input_image_path)

        # Создание объекта для рисования
        draw = ImageDraw.Draw(image)

        # Загрузка шрифта
        font = ImageFont.load_default()

        # Масштабирование шрифта до нужного размера

        # Определение позиции текста
        text_position = (20, 20)  # Позиция, в которой будет нарисован текст

        # Нанесение текста на изображение
        draw.text(text_position, text_to_add, fill="black", font=font)

        # Сохранение измененного изображения
        image.save(output_image_path)
        print(f"Текст успешно добавлен в {output_image_path}")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


class ReaderWriter:
    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt(self, data):
        return self.cipher.encrypt(data)

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
            if bmp:
                f.write(bmp_header)
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

            if bmp:
                f.write(bmp_header)

            f.write(decrypted_data)
