# 使用permutation.py文件中得到的矩阵T和混沌矩阵R进行扩散操作
import numpy as np
import permutation


def row_diffusion(T, R, F, M, N):
    """
    行扩散
    Args:
        T: 置换结果矩阵
        R: 混沌矩阵
        F: F is the number of allowed pixel values in plain-image P, e.g. F = 256 if P is 8-bit grayscale image
        M: 矩阵行数
        N: 矩阵列数
    Return:
        C: 行扩散结果
    """
    G = N
    C = np.zeros_like(T)
    for i in range(G):
        if i == 0:
            tmp = (T[:, 0] + T[:, G - 1] + T[:, G - 2] + np.floor(R[:, i] * (2 ** 32))) % F
        elif i == 1:
            tmp = (T[:, 1] + C[:, 0] + T[:, G - 1] + np.floor(R[:, i] * (2 ** 32))) % F
        else:
            tmp = (T[:, i] + C[:, i - 1] + C[:, i - 2] + np.floor(R[:, i] * (2 ** 32))) % F
        for m in range(M):
            C[m][i] = tmp[m]

    return C


def column_diffusion(T, R, F, M, N):
    '''
    列扩散
    Args:
        T: 置换结果矩阵
        R: 混沌矩阵
        F: F is the number of allowed pixel values in plain-image P, e.g. F = 256 if P is 8-bit grayscale image
        M: 矩阵行数
        N: 矩阵列数
    Return:
        C: 列扩散结果
    '''
    G = M
    C = np.zeros_like(T)
    for i in range(G):
        if i == 0:
            tmp = (T[0] + T[G - 1] + T[G - 2] + np.floor(R[i] * (2 ** 32))) % F
        elif i == 2:
            tmp = (T[1] + C[0] + T[G - 1] + np.floor(R[i] * (2 ** 32))) % F
        else:
            tmp = (T[i] + C[i - 1] + C[i - 2] + np.floor(R[i] * (2 ** 32))) % F
        for m in range(N):
            C[i][m] = tmp[m]

    return C


if __name__ == "__main__":
    T = permutation.permutation(S, P, M, N)
    R = permutation.S
    F = 30
    M = permutation.M
    N = permutation.N

    print(row_diffusion(T, R, F, M, N))
    print(column_diffusion(T, R, F, M, N))
