import numpy as np
import math


def cor_analysis(x, y):
    [rows, cols] = x.shape
    scale = rows * cols
    sum_x = 0
    sum_y = 0
    for i in range(rows):
        for j in range(cols):
            sum_x += x[i, j]
            sum_y += y[i, j]
    aver_x = sum_x / scale
    aver_y = sum_y / scale
    var_x = 0
    var_y = 0
    cov = 0
    for i in range(rows):
        for j in range(cols):
            var_x += (i - aver_x) ** 2
            var_y += (i - aver_y) ** 2
            cov += (i - aver_x) * (i - aver_y)
    var_x /= scale
    var_y /= scale
    cov /= scale
    coc = cov / math.sqrt(var_x * var_y)
    return coc


def ent_analysis(x):
    [rows, cols] = x.shape
    scale = rows * cols
    labels = {}
    for i in range(rows):
        for j in range(cols):
            current = x[i, j]
            if current not in labels.keys():
                labels[current] = 0
        labels[current] += 1
    shannon_ent = 0.0  # 香农熵
    chi_ent = 0.0  # χ2
    for key in labels:
        prob = float(labels[key]) / scale  # 选择该标签的概率
        shannon_ent -= prob * log(prob, 2)
        chi_ent += (prob - 1 / 256) ** 2
    chi_ent = chi_ent * 256 * scale
    return shannon_ent, chi_ent


def npcr_uaci_analysis(x,y):
    [rows, cols] = x.shape
    scale = rows * cols
    npcr=0.0
    uaci=0.0
    for i in range(rows):
        for j in range(cols):
            d=x[i,j]-y[i,j]
            if d==0:
                d=1
            else:
                d=0
            npcr+=d
            uaci+=abs(x[i,j]-y[i,j])
    npcr/=scale
    uaci/=255*scale
    return npcr,uaci

