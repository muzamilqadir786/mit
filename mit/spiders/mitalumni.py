# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mit.items import MitItem
import time
from lxml.html import fromstring
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

global username,password,locations
username = 'nadeem'
password = 'nina123nina'

class MitalumniSpider(scrapy.Spider):
    name = "mitalumni"
    allowed_domains = ["https://alum.mit.edu/"]
    start_urls = (
        #'https://alum.mit.edu/',
        'https://www.google.com.pk/',
    ) 

    def parse(self, response):
    	print "here in parse"
    	global username
        global password
        search_term = 'Cambridge'

        options = webdriver.ChromeOptions()
        #options.add_extension("c://block.crx")
        #options.add_extension("c://browsec.crx") #To use proxy extension to avoid blocking.
        
        #options.add_argument("--disable-javascript")
        #options.add_argument("--disable-java")
        #options.add_argument("--disable-plugins")
        #options.add_argument("--disable-popup-blocking")        
        #options.add_argument("--disable-images")   

        #driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options)
        #driver = webdriver.Firefox()
        driver = webdriver.Chrome('c://chromedriver.exe')
        #driver = webdriver.Firefox()
        driver.get('https://alumsso.mit.edu/cas/login?service=https%3A%2F%2Falum.mit.edu%2Fj_spring_cas_security_check')
        email_elem = driver.find_element_by_name("username")
        email_elem.send_keys(username)
        pass_elem = driver.find_element_by_name("password")
        pass_elem.send_keys(password)
        pass_elem.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.get("https://alum.mit.edu/user/directory/Search.dyn")
        # alumni_directory_xpath = driver.find_element_by_xpath('//a[contains(text(),"Alumni Directory")]')
        # alumni_directory_xpath.click()
        time.sleep(5)
        search_input_elem = driver.find_element_by_xpath('//input[@id="directory-search"]')
        search_input_elem.clear()
        search_input_elem.send_keys(search_term)
        try:
            search_btn = driver.find_element_by_xpath('//input[@id="refine-search"]')
            search_btn.click()
            time.sleep(8)        
        except Exception as e:
            print e
            #driver.refresh()
        
        html = fromstring(driver.page_source)    
        # alumni_links = html.xpath('//div[@class="result"]/h4/a/@href')
        # print alumni_links
        
        page_numbers = html.xpath('//p[@id="results-num"]/a/@href')
        total_records = html.xpath('//p[contains(text(),"records found.")]/text()')
        if total_records:
            total_records = total_records[0]
            total_records = int(re.search('\d*',total_records).group())
        else:
            total_records = 250
        
        for record_no in range(0,total_records,50):
            link = 'https://alum.mit.edu/user/directory/Search.dyn?No={}&Ntk=All&N=0&Ntt=Cambridge'.format(record_no)
            driver.get(link)
            html = fromstring(driver.page_source)    
            alumni_links = html.xpath('//div[@class="result"]/h4')
            links = []
            for link in alumni_links:
                if link.xpath('./span[contains(text(),"(Deceased)")]'):
                    continue
                alumni_link = link.xpath('./a/@href')
                if alumni_link:
                    links.append(alumni_link[0])

            print links
            print len(links)
            alumni_links = links

            for alumni_link in alumni_links:
                url = 'https://alum.mit.edu'+alumni_link
                driver.get(url)
                html = driver.page_source
                hxs = fromstring(html)
                department = hxs.xpath('normalize-space(//li/strong[contains(text(),"Department")]/../text())')
                degrees = hxs.xpath('normalize-space(//li/strong[contains(text(),"Degrees")]/../text())')
                living_groups = hxs.xpath('normalize-space(//li/strong[contains(text(),"Living Groups")]/../text())')
                activities = hxs.xpath('normalize-space(//li/strong[contains(text(),"Activities")]/../text())')
                sports = hxs.xpath('normalize-space(//li/strong[contains(text(),"Sports")]/../text())')            
                alumni_clubs = hxs.xpath('normalize-space(//li/strong[contains(text(),"Alumni Clubs")]/../text())')
                preferred_class_year = hxs.xpath('normalize-space(//li/strong[contains(text(),"Preferred Class Year:")]/../text())')
                term_address = hxs.xpath('normalize-space(//li/strong[contains(text(),"Address")]/../text())')
                phone = hxs.xpath('normalize-space(//li/strong[contains(text(),"Phone")]/../text())')
                home_address = hxs.xpath('normalize-space(//li[@class="mapHomeAddress"]/text())')
                work_address = hxs.xpath('normalize-space(//li[@class="mapWorkAddress"]/text())')
                company = hxs.xpath('normalize-space(//li/strong[contains(text(),"Company")]/../text())')
                job_title = hxs.xpath('normalize-space(//li/strong[contains(text(),"Job Title")]/../text())')
                last_update = hxs.xpath('normalize-space(//li/strong[contains(text(),"Last Update")]/../text())')
                email = hxs.xpath('//li/strong[contains(text(),"Email")]/../a/@href')
                
                item = MitItem()
                item['URL'] = url

                if department:
                    item['department'] = department
                if degrees:
                    item['degrees'] = degrees
                if living_groups:
                    item['living_groups'] = living_groups
                if activities:
                    item['activities'] = activities
                if sports:
                    item['sports'] = sports
                if alumni_clubs:
                    item['alumni_clubs'] = alumni_clubs
                if preferred_class_year:
                    item['preferred_class_year'] = preferred_class_year
                if term_address:
                    item['term_address'] = term_address
                if phone:
                    item['phone'] = phone
                if home_address:
                    item['home_address'] = home_address
                if company:
                    item['company'] = company
                if job_title:
                    item['job_title'] = job_title
                if last_update:
                    item['last_update'] = last_update
                if email:
                    item['email'] = email[0].replace('mailto:','')
                if work_address:
                    item['work_address'] = work_address
                yield item
            time.sleep(60)

            

        #time.sleep(90)
        #driver.quit()

    def parse_info(self,response):
        print "here in info"
        print response.url
        hxs = Selector(response)
        department = hxs.xpath('//li/strong[contains(text(),"Department")]/../text()')
        degrees = hxs.xpath('//li/strong[contains(text(),"Degrees")]/../text()')
        item = MitItem()
        item['department'] = department
        item['degrees'] = degrees
        yield item

        #pass
