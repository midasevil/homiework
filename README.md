操作环境  python 3.5  依赖库 scrapy scrapy-redis pymysql lxml

这是关于爬虫的小作业
目标在于：
1.使用 scrapy / pyspider 抓取 亚马逊-文学图书 上尽可能多的书籍名称、价格及评论数
2.从京东爬取相应的书籍信息（价格及评论数）
3.实现书籍的去重，并考虑如果抓取价格更新的问题
4.将爬取到的信息存入 mysql 中


项目抓取逻辑：
为实现目标，搭建两个scrapy工程Amoj,jinS.(两个工程在项目逻辑上可以相对独立，虽然也可以作为两个爬虫写在一个项目里，用custome_settings做到相对独立，但是
我很懒）。因为亚马逊索引页只有七十五页的限制，也就是最多在一个索引标签下提供1200items的信息，Amoj中的amoj爬虫负责通过文学图书（or 作为更大范围的图书）
的作者索引页作为start，再分别访问各作者作品的索引页（可喜可贺的是没有作者写了超过1200本的书）抓取item信息。jinS中的jins爬虫则通过各item的title信息在京东图书中进行
检索，获得检索首页所得到的所有item信息。


分布式实现;
分布式实现是基于scrapy-redis的解决方案，由redis实现request的调度与去重，并且amoj爬取得到的title信息通过startrequestpipeline加工生成title相关的京东
索引页url，存入redis作为jins的start-urls。


item去重：
爬取item的信息时，包括了唯一标识item的pid,可以通过这些pid对各物品在亚马逊与京东唯一访问item的detail信息，并以这些pid为主键，重复pid物品会被丢弃。

其他中间件实现;
包括实现轮转user-agents，轮转代理ip，添加时间字段，爬虫名称的中间件。


计划实现：可视化扩展，docker部署，连接构造基于redis的代理ip池
