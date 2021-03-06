import numpy as np
import src.util.image_util as iu
import src.util.path_util as pu
import math
import src.util.encrypt_util as eu

__TEST_IMAGE = np.array([[97, 97, 114, 162, 189, 180, 187, 192],
                         [87, 119, 123, 156, 174, 182, 184, 189],
                         [76, 117, 135, 162, 169, 173, 178, 191],
                         [54, 96, 116, 161, 161, 159, 171, 179],
                         [59, 81, 96, 142, 146, 152, 160, 169],
                         [70, 68, 76, 97, 125, 143, 132, 142],
                         [91, 54, 69, 65, 99, 135, 112, 118],
                         [128, 55, 64, 68, 72, 123, 135, 109]])


class Encryptor:

    def __init__(self, img: np.ndarray = None, predict=None):
        self.Is = []
        self.Ps = [None] * 4
        self.PEs = []
        self.PE_stars = []
        self.PEAs = []
        self.raw_LM = []
        # self.raw_LM = np.zeros(img.shape, np.bool)
        self.src_img = img
        if predict is None:
            self.predict_method = Encryptor.predict_method1
        else:
            self.predict_method = predict
        if img is not None:
            self.H, self.W = img.shape

    def decomposition(self):
        """
        将图片分解成4个部分
        :return:
        """
        h, w = int(self.H / 2), int(self.W / 2)
        for i in range(4):
            self.Is.append(np.zeros((h, w), np.int))
        for i in range(h):
            for j in range(w):
                self.Is[0][i, j] = self.src_img[2 * i, 2 * j]
                self.Is[1][i, j] = self.src_img[2 * i, 2 * j + 1]
                self.Is[2][i, j] = self.src_img[2 * i + 1, 2 * j]
                self.Is[3][i, j] = self.src_img[2 * i + 1, 2 * j + 1]

    def error(self):
        """
        返回当前的误差
        :return: 误差 min best
        """
        err = 0
        for i in self.PEs:
            err += np.sum(i ** 2)
        l = len(self.PEs)
        return err * l / (self.H * self.W * (l - 1))

    def predict(self):
        """
        预测并嵌入location map
        :return:
        """
        # 计算P
        self.Ps[0] = self.Is[0]
        self.__predict01()
        self.__predict02()
        self.__predict03()
        # 计算 PE
        for i in range(4):
            # self.PEs[i] = self.Ps[i] - self.Is[i]
            self.PEs.append(self.Is[i] - self.Ps[i])
        self.PE_stars.append(np.copy(self.Is[0]))
        self.PEAs.append(np.copy(self.PE_stars[0]))
        self.raw_LM.append(np.zeros(self.PEAs[0].shape, np.bool))
        for i in range(1, 4):
            self.PE_stars.append(np.copy(self.PEs[i]))
            temp = np.zeros(self.Is[i].shape, np.bool)
            temp[self.PE_stars[i] >= 0] = 1
            self.PE_stars[i][self.PE_stars[i] < 0] = abs(self.PE_stars[i][self.PE_stars[i] < 0]) + 64
            self.raw_LM.append(temp)
            self.PEAs.append(np.copy(self.PE_stars[i]))

        # # 计算PEA
        # self.PEAs.append(np.copy(self.PE_stars[0]))
        # self.raw_LM.append(np.zeros(self.PEAs[0].shape, np.bool))
        # for i in range(1, 4):
        #     self.PEAs.append(np.copy(self.PE_stars[i]))
        #     temp = np.zeros(self.Is[i].shape, np.bool)
        #     temp[self.PE_stars[i] < 64] = 1
        #     self.raw_LM.append(temp)
        #     # self.PEAs[i][self.PE_stars[i] > 64] = self.PEAs[i][self.PE_stars[i] > 64] | 0b10000000
        #     # self.PEAs[i][self.PE_stars[i] < 64] = self.PEAs[i][self.PE_stars[i] < 64] & 0b01111111

    @staticmethod
    def predict_method1(a, b):
        return math.ceil((a + b) / 2)

    @staticmethod
    def predict_method2(a, b):
        return math.ceil(math.sqrt(a * b))

    def __predict01(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[1] = np.zeros((h, w), np.int)
        for i in range(h):
            for j in range(w):
                if j < w - 1:
                    # self.Ps[1][i, j] = self.predict_method(I0[i, j], I0[i + 1, j])
                    self.Ps[1][i, j] = self.predict_method(I0[i, j], I0[i, j + 1])
                else:
                    self.Ps[1][i, j] = I0[i, j]

    def __predict02(self):
        I0 = self.Is[0]
        h, w = I0.shape
        self.Ps[2] = np.zeros((h, w), np.int)
        for i in range(h):
            for j in range(w):
                if i < h - 1:
                    # self.Ps[2][i, j] = self.predict_method(I0[i, j + 1], I0[i, j])
                    self.Ps[2][i, j] = self.predict_method(I0[i, j], I0[i + 1, j])
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
                    self.Ps[3][i, j] = self.predict_method(I0[i, j], I0[i + 1, j + 1])
                else:
                    self.Ps[3][i, j] = self.predict_method(I0[i, j + 1], I0[i + 1, j])

        for i in range(h - 1):
            self.Ps[3][i, w - 1] = self.predict_method(I0[i, w - 1], I0[i + 1, w - 1])

        for j in range(w - 1):
            self.Ps[3][h - 1, j] = self.predict_method(I0[h - 1, j], I0[h - 1, j + 1])

        self.Ps[3][h - 1, w - 1] = I0[h - 1, w - 1]

    def get_gull_img(self, imgs: str = "I"):
        res = np.zeros((self.H, self.W), np.int)
        h, w = int(self.H / 2), int(self.W / 2)
        if imgs == "PEA":
            arr = self.PEAs
        elif imgs == "PE":
            arr = self.PEs
        elif imgs == "P":
            arr = self.Ps
        elif imgs == "PEstar":
            arr = self.PE_stars
        else:
            arr = self.Is
        res[0:h, 0:w] = arr[0]
        res[0:h, w:self.W] = arr[1]
        res[h:self.H, 0:w] = arr[2]
        res[h:self.H, w:self.W] = arr[2]
        return res.astype(np.uint8)

    def encryption(self):
        self.encrypted_I = eu.encrypt(self.ans, eu.SECRET_KEY, 256)
        self.encrypted_LM = eu.encrypt(self.LM, eu.SECRET_KEY, 256)
        # print(self.res_img)
        # print(self.LM)
        return self.encrypted_I

    def max_length(self):
        """
        返回最多可以插入的长度
        :return:
        """
        return np.sum(self.LM)

    def data_hider(self, data: int):
        i, j, k = 0, 0, 0
        self.ans = np.copy(self.res_img)
        l = data.bit_length()
        # print(l)
        while i < self.H:
            while j < self.W:
                if self.LM[i, j]:
                    data_k = data & 0b1
                    self.ans[i, j] = self.ans[i, j] % 128 + data_k * 128
                    data >>= 1
                    k += 1
                    if k >= l:
                        return
                j += 1
            i, j = i + 1, 0
        if k < l:
            print("too many data!")

    def save(self, pth: str):
        """
        将LM和加密后的图片存储到路径中
        :param pth: 存储的路径
        :return:
        """
        iu.save_img(self.encrypted_I, pu.path_join(pth, "image.png"))
        iu.save_img(self.encrypted_LM, pu.path_join(pth, "LM.png"))
        # iu.save_img(self.LM.astype(np.uint8), pu.path_join(pth, "LM.png"))

    def recomposition(self):
        """
        将图片还原成本身的样子
        :return: self.res_img
        """
        self.res_img = np.zeros((self.H, self.W), np.uint8)
        self.LM = np.zeros((self.H, self.W), np.bool)
        h, w = int(self.H / 2), int(self.W / 2)
        for i in range(h):
            for j in range(w):
                self.res_img[2 * i, 2 * j] = self.PEAs[0][i, j]
                self.res_img[2 * i, 2 * j + 1] = self.PEAs[1][i, j]
                self.res_img[2 * i + 1, 2 * j] = self.PEAs[2][i, j]
                self.res_img[2 * i + 1, 2 * j + 1] = self.PEAs[3][i, j]
                self.LM[2 * i, 2 * j] = self.raw_LM[0][i, j]
                self.LM[2 * i, 2 * j + 1] = self.raw_LM[1][i, j]
                self.LM[2 * i + 1, 2 * j] = self.raw_LM[2][i, j]
                self.LM[2 * i + 1, 2 * j + 1] = self.raw_LM[3][i, j]
        return self.res_img


def __test(file):
    e = Encryptor(file, Encryptor.predict_method1)
    e.decomposition()
    e.predict()
    e.recomposition()
    print(e.max_length())
    e.data_hider(0b11000100000110001111111011100001000001100011111110111000010000011000111111101110000100000110001111111011)
    e.encryption()
    root_path = pu.get_root_path()
    out = pu.path_join(root_path, pu.OUTPUT_PATH)
    e.save(out)
    # lm = dec.decryptioner(e.encrypted_LM, dec.secretKey, 256)
    # diff = e.LM.astype(np.int) - lm.astype(np.int)
    # i = dec.decryptioner(e.encrypted_I, dec.secretKey, 256)
    # diff_I = i - e.res_img
    # print(np.sum(abs(diff)))
    # print(np.sum(abs(diff_I)))
    # iu.print_imgs(e.ans.astype(np.uint8), e.encrypted_LM.astype(np.uint8))
    pass


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_name = "200px-Lenna.jpg"
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    gray_lena = iu.read_img(file_path, iu.READ_GRAY)
    #
    # e1 = Encryptor(gray_lena, Encryptor.predict_method1)
    # e1.decomposition()
    # e1.predict()
    #
    # print(e1.error())

    # iu.print_imgs(e1.recomposition())
    __test(gray_lena)
