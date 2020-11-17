import numpy as np
import src.util.image_util as iu
import src.util.path_util as pu
import math


class Encryptor:

    def __init__(self, img: np.ndarray = None):
        self.Is = [None] * 4
        self.Ps = [None] * 4
        self.PEs = [None] * 4
        self.PEAs = [None] * 4
        self.src_img = img
        if img is not None:
            self.H, self.W = img.shape

    def decomposition(self):
        h, w = int(self.H / 2), int(self.W / 2)
        for i in range(4):
            self.Is[i] = np.zeros((h, w), np.int)
        for i in range(h):
            for j in range(w):
                self.Is[0][i, j] = self.src_img[2 * i - 1, 2 * j - 1]
                self.Is[1][i, j] = self.src_img[2 * i - 1, 2 * j]
                self.Is[2][i, j] = self.src_img[2 * i, 2 * j - 1]
                self.Is[3][i, j] = self.src_img[2 * i, 2 * j]

    def predict(self):
        # 计算P
        self.Ps[0] = self.Is[0]
        self.__predict01()
        self.__predict02()
        self.__predict03()
        # 计算 PE
        for i in range(1, 4):
            self.PEs[i] = self.Ps[i] - self.Is[i]
        self.PEs[0] = np.copy(self.Is[0])
        # 计算PEA, 同时嵌入location map
        for i in range(4):
            self.PEAs[i] = np.copy(self.PEs[i])
            self.PEAs[i][self.PEAs[i] < 0] = abs(self.PEAs[i][self.PEAs[i] < 0]) + 64
            self.PEAs[i][self.PEAs[i] > 64] = self.PEAs[i][self.PEAs[i] > 64] | 0b10000000

    def __predict01(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[1] = np.zeros((h, w), np.int)
        for i in range(h):
            for j in range(w):
                if i == h:
                    self.Ps[1][i, j] = math.ceil((I0[i, j] + I0[i, j + 1])/2)
                else:
                    self.Ps[1][i, j] = I0[i, j]

    def __predict02(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[2] = np.zeros((h, w), np.int)
        for i in range(h):
            for j in range(w):
                if j == w:
                    self.Ps[2][i, j] = math.ceil((I0[i, j] + I0[i + 1, j]) / 2)
                else:
                    self.Ps[2][i, j] = I0[i, j]

    def __predict03(self):
        I0 = self.Is[0]

        def H1(i, j):
            return abs(int(I0[i, j]) - int(I0[i + 1, j + 1]))

        def H2(i, j):
            return abs(int(I0[i, j + 1]) - int(I0[i + 1, j]))

        h, w = I0.shape
        self.Ps[3] = np.zeros((h, w), np.int)

        for i in range(h - 1):
            for j in range(w - 1):
                if H1(i, j) < H2(i, j):
                    self.Ps[3][i, j] = math.ceil((I0[i, j] + I0[i + 1, j + 1]) / 2)
                else:
                    self.Ps[3][i, j] = math.ceil((I0[i, j + 1] + I0[i + 1, j]) / 2)

        for i in range(h - 1):
            self.Ps[3][i, w - 1] = math.ceil((I0[i, w - 1] + I0[i + 1, w - 1]) / 2)

        for j in range(w - 1):
            self.Ps[3][h - 1, j] = math.ceil((I0[h - 1, j] + I0[h - 1, j + 1]) / 2)

        self.Ps[3][h - 1, w - 1] = I0[h - 1, w - 1]

    def get_gull_img(self, imgs: str = "I"):
        res = np.zeros((self.H, self.W), np.int)
        h, w = int(self.H / 2), int(self.W / 2)
        if imgs == "PEA":
            arr = self.PEAs
        elif imgs == "PE":
            arr = self.PEs
        else:
            arr = self.Is
        res[0:h, 0:w] = arr[0]
        res[0:h, w:self.W] = arr[1]
        res[h:self.H, 0:w] = arr[2]
        res[h:self.H, w:self.W] = arr[2]
        return res.astype(np.uint8)


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_name = "200px-Lenna.jpg"
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    gray_lena = iu.read_img(file_path, iu.READ_GRAY)

    e = Encryptor(gray_lena)
    e.decomposition()
    e.predict()

    iu.print_img(e.get_gull_img("I"))
    iu.print_img(e.get_gull_img("PE"))
    iu.print_img(e.get_gull_img("PEA"))