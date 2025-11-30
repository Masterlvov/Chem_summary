
Q1:python配置opencv环境后，读取图片，报错：findDecoder imread_('../Rawfig/xfc石墨2.0/21.jpg'):can't open/read file: check file path/integrity<br>
A1:报错原因：路径出现中为字符，解决办法：修改为英文路径。

Q2: jupyter notebook怎么修改默认目录？
A2: 
方法1：jupyter notebook --notebook-dir=/path/to/your/directory

方法2：通过修改 Jupyter 的配置文件来永久更改默认打开的目录。以下是具体步骤：
1. 生成 Jupyter 配置文件（如果不存在）
在命令行中输入以下命令来生成 Jupyter 配置文件：

jupyter notebook --generate-config
如果配置文件已经存在，会提示你是否覆盖，一般选择不覆盖。

2. 找到并打开 Jupyter 配置文件
配置文件通常位于以下路径：

Windows：C:\Users\your_username\.jupyter\jupyter_notebook_config.py
使用文本编辑器（如记事本、VS Code 等）打开该文件。

3. 修改配置文件中的目录设置
在配置文件中找到以下行（可能被注释掉了，即以 # 开头）：
‘# c.NotebookApp.notebook_dir = ''’
去掉行首的注释符号 #，并在引号中填入你想要设置的默认目录路径，例如：
c.NotebookApp.notebook_dir = '/path/to/your/directory'

Q3: python镜像源安装<br>
A3: 命令行修改配置：pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/，之后pip install packagename.

临时使用；pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple/