import sys
import os

sys.path.append(os.path.join(os.getcwd(), os.pardir))

# import src.util.image_util as iu
# import src.util.path_util as pu
# from src.util.encrypt_util import encrypt, decrypt, SECRET_KEY
# import numpy as np
from src.integration.reversible_data_hidig import main as main_hiding
from src.integration.reversible_data_hiding_rgba import main as main_hiding_rgba


def main():
    args = sys.argv
    run = None
    try:
        if args[1] == "gray":
            run = main_hiding
        elif args[1] == "rgb":
            run = main_hiding_rgba
        else:
            raise ValueError
    except IndexError:
        print("输入参数过少！第一个参数应为gray或rgb！\ngray表示加密灰度图像，rgb表示加密彩色图像")
        return
    except ValueError:
        print("第一个参数应为gray或rgb！")
        return
    file_name = "200px-Lenna.jpg"
    if len(args) > 2:
        file_name = args[2]
    run(file_name)


if __name__ == '__main__':
    main()
    # root_path = pu.get_root_path()
    # file_name = "200px-Lenna.jpg"
    # file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)
    #
    # gray_lena = iu.read_img(file_path, iu.READ_GRAY)
    # color_lena = iu.read_img(file_path, iu.READ_COLOR)
    #
    # lab_lena = cv2.cvtColor(color_lena, cv2.COLOR_RGB2LAB)
    # iu.print_img(lab_lena)
    #
    # iu.print_img(gray_lena, "gray lena")
    # iu.print_img(color_lena, "colorful lena")
    #
    # out_file_name = "200px-Gray-Lenna.jpg"
    # out_file_path = pu.path_join(root_path, pu.OUTPUT_PATH, out_file_name)
    #
    # # iu.save_img(gray_lena, out_file_path)
    # iu.print_imgs(gray_lena, color_lena)

    # root_path = pu.get_root_path()
    # img = iu.read_img(pu.path_join(root_path, "static/input/trees.png"), iu.READ_GRAY)
    #
    # e = encrypt(img, SECRET_KEY, 256)
    # d = decrypt(e, SECRET_KEY, 256)
    #
    # diff = np.sum(abs(d.astype(np.int) - img.astype(np.int)))
    # print(diff)
