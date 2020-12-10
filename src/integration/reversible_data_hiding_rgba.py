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

    def encrypt(self, img: np.ndarray, hide_data=0, pth="static/integral_rgba"):
        b_ = img[:, :, 0]
        g_ = img[:, :, 1]
        r_ = img[:, :, 2]
        self.b.encrypt(b_, pth=pth + "/b")
        self.g.encrypt(g_, pth=pth + "/g")
        self.r.encrypt(r_, pth=pth + "/r")
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
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    color_lena = iu.read_img(file_path, iu.READ_COLOR)

    r = ReversibleDataHidingRGBA()
    r.encrypt(color_lena)
    iu.print_img(r.encrypted)

    # encrypted = iu.read_img(pu.path_join(root_path, "static", "integral_rgba", "image.png"), cv2.IMREAD_UNCHANGED)
    r.decrypt(r.encrypted)
    iu.print_img(r.decrypted)