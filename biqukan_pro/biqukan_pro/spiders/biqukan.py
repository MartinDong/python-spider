# -*- coding: utf-8 -*-

import scrapy


# scrapy crawl biqukan --nolog
class BiqukanSpider(scrapy.Spider):
    print("*************************************************************************")
    print("\n\t\t欢迎使用《笔趣看》小说下载小工具\n\n\t\t作者:NJ宇众不同\t时间:2019-02-17\n")
    print("*************************************************************************")

    # 小说地址
    # target_url = str(input("请输入小说目录下载地址:\n"))

    name = 'biqukan'
    allowed_domains = ['biqukan.com']
    start_urls = ['https://www.biqukan.com/0_973/']

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
        print(chapter_name)
        if chapter_name:
            chapter_content = response.xpath('.//div[@id="content" and @class="showtxt"]//text()').extract()
            # print(chapter_content[0])
            # soup_text = chapter_content[0].replace('\xa0', '')
            print(chapter_content)
            self.Writer(chapter_name[0], "爬蟲.txt", chapter_content)

    """
    函数说明:将爬取的文章内容写入文件

    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)

    Returns:
        无

    Modify:
        2019-02-18
    """

    def Writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as  f:
            f.write(name + '\n\n')
            for each in text:
                each = each.replace('\xa0', '')
                if each == 'h':
                    write_flag = False
                if write_flag == True and each != ' ':
                    f.write("\t" + each)
            f.write('\n\n')
