# 利用python生成简历

这个项目能够自动生成简历，从yaml文件中获取简历数据，并能够只能一页。

## 如何使用
- python3环境
- 克隆项目
- 创建虚拟环境并激活 ```python3 -m venv env```
- 安装依赖 ```pip install -r requirements.txt```

然后使用快速命令`cc-resume`，将显示交互式命令，会自动告知你本程序会搜索哪个目录的yaml数据文件，输入一个序号，然后将为你生成一页纸简历。

```shell
(py38) PS Z:\4t\mnt\code\mine\cc-resume> cc-resume.exe
=== 本工具完全免费, 由B站UP主吵吵博士开发 ===
find resume yaml in C:\Users\admin\AppData\Local\cc\resume
please choose one yaml:
1: author.yaml
2: demo.yaml
3: test20240418.yaml
q: exit
please input number[1-3]:1
now generate pdf for author.yaml
create pdf 1 times
pdf page is 2, path is C:\Users\admin\AppData\Local\cc\resume\author.pdf
page=2, font_size=15, padding=10, height=820.2897637795277, frame_height=733.4897637795277
create pdf 2 times
pdf page is 2, path is C:\Users\admin\AppData\Local\cc\resume\author.pdf
page=2, font_size=15, padding=9, height=820.2897637795277, frame_height=737.4897637795277
create pdf 3 times
pdf page is 2, path is C:\Users\admin\AppData\Local\cc\resume\author.pdf
page=2, font_size=15, padding=8, height=820.2897637795277, frame_height=773.4897637795277
create pdf 4 times
pdf page is 2, path is C:\Users\admin\AppData\Local\cc\resume\author.pdf
page=2, font_size=15, padding=7, height=820.2897637795277, frame_height=798.4897637795277
create pdf 5 times
pdf page is 1, path is C:\Users\admin\AppData\Local\cc\resume\author.pdf
page=1, font_size=15, padding=6, height=820.2897637795277, frame_height=24.48976377952772
(py38) PS Z:\4t\mnt\code\mine\cc-resume> 
```

从上面的实际操作记录来看，一共生成了6次，终于生成成功，并提示了最终的pdf文件的位置。

## 截图

本项目自带的`author.yaml`生成的pdf如下：

![image.png](https://gitee.com/m986883511/picture-bed/raw/master/PyPicGo/cs-20240419134328-tmp.png)
