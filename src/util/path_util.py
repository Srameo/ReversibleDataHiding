import os

PROJECT_NAME = "ReversibleDataHiding"
INPUT_PATH = "static" + os.sep + "input"
OUTPUT_PATH = "static" + os.sep + "output"
REC_PATH = "static" + os.sep + "reconstruction"


def get_root_path() -> str:
    """
    :return: 项目根路径
    """
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find(PROJECT_NAME + os.path.sep)+len(PROJECT_NAME + os.path.sep)]
    return root_path


def path_join(*paths) -> str:
    """
    返回拼接的路径
    :param paths: 路径集合
    :return: 拼接后的路径
    """
    total_path = ""
    for path in paths:
        total_path = os.path.join(total_path, path)
    return total_path
