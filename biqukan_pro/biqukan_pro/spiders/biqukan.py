# -*- coding: utf-8 -*-
import collections
import re

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
        charter = re.compile(u'[第](.+)章', re.IGNORECASE)

        # 小说名称
        novel_name = response.xpath('.//div[@class="info"]//h2//text()').extract()
        flag_name = "《" + novel_name[0] + "》" + "正文卷"
        # print("flag_name====", flag_name)

        # 章节列表
        chapters = response.xpath('.//div[@class="listmain"]//dl//dt | .//div[@class="listmain"]//dl//dd')
        # print(chapters)

        # 获取下载链接
        download_dict = collections.OrderedDict()
        begin_flag = False
        numbers = 1

        for child in chapters:
            # print(child)
            if child != '\n':
                if child.xpath('.//text()').extract()[0] == u"%s" % flag_name:
                    begin_flag = True

                if begin_flag == True and len(child.xpath('.//a'))>0:
                    aMark = child.xpath('.//a')
                    chapterName = aMark.xpath('.//text()').extract()

                    chapterHref = aMark.xpath('@href').extract()
                    download_url = "https://www.biqukan.com" + chapterHref[0]

                    names = str(chapterName).split(' ')
                    name = charter.findall(names[0] + '章')
                    if name:
                        download_dict[chapterName[0]] = download_url
                        numbers += 1
        # print(download_dict)

        if novel_name[0] in os.listdir():
            os.remove(novel_name[0])
        index = 1

        # 下载中
        print("《%s》下载中:" % novel_name[0])
        for key, value in download_dict.items():
            print(key, value)


        pass

    """
    函数说明:爬取文章内容

    Parameters:
        url - 下载连接(string)

    Returns:
        soup_text - 章节内容(string)

    Modify:
        2017-05-06
    """

    def Downloader(self, url):
        download_req = request.Request(url=url, headers=self.__head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('gbk', 'ignore')
        soup_texts = BeautifulSoup(download_html, 'lxml')
        texts = soup_texts.find_all(id='content', class_='showtxt')
        soup_text = BeautifulSoup(str(texts), 'lxml').div.text.replace('\xa0', '')
        return soup_text

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
            f.write(name+'\n\n')
            for each in text:
                if each == 'h':
                    write_flag = False
                if write_flag == True and each != ' ':
                    f.write(each)
                if write_flag == True and each == '\r':
                    f.write('\n')
            f.write('\n\n')