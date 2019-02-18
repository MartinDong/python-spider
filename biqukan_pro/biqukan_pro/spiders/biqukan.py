# -*- coding: utf-8 -*-

import scrapy
from pymongo import MongoClient


# scrapy crawl biqukan --nolog
class BiqukanSpider(scrapy.Spider):
    print("*************************************************************************")
    print("\n\t\t欢迎使用《笔趣看》小说下载小工具\n\n\t\t作者:NJ宇众不同\t时间:2019-02-17\n")
    print("*************************************************************************")

    # 小说地址
    # target_url = str(input("请输入小说目录下载地址:\n"))

    name = 'biqukan'
    allowed_domains = ['biqukan.com']
    start_urls = ['https://www.biqukan.com/57_57405/']

    # 建立MongoDB数据库连接
    client = MongoClient('localhost', 27017)
    # 连接所需数据库
    db = client.biqukan
    # 连接所用集合，也就是我们通常所说的表
    collection = db.novel

    def parse(self, response):
        # 提取小说基本信息
        # 小说名称
        novel_name = response.xpath('.//div[@class="info"]//h2//text()').extract()
        if novel_name:
            flag_name = "《" + novel_name[0] + "》" + "正文卷"
            print("flag_name====", flag_name)

            # 提取小章节信息
            # 章节列表
            chapters = response.xpath('.//div[@class="listmain"]//dl//dt | .//div[@class="listmain"]//dl//dd')
            # print(chapters)
            begin_flag = False
            for child in chapters:
                # print(child)
                if child != '\n':
                    # 只有正文章节才提取
                    if child.xpath('.//text()').extract()[0] == u"%s" % flag_name:
                        begin_flag = True
                    if begin_flag == True and len(child.xpath('.//a')) > 0:
                        aMark = child.xpath('.//a')
                        chapterHref = aMark.xpath('@href').extract()
                        download_url = "https://www.biqukan.com" + chapterHref[0]
                        yield scrapy.Request(url=download_url, callback=self.parse)
        chapter_name = response.xpath('.//div[@class="content"]//h1//text()').extract()
        # print(chapter_name)
        if chapter_name:
            chapter_content = response.xpath('.//div[@id="content" and @class="showtxt"]//text()').extract()
            # print(chapter_content[0])
            # soup_text = chapter_content[0].replace('\xa0', '')
            # print(chapter_content)
            self.saveNovel(chapter_name[0], chapter_content)

    # 向集合中插入数据
    # https://www.biqukan.com/0_973/276441.html
    def saveNovel(self, name, text):
        content = ""
        for each in text:
            content += each.replace('\xa0', '')

        if self.findNovelByName(name) is None:
            print("====保存数据====")
            self.collection.insert(
                {
                    "name": name,
                    "content": content,
                }
            )

    # 根据小说ID查询
    def findNovelByName(self, name):
        print("====查找数据====")
        res = self.collection.find_one({"name": name})
        print(res)
        return res
