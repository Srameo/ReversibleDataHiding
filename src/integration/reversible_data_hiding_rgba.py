from src.integration.reversible_data_hidig import ReversibleDataHiding
from src.receiver.decryption import decryptioner
import src.util.encrypt_util as eu
import src.util.path_util as pu
import src.util.image_util as iu
import numpy as np
import cv2


class ReversibleDataHidingRGBA:
    b = ReversibleDataHiding()
    g = ReversibleDataHiding()
    r = ReversibleDataHiding()

    def __init__(self):
        self.LM = None

    @property
    def max_length(self):
        return self.r.e.max_length() + \
               self.g.e.max_length() + \
               self.b.e.max_length()

    @property
    def r_data(self):
        return self.r.r.data

    @property
    def g_data(self):
        return self.g.r.data

    @property
    def b_data(self):
        return self.b.r.data

    def encrypt(self, img: np.ndarray, r_data=0, g_data=0, b_data=0, pth="static/integral_rgba"):
        b_ = img[:, :, 0]
        g_ = img[:, :, 1]
        r_ = img[:, :, 2]
        self.b.encrypt(b_, b_data, pth=pth + "/b")
        self.g.encrypt(g_, g_data, pth=pth + "/g")
        self.r.encrypt(r_, r_data, pth=pth + "/r")
        self.LM = self.b.LM.astype(np.uint8) * 4 + \
                  self.g.LM.astype(np.uint8) * 2 + \
                  self.r.LM.astype(np.uint8) * 1
        self.encrypted_LM = eu.encrypt(self.LM, eu.SECRET_KEY, 256)
        self.encrypted = np.zeros((img.shape[0], img.shape[1], 4), np.uint8)
        self.encrypted[:, :, 0] = self.r.encrypted
        self.encrypted[:, :, 1] = self.g.encrypted
        self.encrypted[:, :, 2] = self.b.encrypted
        self.encrypted[:, :, 3] = self.encrypted_LM
        iu.save_img(self.encrypted, pu.path_join(pu.get_root_path(), pth, "image.png"))

    def decrypt(self, img: np.ndarray, pth="static/integral_rgba"):
        r_ = img[:, :, 0]
        g_ = img[:, :, 1]
        b_ = img[:, :, 2]
        a_ = img[:, :, 3]
        a_ = decryptioner(a_, eu.SECRET_KEY, 256).astype(np.uint8)
        r_LM = a_ % 2
        a_ >>= 1
        g_LM = a_ % 2
        a_ >>= 1
        b_LM = a_ % 2
        self.r.decrypt(r_, r_LM, False, pth=pth + "/r")
        self.g.decrypt(g_, g_LM, False, pth=pth + "/g")
        self.b.decrypt(b_, b_LM, False, pth=pth + "/b")
        r, g, b = self.r.decrypted, self.g.decrypted, self.b.decrypted
        self.decrypted = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        self.decrypted[:, :, 0] = b
        self.decrypted[:, :, 1] = g
        self.decrypted[:, :, 2] = r
        iu.save_img(self.decrypted, pu.path_join(pu.get_root_path(), pth, "res.png"))


if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_name = "200px-Lenna.jpg"
    # file_name = "trees.png"
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    color_lena = iu.read_img(file_path, iu.READ_COLOR)

    r_data = 0b11111000001111100000
    g_data = 0b11111111110000000000
    b_data = 0b10101010101010101010

    r = ReversibleDataHidingRGBA()
    r.encrypt(color_lena, r_data, g_data, b_data)
    iu.print_img(r.encrypted)

    # encrypted = iu.read_img(pu.path_join(root_path, "static", "integral_rgba", "image.png"), cv2.IMREAD_UNCHANGED)
    r.decrypt(r.encrypted)
    iu.print_img(r.decrypted)
    print(r.r_data, r.g_data, r.b_data)
    print(r.max_length)