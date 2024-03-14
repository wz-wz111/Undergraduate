# 如何复现我们的项目？

# 1. 数据库

首先创建数据库，运行SupMarDB中的sql语句创建名为supermarket的mysql数据库。

# 2. 后端

python配置：使用pip安装下面库（flask、flask_cors、json_flask、json_response、json、pymysql）

运行app.py即可。

# 3. 前端

首先准备好Node和Python环境

1. 安装安装Vue脚手架

~~~
npm install -g @vue/cli
~~~

2. 创建名为front的vue2项目

~~~
vue create front
~~~

此时要选择创建选项，选择

Manually select features，然后只勾选Router，之后版本选择2.x，选In package.json

3. 下载完成后，进入到项目内，下载需要的库

~~~
cd front
npm install axios --save
npm i element-ui -S
~~~

4. 运行

~~~
npm run serve
~~~

如果运行时显示缺失什么库，就使用`npm install xx`来安装即可。