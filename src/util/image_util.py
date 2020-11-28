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


def print_img(img: np.ndarray, name: str = "image") -> None:
    """
    打印一个图片，此时程序会进入阻塞状态！直到输入任一字符！
    :param img: 图片的数组
    :param name: 窗口的名字
    :return: None
    """
    cv2.imshow(name, img)
    cv2.waitKey()
    cv2.destroyWindow(name)


def print_imgs(*imgs) -> None:
    """
    打印一个图片，此时程序会进入阻塞状态！直到输入任一字符！
    :param imgs: 图片的数组
    :return: None
    """
    for index, img in enumerate(imgs):
        cv2.imshow(str(index), img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def save_img(img: np.ndarray, file: str) -> None:
    """
    保存图片到指定位置
    :param img: 要保存的图片数组
    :param file: 保存的位置
    :return: None
    """
    cv2.imwrite(file, img)
