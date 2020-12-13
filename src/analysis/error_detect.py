import src.util.image_util as iu
import src.util.path_util as pu

import numpy as np

if __name__ == '__main__':
    root_path = pu.get_root_path()
    src_black_img = iu.read_img(pu.path_join(root_path, pu.INPUT_PATH, "200px-Lenna.jpg"), iu.READ_GRAY)
    res_black_img = iu.read_img(pu.path_join(root_path, "static", "integral", "res.png"), iu.READ_GRAY)

    src_color_img = iu.read_img(pu.path_join(root_path, pu.INPUT_PATH, "trees.png"), iu.READ_COLOR)
    res_color_img = iu.read_img(pu.path_join(root_path, "static", "integral_rgba", "res.png"), iu.READ_COLOR)

    diff_color_img = abs(src_color_img.astype(np.int) - res_color_img.astype(np.int)).astype(np.uint8)
    diff_black_img = abs(src_black_img.astype(np.int) - res_black_img.astype(np.int)).astype(np.uint8)

    iu.print_imgs(diff_black_img, diff_color_img)

    diff_color_path = pu.path_join(root_path, "static", "difference", "color_difference.png")
    diff_black_path = pu.path_join(root_path, "static", "difference", "black_difference.png")

    iu.save_img(diff_black_img, diff_black_path)
    iu.save_img(diff_color_img, diff_color_path)