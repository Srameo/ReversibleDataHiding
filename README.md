# ReversibleDataHiding
> 2020秋-信息安全基础-高铁杠教授

- [ReversibleDataHiding](#reversibledatahiding)
  - [File Structure](#file-structure)
  - [environment](#environment)
  - [contributor](#contributor)
  - [使用说明](#使用说明)

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
    - [util](./src/util/README.md): 工具package

## environment

- python  (v3.8.6)
- opencv3  (v4.0.0.21)
- numpy  (v1.18.5)
- scipy  (v1.4.1)

## contributor

- 靳鑫: [https://github.com/Srameo](https://github.com/Srameo)
- 陈昭宇: [https://github.com/czy1812977](https://github.com/czy1812977)
- 张祥玙: [https://github.com/westrious](https://github.com/westrious)
- 吴若愚: [https://github.com/Wuruoyu1](https://github.com/Wuruoyu1)
- 贾雨欣: [https://github.com/xiaohuaniangniang](https://github.com/xiaohuaniangniang)
- 李奥

## 使用说明

1. 确保电脑上装有[environment](#environment)中所有的需求!
2. 进入src文件夹
3. 执行`python main.py arg1 [arg2]`
   - arg1: `gary` 或者 `rgb`, 表示需要加密的图像为灰度或者彩色
   - arg2: 想要加密的文件名, **文件必须在`/static/input`中！否则会找不到文件！**
4. 其中彩色图像的加密解密以及中间结果保存在`/static/integral_rgba`中，灰度图像的保存在`/static/integral`中