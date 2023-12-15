from Lab2.affine_block_cipher import Affine_block_cipher as afbc
from Lab2.ReaderWriter import ReaderWriter as RW, add_text_to_image


if __name__ == '__main__':
    block_size = 16
    round_count = 1
    # key = afbc.generate_key(block_size)
    # afbc.save_keys(key)
    key = afbc.load_keys()
    test = afbc(key, block_size, round_count=round_count)
    rw = RW(test)

    mode = "CBC"

    rw.encrypt_file("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny.bmp", "/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_enc.bmp", True, mode)
    rw.decrypt_file("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_enc.bmp","/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_dec.bmp", True, mode)
    #
    # add_text_to_image("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_enc.bmp",
    #                   "/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_enc_bad.bmp", "SUAI SUAI SUAI SUAI SUAI")
    rw.decrypt_file("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_enc_bad.bmp",
                    "/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/Funny/funny_bad_dec.bmp", True, mode)



    # rw.encrypt_file("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/test.txt", "/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/test_enc.txt", False, mode)
    # rw.decrypt_file("/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab2/test_enc.txt", "/Users/yyyyyliaa/PycharmProjects/Cryptography/Lab1/test_dec.txt", False, mode)
