import src.util.image_util as iu
import src.util.path_util as pu
import math
import numpy as np


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
        if prob == 0:
            continue
        shannon_ent -= prob * math.log(prob, 2)
        chi_ent += (prob - 1 / 256) ** 2
    chi_ent = chi_ent * 256 * scale
    return shannon_ent, chi_ent


def npcr_uaci_analysis(x, y):
    [rows, cols] = x.shape
    scale = rows * cols
    npcr = 0.0
    uaci = 0.0
    for i in range(rows):
        for j in range(cols):
            d = x[i, j] - y[i, j]
            if d == 0:
                d = 1
            else:
                d = 0
            npcr += d
            uaci += abs(x[i, j] - y[i, j])
    npcr /= scale
    uaci /= (255 * scale)
    return 1 - npcr, uaci


def analysis3D(img1, img2):
    b1 = img1[:, :, 0]
    g1 = img1[:, :, 1]
    r1 = img1[:, :, 2]
    b2 = img2[:, :, 0]
    g2 = img2[:, :, 1]
    r2 = img2[:, :, 2]
    r = np.array([0, 0, 0, 0, 0])
    g = np.array([0, 0, 0, 0, 0])
    b = np.array([0, 0, 0, 0, 0])
    r[0], r[1] = npcr_uaci_analysis(r1, r2)
    g[0], g[1] = npcr_uaci_analysis(g1, g2)
    b[0], b[1] = npcr_uaci_analysis(b1, b2)
    r[2] = ent_analysis(r2)
    g[2] = ent_analysis(g2)
    b[2] = ent_analysis(b2)
    r[3], r[4] = cor_analysis(r1, r2)
    g[3], g[4] = cor_analysis(g1, g2)
    b[3], b[4] = cor_analysis(b1, b2)
    return np.mean(r + g + b)


if __name__ == "__main__":
    root_path = pu.get_root_path()
    img1 = iu.read_img(pu.path_join(root_path, "static/test/unchanged/image.png"), iu.READ_GRAY)
    img2 = iu.read_img(pu.path_join(root_path, "static/test/changed/image.png"), iu.READ_GRAY)

    print(npcr_uaci_analysis(img1, img2))
    print(ent_analysis(img2))
    print(cor_analysis(img1, img2))
