# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MitItem(scrapy.Item):
	URL = scrapy.Field()
	department = scrapy.Field() 
	degrees = scrapy.Field() 
	living_groups = scrapy.Field()
	activities = scrapy.Field()
	sports = scrapy.Field()
	alumni_clubs = scrapy.Field()
	preferred_class_year = scrapy.Field()
	term_address = scrapy.Field()
	phone = scrapy.Field()
	home_address = scrapy.Field()
	last_update = scrapy.Field()
	company = scrapy.Field()
	job_title = scrapy.Field()
	email = scrapy.Field()
	work_address = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
