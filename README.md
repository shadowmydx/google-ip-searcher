# google-ip-searcher

这是一个在macbook上使用Pycharm开发的、并没有在Linux和windows上测试过的google-ip-searcher。

使用python default.py来启动程序，根目录下会打出寻找到的ip信息，并整理一份可以复制进Goagent的ini格式。

tips: 也可以使用python fromConfig.py，ip_list是我收集的能够返回证书的全部ip地址，直接从这里找可以更快。

2015/26/10：

1、增加fromConfig.py入口，读取并测试以斜线分割的ip地址。

2、修复一个写文件的bug

2015/27/10：

1、造了个线程安全的日志输出模块Logger，并将输出升级为Logger

2015/09/12

1、抄来了一个ip_range, 入口是fromFile，注释了mac平台中的测速逻辑，因此可以跑在任何平台上


检测逻辑：

1、先测试能否连接上目标ip的443端口，若成功进入2，若超时失败则返回。

2、测试返回的证书commonName是否包含google的字样，若成功进入3，若超时或没有google字样则返回。

3、使用goagent的proxylib.py中的检测逻辑来做最后的判断能否使用该ip，这段代码是直接从goagent那边移植过来的。


本项目目前支持通过nslookup -q=TXT _netblocks.google.com 8.8.8.8命令来搜索goagent可用的google ip，可以通过修改源代码
来实现定制的ip地址扫描，目前支持的ip段地址模式为xx.xx.xx.xx/xx，其他的因为懒，并没有加。

本项目的架构设计可以在这里找到：

http://www.cnblogs.com/shadowmydx/p/4873160.html
