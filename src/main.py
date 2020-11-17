import src.util.image_util as iu
import src.util.path_util as pu
import cv2

if __name__ == '__main__':
    root_path = pu.get_root_path()
    file_name = "200px-Lenna.jpg"
    file_path = pu.path_join(root_path, pu.INPUT_PATH, file_name)

    gray_lena = iu.read_img(file_path, iu.READ_GRAY)
    color_lena = iu.read_img(file_path, iu.READ_COLOR)

    lab_lena = cv2.cvtColor(color_lena, cv2.COLOR_RGB2LAB)
    iu.print_img(lab_lena)

    iu.print_img(gray_lena, "gray lena")
    iu.print_img(color_lena, "colorful lena")

    out_file_name = "200px-Gray-Lenna.jpg"
    out_file_path = pu.path_join(root_path, pu.OUTPUT_PATH, out_file_name)

    # iu.save_img(gray_lena, out_file_path)
    iu.print_imgs(gray_lena, color_lena)
