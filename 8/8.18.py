from selenium import webdriver
import time
import os
import requests
import random

from urllib3.util import url


class Crawler_google_img:
    # 初始化
    def __init__(self):
        self.url = url

    # 获得Chrome驱动，并访问url
    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()  # 配置chrome启动
        chrome_options.add_argument("--disable-infobars")  # 添加启动参数
        chrome_options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'")
        browser = webdriver.Chrome(chrome_options=chrome_options)

        # chromeOptions 是一个配置 chrome 启动 是属性的类。通过这个类，我们可以为chrome配置如下参数（这个部分可以通过selenium源码看到）：
        # 设置 chrome 二进制文件位置 (binary_location)
        # 添加启动参数 (add_argument)
        # 添加扩展应用 (add_extension, add_encoded_extension)
        # 添加实验性质的设置参数 (add_experimental_option)
        # 设置调试器地址 (debugger_address)
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser

    # 下载图片
    def download_images(self, browser, round=10):
        picpath = 'G:/爬虫内容/爬取图片/images'
        # 路径不存在时创建一个
        if not os.path.exists(picpath):
            os.makedirs(picpath)

        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []

        count = 0  # 图片序号
        pos = 0
        for i in range(round):
            pos += 500
            # 向下滑动
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(1)

            # 找到图片
            # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
            # 直接通过tag_name来抓取是最简单的，比较方便

            img_elements = browser.find_elements_by_tag_name('img')

            # 遍历抓到的webElement
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')

                # 前几个图片的url太长，不是图片的url，先过滤掉，爬后面的
                if isinstance(img_url, str):
                    if len(img_url) <= 200:
                        # 将干扰的goole图标筛去
                        if 'images' in img_url:
                            # 判断是否已经爬过，因为每次爬取当前窗口，或许会重复
                            if img_url not in img_url_dic:
                                try:
                                    img_url_dic.append(img_url)
                                    # 下载并保存图片到当前目录下
                                    filename = "G:/爬虫内容/爬取图片/images/" + str(count) + ".jpg"
                                    r = requests.get(img_url)
                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()
                                    count += 1
                                    print('this is ' + str(count) + 'st img')
                                    # 防止反爬机制
                                    time.sleep(0.2)
                                except:
                                    print('failure')

    def run(self):
        self.__init__()
        browser = self.init_browser()
        self.download_images(browser, round=20)  # 可以修改爬取的页面数，基本10页是100多张图片
        browser.close()
        print("爬取完成")
