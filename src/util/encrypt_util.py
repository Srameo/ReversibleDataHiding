import numpy as np
import src.util.image_util as iu
import src.util.path_util as pu
from src.encryption_2d_lscm.InitialStateGeneration import init_confusion_matrix, init_states
from src.encryption_2d_lscm.diffusion import row_diffusion, column_diffusion
from src.encryption_2d_lscm.permutation import permutation

SECRET_KEY = {
    "x0": [1] * 13 + [0] * 13 + [1] * 13 + [0] * 13,
    "y0": [0] * 13 + [1] * 13 + [0] * 13 + [1] * 13,
    "r": [1] * 40 + [0] * 12,
    "a1": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    "a2": [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    "a3": [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
    "a4": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1]
}


def encrypt(P, S, F):
    """
    :param P: 加密的矩阵
    :param S: 密钥
    :param F: pixel
    :return: 加密后的图片矩阵
    """
    global T2
    M, N = P.shape
    init_matixs = init_confusion_matrix(M, N, init_states(S))
    for i in range(0, 4):
        T = permutation(P, init_matixs[i], M, N)
        T1 = row_diffusion(T, init_matixs[i], F, M, N)
        T2 = column_diffusion(T1, init_matixs[i], F, M, N)
    return T2


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_path = pu.path_join(root_path, pu.INPUT_PATH, '200px-Lenna.jpg')
    P = iu.read_img(file_path, iu.READ_GRAY)
    encrypted_img = encrypt(P, SECRET_KEY, 256).astype(np.uint8)
    iu.print_img(encrypted_img, "encrypted_lena")
