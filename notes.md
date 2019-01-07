>[慕课网学习链接](https://www.imooc.com/learn/1017)
#开始
##1.创建项目
    scrapy startproject xxx

##2.生成spider
进入项目路径下spiders文件夹

    scrapy genspider xxx_spider movie.douban.com

##3.配置设置
setting里的user agent需要修改

##4.运行测试
可以写一个main.py来代替cmd，或者，在spider直接写个main？

    from scrapy import cmdline
    cmdline.execute("scrapy crawl douban250".split())

##5.报错
####缺少win32 api

    pip install pywin32

####DNS lookup failed: no results for hostname lookup: https
- 生成spider的时候，后面的url，在spider里会自动添加http，去掉就正常了
- 网络无连接，检查网络
##测试完成

#pass

##1.xpath
进入页面查看数据所在位置，在浏览器安装一个xpath工具
>[XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl)

定位语法规则：
- 定位到类名为xxx的

        //div[@class="xxx"]
- 定位下一级

        //
- 定位href

        //span[@class="next"]//a/@href
- p标签，获取第一段...

        //p[1]
- 获取文本内容

        /text()
##2.使用xpath，获取数据
在页面上使用xpath工具，找到数据列表位置，复制xpath，进入spider  (.md[2个空格+回车]()/2个回车 换行)

- parse：默认解析方法  
- 获取对象列表,然后开始循环列表  

        list = response.xpath("//xx//xxx")
        for i in list:
            pass
- 实例化item  
    
        from ..items import *
        items = XXXItem()
- 获取

        # 获取全部，存为列表
        item["xx"]=i.xpath(".//xxxx//x/text()").extract()
        # 获取列表第一个[0]，字符串
        item["xx"]=i.xpath(".//xxxx//x/text()").extract_first()
##3.数据处理
获取到需要的数据之后，在for循环外，yield 一整个items对象
        
        yield items
会将其交给pipelines，管道，用于待会保存数据等操作  
####·下一页
在页面上定位到下一页的a标签，获取它的href，然后同样yield，这里理解，应该是交给队列了。  
这里忘记写回调函数，但是似乎也不妨碍所有数据的获取

        next_link = response.xpath('//span[@class="next"]//a/@href').extract_first()
        if next_link:  # 如果有内容
            next_link = scrapy.Request("https://movie.douban.com/top250"+next_link, callback=self.parse)
            yield next_link
####·保存数据

        scrapy crawl douban250 -o xxx.json
        scrapy crawl douban250 -o xxx.csv
用excel打开csv可能会乱码，用编辑器打开保存为utf-8 bom格式即可
####·很久没用的mongodb
控制台输入mongod，报错，找不到/data/db

        mongod --dbpath xxxxxx
报错，路径不能有空格
切换到目录下再来一次，可以了，访问localhost:27017

        It looks like you are trying to access MongoDB over HTTP on the native driver port.
还不是很熟练。  
现在在c盘下新建了data/db文件夹，  
cmd直接mongod打开，使用navicat连接

准备就绪之后就可以在setting里开启pipelines（即取消掉注释）  
然后去pipelines创建连接，写入数据

打开pipelines.py，先导入pymongo

        import pymongo
然后定义多一个init方法，来到pipelines在初始化时同时打开连接         
定义主机、端口、库名、集合名 

        def __init__(self):
            host = "127.0.0.1"
            port = 27017
            dbname = "test"
            collection_name = "test1"
            client = pymongo.MongoClient(host,port)
            mydb = client[dbname]
            self.post = mydb[collection_name]
再在process_item方法中把item转换为字典，然后insert进mongodb，结果ok

        def process_item(self, item, spider):
            data = dict(item)
            self.post.insert(data)
            return item
            
##4.伪装
代理ip：在middleware.py最后加入自定义中间件

        # 自定义中间件：ip代理
        class my_ip_proxy(object):
            def process_request(self, request, spider):
                # 代理主机和端口
                request.meta['proxy'] = 'http-cla.abuyun.com:9030'
                # 主机用户名密码
                proxy_name_pwd = b'xxxxxx:xxxxxx'
                # 加密用户名密码
                encode_info = base64.b64encode(proxy_name_pwd)
                request.headers['Proxy-Authorization'] = 'Basic ' + encode_info.decode()
                # 完成之后要到setting中找到middleware添加
随机agent：同上，定义中间件，在网上搜索scrapy user agent，找一个列表
        
    USER_AGENT_LIST = [
        'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
        'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
        'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
        'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
        'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
        'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
        'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
        'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
    ]
然后定义随机选择

        agent = random.choice(USER_AGENT_LIST)
        request.headers['User_Agent'] = agent
运行main，可见中间件已经被使用
>Alt + Enter，可以快速提示并导入模块