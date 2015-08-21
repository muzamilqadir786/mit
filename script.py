import os
print "Scraper running ...."
os.popen("scrapy crawl mitalumni -o mitdata.csv -t csv")
print "Successfully done...."
