# 普通图像P：M * N
# 混乱矩阵S：M * N

import numpy as np

M = 4
N = 5

S = np.array([[0.96, 0.50, 0.08, 0.75, 0.97],
              [0.44, 0.05, 0.84, 0.72, 0.33],
              [0.06, 0.68, 0.99, 0.58, 0.38],
              [0.70, 0.45, 0.07, 0.12, 0.18]])

P = np.array([[1, 5, 9, 13, 17],
              [2, 6, 10, 14, 18],
              [3, 7, 11, 15, 19],
              [4, 8, 12, 16, 20]])




def permutation():
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
            T[int(PM[i][m][0])][int(PM[i][m][1])] = tmpP[tmpS[m][1]]

    return T


if __name__ == "__main__":
    t = permutation()
