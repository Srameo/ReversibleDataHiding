# ReversibleDataHiding
> 2020秋-信息安全基础-高铁杠教授

## File Structure
- [\$root\$](./README.md): root folder
  - [static](./static/README.md): image folder
    - difference: 输出图片区别的文件夹
    - input
    - integral: 保存整合之后的测试图片输出
    - integral_rgba: 保存整合之后的测试图片输出（彩色）
    - output: 临时输出
    - reconstruction: 接受端的测试
    - test: 批量测试的文件夹
  - [src](./src/README.md): source code
    - [analysis](./src/analysis/README.md): 用于分析实验结果
    - [encryption](./src/encryption/README.md): 加密与隐藏数据部分的数据
    - [integration](./src/integration/README.md): 加密和解密双向的整合
    - [receiver](./src/receiver/README.md): 重构的源文件
    - [util](./src/util/)

## environment

- python  (v3.8.6)
- opencv3  (v4.0.0.21)
- numpy  (v1.18.5)
- scipy  (v1.4.1)