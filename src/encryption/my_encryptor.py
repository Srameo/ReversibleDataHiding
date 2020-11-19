import math

import numpy as np
from src.encryption.encryptor import Encryptor
import src.util.image_util as iu
import src.util.path_util as pu


class MyEncryptor(Encryptor):

    def __init__(self, img: np.ndarray = None, predict=None):
        super().__init__(None, None)
        self.Is = [None] * 6
        self.Ps = [None] * 6
        self.PEs = [None] * 6
        self.PEAs = [None] * 6
        self.src_img = img
        if predict is None:
            self.predict_method = Encryptor.predict_method1
        else:
            self.predict_method = predict
        if img is not None:
            self.H, self.W = img.shape
            # need to fix
            self.H = self.H - self.H % 3

    def decomposition(self):
        h, w = int(self.H / 3), int(self.W / 2)
        i, j = 0, 0
        while i < 6:
            self.Is[i] = np.zeros((h, w), np.int)
            i += 1
        i = 0
        while i < self.H:
            while j < self.W:
                row = i % 3
                column = j % 2
                self.Is[row * 2 + column][int(i / 3)][int(j / 2)] = self.src_img[i][j]
                j += 1
            j = 0
            i += 1

    def predict(self):
        self.Ps[0] = np.copy(self.Is[0])
        self.__predict01()
        self.__predict02()
        self.__predict03()
        self.__predict04()
        self.__predict05()
        # 计算 PE
        for i in range(6):
            self.PEs[i] = self.Ps[i] - self.Is[i]

    def __predict01(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[1] = np.zeros((h, w), np.int)
        i, j = 0, 0
        while i < h:
            while j < w:
                if j == w - 1:
                    self.Ps[1][i, j] = I0[i, j]
                else:
                    self.Ps[1][i, j] = self.predict_method(I0[i, j], I0[i, j + 1])
                j += 1
            i, j = i + 1, 0

    def __predict02(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[2] = np.zeros((h, w), np.int)
        i, j = 0, 0
        while i < h:
            while j < w:
                if i == h - 1:
                    self.Ps[2][i, j] = I0[i, j]
                else:
                    self.Ps[2][i, j] = math.ceil(I0[i, j] * 2 / 3 + I0[i + 1, j] / 3)
                j += 1
            i, j = i + 1, 0

    def __predict03(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[3] = np.zeros((h, w), np.int)
        i, j = 0, 0
        while i < h - 1:
            while j < w - 1:
                self.Ps[3][i, j] = math.ceil(I0[i + 1, j] / 3 + I0[i, j] / 6 + I0[i, j + 1] / 2)
                j += 1
            i, j = i + 1, 0

    def __predict04(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[4] = np.zeros((h, w), np.int)
        i, j = 0, 0
        while i < h:
            while j < w:
                if i == h - 1:
                    self.Ps[4][i, j] = I0[i, j]
                else:
                    self.Ps[4][i, j] = math.ceil(I0[i, j] / 3 + I0[i + 1, j] * 2 / 3)
                j += 1
            i, j = i + 1, 0

    def __predict05(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[5] = np.zeros((h, w), np.int)
        i, j = 0, 0
        while i < h - 1:
            while j < w - 1:
                self.Ps[5][i, j] = math.ceil(I0[i + 1, j] / 6 + I0[i, j] / 3 + I0[i + 1, j + 1] / 2)
                j += 1
            i, j = i + 1, 0

    @staticmethod
    def get_uint8_img(*lst: np.ndarray):
        return (i.astype(np.uint8) for i in lst)


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_name = "200px-Lenna.jpg"
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    gray_lena = iu.read_img(file_path, iu.READ_GRAY)

    me = MyEncryptor(gray_lena, Encryptor.predict_method1)
    me.decomposition()
    me.predict()

    print(me.error())

    # iu.print_imgs(*me.get_uint8_img(*me.Ps))
