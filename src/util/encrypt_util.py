"""
加密解密的工具函数
"""

import numpy as np
import src.util.image_util as iu
import src.util.path_util as pu
from src.util.for_encrypt.encryption_2d_lscm.InitialStateGeneration import init_confusion_matrix, init_states
from src.util.for_encrypt.encryption_2d_lscm.diffusion import row_diffusion, column_diffusion
from src.util.for_encrypt.encryption_2d_lscm.permutation import permutation
import src.util.for_encrypt.decryption as dec

SECRET_KEY = {
    "x0": [1] * 13 + [0] * 13 + [1] * 13 + [0] * 13,
    "y0": [0] * 13 + [1] * 13 + [0] * 13 + [1] * 13,
    "r": [1] * 40 + [0] * 12,
    "a1": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    "a2": [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    "a3": [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
    "a4": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1]
}


def encrypt(P, S, F=256):
    """
    :param P: 加密的矩阵
    :param S: 密钥
    :param F: pixel
    :return: 加密后的图片矩阵
    """
    M, N = P.shape
    init_matixs = init_confusion_matrix(M, N, init_states(S))
    for i in range(0, 4):
        P = permutation(P, init_matixs[i], M, N)
        P = row_diffusion(P, init_matixs[i], F, M, N)
        P = column_diffusion(P, init_matixs[i], F, M, N)
    return P


def decrypt(P, S, F=256):
    """

    Args:
        P: 要解密的矩阵
        S: 密钥
        F: pixel值

    Returns: 解密后的数据

    """
    return dec.decryptioner(P, S, F)


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_path = pu.path_join(root_path, pu.INPUT_PATH, '200px-Lenna.jpg')
    P = iu.read_img(file_path, iu.READ_GRAY)
    encrypted_img = encrypt(P, SECRET_KEY, 256).astype(np.uint8)
    iu.print_img(encrypted_img, "encrypted_lena")
    anti_encrypted_img = dec.decryptioner(encrypted_img, SECRET_KEY, 256).astype(np.uint8)
    iu.print_img(anti_encrypted_img, "anti-encrypted_lena")
