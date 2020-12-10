from src.receiver.reconstruction import Receiver
from src.encryption.encryptor import Encryptor
import src.util.path_util as pu
import src.util.image_util as iu


class ReversibleDataHiding:

    def __init__(self):
        self.r = None
        self.data_length = 0
        self.LM = None
        self.encrypted = None
        self.e = None
        self.decrypted = None
        self.root_path = pu.get_root_path()

    def encrypt(self, img, hide_data: int = 0, pth="static/integral"):
        self.data_length = hide_data.bit_length()
        e = Encryptor(img)
        e.decomposition()
        e.predict()
        e.recomposition()
        e.data_hider(hide_data)
        e.encryption()
        e.save(pu.path_join(self.root_path, pth))
        self.LM = e.LM
        self.encrypted = e.encrypted_I
        self.e = e

    def decrypt(self, img=None, LM=None, LM_encrypted=True, pth="static/integral"):
        if img is None:
            img = iu.read_img(pu.path_join(self.root_path, "static", "integral", "image.png"))
        if LM is None:
            LM = iu.read_img(pu.path_join(self.root_path, "static", "integral", "LM.png"))
        r = Receiver(img, LM, LM_encrypted)
        r.decryption()
        r.data_extraction(self.data_length)
        r.recomposition()
        iu.save_img(r.res_img, pu.path_join(self.root_path, pth, "res.png"))
        self.decrypted = r.res_img
        self.r = r


if __name__ == '__main__':
    a = ReversibleDataHiding()
    root_path = pu.get_root_path()
    file_name = "200px-Lenna.jpg"
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    gray_lena = iu.read_img(file_path, iu.READ_GRAY)

    a.encrypt(gray_lena, 0b11111111111111111111111)
    a.decrypt()
    print(a.r.data)