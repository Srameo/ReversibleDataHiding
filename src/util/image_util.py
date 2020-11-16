import cv2
import numpy as np

READ_GRAY = cv2.IMREAD_GRAYSCALE
READ_COLOR = cv2.IMREAD_COLOR


def read_img(file: str, color: int = READ_GRAY) -> np.ndarray:
    """
    读取一个图片并返回图片的数组
    :param file: 要读取的文件
    :param color: 读取的颜色空间，有两个取值
    :return: 一个numpy的array
    """
    res = cv2.imread(file, color)
    if res is None:
        raise ValueError("\"{0}\" is not a valid image!".format(file))
    return res
