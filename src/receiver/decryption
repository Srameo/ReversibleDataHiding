import numpy
import math

from src.encryption_2d_lscm.InitialStateGeneration import init_confusion_matix, init_states

# 测试数据
'''
行数，
列数，
密钥,
F

'''
M = 4
N = 5
F = 256
res = numpy.array([[7, 5, 2, 17, 11],
                   [9, 3, 4, 14, 15],
                   [6, 13, 1, 8, 10],
                   [19, 18, 12, 16, 20]])
S = numpy.array([[0.96, 0.50, 0.08, 0.75, 0.97],
                 [0.44, 0.05, 0.84, 0.72, 0.33],
                 [0.06, 0.68, 0.99, 0.58, 0.38],
                 [0.70, 0.45, 0.07, 0.12, 0.18]])
secretKey = {
    "x0": [1] * 13 + [0] * 13 + [1] * 13 + [0] * 13,
    "y0": [0] * 13 + [1] * 13 + [0] * 13 + [1] * 13,
    "r": [1] * 40 + [0] * 12,
    "a1": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    "a2": [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    "a3": [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
    "a4": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1]
}


def get_LM(res, M, N):
    pass


def reverse_row_diffusion(C, init_matix, F, M, N):
    """
        反向扩散
        :param C: 为加密后矩阵
        :param init_matix: 混乱矩阵
        :param F: 图片pixel值
        :param M: 矩阵行数
        :param N: 矩阵列数
        :return: 列扩散结果
        """
    G = N
    res = numpy.zeros_like(C)
    for i in range(G):
        if i >= 2:
            tmp = (C[:, i] - C[:, i - 1] - C[:, i - 2] + numpy.floor(init_matix[:, i] * (2 ** 32))) % F
        elif i == 1:
            tmp = (C[:, 1] - C[:, 0] - res[:, G - 1] + numpy.floor(init_matix[:, i] * (2 ** 32))) % F
        else:
            tmp = (C[:, 0] + res[:, G - 1] + res[:, G - 2] + numpy.floor(init_matix[:, i] * (2 ** 32))) % F

        for m in range(M):
            res[m][i] = tmp[m]

    return res


def reverse_col_diffusion(C, init_matix, F, M, N):
    """
        反向扩散
        :param res: 为加密后矩阵
        :param init_matix: 混乱矩阵
        :param F: 图片pixel值
        :param M: 矩阵行数
        :param N: 矩阵列数
        :return: 列扩散结果
        """
    G = M
    res = numpy.zeros_like(C)
    for i in range(G):
        if i >= 2:
            tmp = (C[i] - C[i - 1] - C[- 2] + numpy.floor(init_matix[i] * (2 ** 32))) % F
        elif i == 1:
            tmp = (C[1] - C[0] - res[G - 1] + numpy.floor(init_matix[i] * (2 ** 32))) % F
        else:
            tmp = (C[0] + res[G - 1] + res[G - 2] + numpy.floor(init_matix[i] * (2 ** 32))) % F

        for m in range(N):
            res[i][m] = tmp[m]

    return res


def reverse_diffusion(res, init_matix, F, M, N):
    """
    反向扩散
    :param res: 为加密后矩阵
    :param init_matix: 混乱矩阵
    :param F: 图片pixel值
    :param M: 矩阵行数
    :param N: 矩阵列数
    :return: 列扩散结果
    """
    C = reverse_col_diffusion(res, init_matix, F, M, N)
    C = reverse_row_diffusion(C, init_matix, F, M, N)
    return C


def reverse_permutation(T, init_matix, M, N):
    """
    反向乱序
    :param T: 反向扩散后的矩阵
    :param init_matix: 混乱矩阵
    :return: 源矩阵
    """
    # 对S的每一列进行排序并获得反向索引矩阵O
    O = numpy.zeros((M, N))
    for j in range(N):
        tmp = []
        for i in range(M):
            tmp.append((init_matix[i][j], i))
        columnO = sorted(tmp, key=lambda x: x[0])
        for i in range(M):
            O[i][j] = columnO[i][1]

    # 设置列索引得到PM
    PM = []
    for i in range(M):
        PM.append([])
        for j in range(N):
            PM[-1].append((O[i][j], j))
    res = numpy.zeros((M, N))
    # 得到目标矩阵T
    for i in range(M):
        tmpS = []
        tmpP = []
        for j in range(N):
            tmpS.append((init_matix[int(PM[i][j][0])][int(PM[i][j][1])], j))
            tmpP.append(T[int(PM[i][j][0])][int(PM[i][j][1])])
        tmpS = sorted(tmpS, key=lambda x: x[0])
        tempS = []
        for k in range(N):
            for l in range(N):
                if tmpS[l][1] == k:
                    tempS.append(l)
        for m in range(N):
            res[int(PM[i][m][0])][int(PM[i][m][1])] = tmpP[tempS[m]]
    return res


if __name__ == "__main__":
    init_matixs = [None] * 4
    init_matixs = init_confusion_matix(M, N, init_states(secretKey))
    # 取出LM
    get_LM(res, M, N)
    for i in range(0, 4):
        # 反向扩散
        res = reverse_diffusion(res, init_matixs[i], F, M, N)
        res = reverse_permutation(res,init_matixs[i],M, N)
