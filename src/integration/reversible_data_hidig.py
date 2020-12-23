from src.receiver.reconstruction import Receiver
from src.encryption.encryptor import Encryptor
import src.util.path_util as pu
import src.util.image_util as iu


class ReversibleDataHiding:
    __INTEGRAL_PATH = pu.path_join("static", "integral")

    def __init__(self):
        self.r = None
        self.data_length = 0
        self.LM = None
        self.encrypted = None
        self.e = None
        self.decrypted = None
        self.root_path = pu.get_root_path()

    def encrypt(self, img, hide_data: int = 0, pth=__INTEGRAL_PATH):
        """

        Args:
            img: 要加密的图片
            hide_data: 想要隐藏的数据
            pth: 保存的相对路径

        Returns:

        """
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

    def decrypt(self, img=None, LM=None, LM_encrypted=True, pth=__INTEGRAL_PATH):
        """

        Args:
            img: 需要解密的图像
            LM: 保存有LM图像
            LM_encrypted: LM是否需要解密
            pth: 保存的路径

        Returns:

        """
        if img is None:
            img = iu.read_img(pu.path_join(self.root_path, pth, "image.png"))
        if LM is None:
            LM = iu.read_img(pu.path_join(self.root_path, pth, "LM.png"))
        r = Receiver(img, LM, LM_encrypted)
        r.decryption()
        r.data_extraction(self.data_length)
        r.recomposition()
        iu.save_img(r.res_img, pu.path_join(self.root_path, pth, "res.png"))
        self.decrypted = r.res_img
        self.r = r


def main(file_name):
    a = ReversibleDataHiding()
    root_path = pu.get_root_path()
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    gray_lena = iu.read_img(file_path, iu.READ_GRAY)
    # changed_gray_lena = gray_lena.copy()
    # changed_gray_lena[100, 100] = 0

    # a.encrypt(gray_lena, 0b11111000001111100000)
    # a.decrypt()

    # print("1")
    print("encrypting!")
    print("insert data: 0b11111000001111100000")
    a.encrypt(gray_lena, 0b11111000001111100000)
    # print("2")
    print("decrypting!")
    a.decrypt()
    # print("3")
    # a.encrypt(changed_gray_lena, 0b11111000001111100000, pth="static/test/changed")
    # print("4")
    # a.decrypt(pth="static/test/changed")
    print("extract data: ", end="")
    print(a.r.data)
    print(f"hide data max length: {a.e.max_length()}")
    print(f"image size: {gray_lena.shape}")
    # print(a.r.data)
    print("file save in /static/integral!")


if __name__ == '__main__':
    main("200px-Lenna.jpg")
