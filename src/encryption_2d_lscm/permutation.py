# 普通图像P：M * N
# 混乱矩阵S：M * N

import numpy as np


def permutation(P, S, M, N):
    # 对S的每一列进行排序并获得索引矩阵O
    O = np.zeros((M, N))
    for j in range(N):
        tmp = []
        for i in range(M):
            tmp.append((S[i][j], i))
        columnO = sorted(tmp, key=lambda x: x[0])
        for i in range(M):
            O[i][j] = columnO[i][1]

    # 设置列索引得到PM
    PM = []
    for i in range(M):
        PM.append([])
        for j in range(N):
            PM[-1].append((O[i][j], j))

    # 得到目标矩阵T
    T = np.zeros((M, N))
    for i in range(M):
        tmpS = []
        tmpP = []
        for j in range(N):
            tmpS.append((S[int(PM[i][j][0])][int(PM[i][j][1])], j))
            tmpP.append(P[int(PM[i][j][0])][int(PM[i][j][1])])
        tmpS = sorted(tmpS, key=lambda x: x[0])
        for m in range(N):
            T[int(PM[i][m][0])][int(PM[i][m][1])] = int(tmpP[tmpS[m][1]])
    return T

