import math
import numpy

secretKey = {
    "x0": [1] * 13 + [0] * 13 + [1] * 13 + [0] * 13,
    "y0": [0] * 13 + [1] * 13 + [0] * 13 + [1] * 13,
    "r": [1] * 40 + [0] * 12,
    "a1": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    "a2": [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
    "a3": [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1],
    "a4": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1]
}


def _2D_LSCM(x, y, r):
    next_x = math.sin(math.pi * (4 * r * (x) * (1 - x) + (1 - r) * math.sin(math.pi * y)))
    next_y = math.sin(math.pi * (4 * r * (y) * (1 - y) + (1 - r) * math.sin(math.pi * x)))
    return next_x, next_y


def v(l):
    """
    使用IEEE754浮点标准转换为浮点数
    Args:
        l: 存储二进制的列表
    Return:
        reslut: 返回十进制浮点数
    """
    result = 0
    for i in range(len(l)):
        result += l[i] * (2 ** (-(i + 1)))

    return result


def transformToDecimal(l):
    """
    将二进制串正常转换为十进制
    Args:
        l: 存储二进制的列表
    Return:
        result: 返回十进制整数
    """
    result = 0
    n = len(l) - 1
    for i in range(len(l)):
        result += l[i] * (2 ** (n - i))

    return result


def init_states(k):
    """
    生成4个初始状态
    Args:
        k: 密钥 {x0, y0, r, a1, a2, a3, a4}
    Returns:
        initialStates: 生成的四个初始状态
    """
    initialStates = [None] * 4
    r = [0] * 4

    r[0] = (v(k['r']) * transformToDecimal(k['a1'])) % 1
    r[1] = (v(k['r']) * transformToDecimal(k['a2'])) % 1
    r[2] = (v(k['r']) * transformToDecimal(k['a3'])) % 1
    r[3] = (v(k['r']) * transformToDecimal(k['a4'])) % 1

    initialStates[0] = (v(k['x0']), v(k['y0']), r[0])

    for i in range(1, 4):
        next_x, next_y = _2D_LSCM(*initialStates[i - 1])
        initialStates[i] = (next_x, next_y, r[i])

    return initialStates


def init_confusion_matrix(M, N, initialStates):
    init_matixs = [None] * 4
    for i in range(0, 4):
        init_matixs[i] = numpy.zeros((M, N))
    for k in range(0, 4):
        for i in range(0, M):
            for j in range(0, N):
                temp_x, temp_y = _2D_LSCM(*initialStates[k])
                init_matixs[k][i][j] = (temp_x + temp_y) / 2
                initialStates[k] = (temp_x, temp_y, initialStates[k][2])
    return init_matixs


if __name__ == "__main__":
    print(init_states(secretKey))
    print(init_confusion_matrix(20, 30, init_states(secretKey)))
