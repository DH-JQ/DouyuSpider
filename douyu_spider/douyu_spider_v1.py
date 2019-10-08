from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import json


class DouyuSpider:

    def __init__(self):
        """ 初始化
        """
        start_url = 'https://www.douyu.com/g_LOL'

        self.browser = webdriver.Chrome()
        self.browser.get(start_url)

    # def fetch_one_page(self):
    #     import time
    #     time.sleep(5)
    #     page_source = self.browser.page_source
    #     html = etree.HTML(page_source)
    #     # print(etree.tostring(html))
    #     li_list = html.xpath('//ul[@class="layout-Cover-list"]/li')
    #     print(dir(li_list[0]))
    #     content_list = []
    #     for li in li_list:
    #         item = {}
    #         item['title'] = li.xpath('./div/a[1]/div[2]/div[1]/h3/@title')[0]
    #         item['hot'] = li.xpath('.//span[@DyListCover-hot]')

    #         # item['user'] = li.xpath('./h2')[0]
    #         content_list.append(item)
    #     print(len(li.xpath('.//span[@DyListCover-hot]')))
    #     print(content_list)

    def fetch_one_page(self):
        path = '//*[@id="listAll"]/div[2]/ul/li[8]/div/a[1]/div[2]/div[2]/span'
        method = EC.presence_of_element_located((By.XPATH, path))        
        wait = WebDriverWait(self.browser, 10)         
        # self.browser.refresh()
        wait.until(method, message='加载超时')
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        li_list = self.browser.find_elements_by_xpath('//ul[@class="layout-Cover-list"]/li')
        li_num = len(li_list)

        # //*[@id="listAll"]/div[2]/ul/li[1]/div/a[1]/div[2]/div[1]/h3
        title_path = '//*[@id="listAll"]/div[2]/ul/li[{}]/div/a[1]/div[2]/div[1]/h3'
        # hot_path = '//*[@id="listAll"]/div[2]/ul/li[{}]/div/a[1]/div[2]/div[2]/h2'
        hot_path = '//*[@id="listAll"]/div[2]/ul/li[{}]/div/a[1]/div[2]/div[2]/span'
        room_path = '//*[@id="listAll"]/div[2]/ul/li[{}]/div/a[1]'
        user_path = '//*[@id="listAll"]/div[2]/ul/li[{}]/div/a[1]/div[2]/div[2]/h2'
        items    = []
        for num in range(li_num):
            item = {}
            item['title'] = self.browser.find_element_by_xpath(title_path.format(num+1)).get_attribute('title')

            item['hot'] = self.browser.find_element_by_xpath(hot_path.format(num+1)).text

            item['room_url'] = self.browser.find_element_by_xpath(room_path.format(num+1)).get_attribute('href')

            item['user'] = self.browser.find_element_by_xpath(user_path.format(num+1)).text
            if num % 20 == 0:
                print(f'完成第{num+1}条数据')
                print(item)
            items.append(item)        
        return items

    def save_content(self, items):
        with open('douyu.json', 'a+', encoding='utf-8') as f:
            for item in items:
                # print(item)
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')

    def get_next_url(self, num):
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        max_num = self.browser.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/ul/li[last()-1]/a').text
        if num <= int(max_num):
            self.browser.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/span/span/input').clear()
            self.browser.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/span/span/input').send_keys(num)
            self.browser.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/span/span/span').click()
            next_flag = True
        if num >= int(max_num):
            next_flag = False
        return next_flag
        
    def run(self):
        next_flag = True
        num = 1
        while next_flag is not None:
            items = self.fetch_one_page()
            self.save_content(items)            
            print('*'*10 + f'完成第{num}页' + '*'*10)            
            if num % 2 == 0:
                self.browser.implicitly_wait(15)            
            num += 1
            next_flag = self.get_next_url(num)
            # next_url.click()
            # self.browser.implicitly_wait(1000)



if __name__ == '__main__':
    dou_spider = DouyuSpider()
    dou_spider.run()

