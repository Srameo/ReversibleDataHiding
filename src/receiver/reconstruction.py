import src.receiver.decryption as dec
import numpy as np
import src.util.image_util as iu
import src.util.path_util as pu
import math
import src.util.encrypt_util as eu
import src.encryption as en


class Receiver:

    def __init__(self, img: np.ndarray = None, LM: np.ndarray = None, decrypt_LM=True, predict=None):
        self.encrypted_img = img
        self.encrypted_LM = LM
        self.LM = []
        self.decrypt_LM = decrypt_LM
        self.PE_stars = []
        self.PEAs = []
        self.PEAs_whole = []
        self.PEE = []
        self.Is = []
        self.Is_whole = []
        self.Ps = [None] * 4
        self.res_img = []
        if predict is None:
            self.predict_method = self.predict_method1
        else:
            self.predict_method = predict
        if img is not None:
            self.H, self.W = img.shape

    def data_extraction(self, b_length):
        """
        取出数据
        Returns:
        """
        i, j, length = 0, 0, 0
        self.data = int(0)
        self.ans = np.copy(self.decrypted_img)
        while i < self.H:
            while j < self.W:
                if self.LM[i, j] == 1:
                    # print(data_k)
                    data_k = 0
                    if length < b_length:
                        self.data <<= 1
                        data_k = int(self.ans[i, j] / 128)
                        self.data = self.data | data_k
                        length += 1
                    self.ans[i, j] -= 128 * data_k
                j += 1
            i, j = i + 1, 0
        self.data = bin(self.data)[-1:1:-1]
        l = len(self.data)
        if l < length:
            self.data += "0" * (length - l)
        Receiver.save(self.ans, 'ans.png')

    def decryption(self):
        self.decrypted_img = dec.decryptioner(self.encrypted_img, eu.SECRET_KEY, 256).astype(np.uint8)
        if self.decrypt_LM:
            self.LM = dec.decryptioner(self.encrypted_LM, eu.SECRET_KEY, 256).astype(np.uint8)
        else:
            self.LM = self.encrypted_LM
        # print(self.img)
        # en_test_img = eu.encrypt(self.img, eu.SECRET_KEY, 256)
        # print(en_test_img)
        # de_test_img = dec.decryptioner(en_test_img, eu.SECRET_KEY, 256)
        # print(de_test_img)
        # print(self.decrypted_img)
        # Receiver.save(self.decrypted_img, 'decrypted.png')

    def recomposition(self):
        """
        将解密后的图片逆向还原
        其中得到PEE与PEA的顺序调换（直接利用lm）
        Returns:
        """
        # 先还原正负号得到PEE
        self.PEE = self.ans.copy().astype(np.int)
        i, j = 0, 0
        while i < self.H:
            while j < self.W:
                if not i % 2 and not j % 2:
                    j += 1
                    continue
                if not self.LM[i, j]:
                    self.PEE[i, j] -= 64
                    self.PEE[i, j] = -self.PEE[i, j]
                j += 1
            i += 1
            j = 0
        # Receiver.save(self.PEE, 'PEE.png')

        # 将图片分解为四部分
        # 得到PE_stars(PEA)
        h, w = int(self.H / 2), int(self.W / 2)
        for i in range(4):
            self.PE_stars.append(np.zeros((h, w), np.int))
        for i in range(h):
            for j in range(w):
                self.PE_stars[0][i, j] = self.PEE[2 * i, 2 * j]
                self.PE_stars[1][i, j] = self.PEE[2 * i, 2 * j + 1]
                self.PE_stars[2][i, j] = self.PEE[2 * i + 1, 2 * j]
                self.PE_stars[3][i, j] = self.PEE[2 * i + 1, 2 * j + 1]
        # self.PEAs_whole = Receiver.composition(self.PE_stars[0], self.PE_stars[1], self.PE_stars[2], self.PE_stars[3])
        # Receiver.save(self.PEAs_whole, 'PEAs.png')

        # 由I[0]获得预测矩阵Ps
        for i in range(0, 4):
            self.Is.append(self.PE_stars[i])
        self.Ps[0] = self.Is[0]
        self.__predict01()
        self.__predict02()
        self.__predict03()
        # self.Ps_whole = Receiver.composition(self.Ps[0], self.Ps[1], self.Ps[2], self.Ps[3])
        # Receiver.save(self.Ps_whole, 'Ps.png')

        # PEEs加上预测矩阵Ps
        # 得到Is
        for j in range(1, 4):
            self.Is[j] += self.Ps[j]
        # self.Is_whole = Receiver.composition(self.Is[0], self.Is[1], self.Is[2], self.Is[3])
        # Receiver.save(self.Is_whole, 'Is.png')

        # 将Is四部分按原放回
        # 得到复原图res
        self.res_img = np.zeros((self.H, self.W), np.uint8)
        h, w = int(self.H / 2), int(self.W / 2)
        for i in range(h):
            for j in range(w):
                self.res_img[2 * i, 2 * j] = self.Is[0][i, j]
                self.res_img[2 * i, 2 * j + 1] = self.Is[1][i, j]
                self.res_img[2 * i + 1, 2 * j] = self.Is[2][i, j]
                self.res_img[2 * i + 1, 2 * j + 1] = self.Is[3][i, j]
        # Receiver.save(self.res_img, 'res.png')

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

    @staticmethod
    def save(img, name):
        """
        :param pth: 存储的路径
        :return:
        """
        root_path = pu.get_root_path()
        out = pu.path_join(root_path, pu.REC_PATH)
        pth = pu.path_join(out, name)
        iu.save_img(img, pth)

    @staticmethod
    def composition(img0, img1, img2, img3):
        a = np.hstack((img0, img1))
        b = np.hstack((img2, img3))
        all = np.vstack((a, b))
        return all


def __test(img, LM):
    e = Receiver(img, LM)
    e.decryption()
    e.data_extraction(104)
    e.recomposition()
    Receiver.save(e.res_img, 'res.png')


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file1_name = "image.png"
    file1_path = pu.path_join(root_path, pu.OUTPUT_PATH, file1_name)
    file2_name = "LM.png"
    file2_path = pu.path_join(root_path, pu.OUTPUT_PATH, file2_name)

    encrypted_img = iu.read_img(file1_path, iu.READ_GRAY)
    LM = iu.read_img(file2_path, iu.READ_GRAY)
    __test(encrypted_img, LM)
