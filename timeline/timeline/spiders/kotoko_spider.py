import scrapy

class LiveSpider(scrapy.Spider):
	name = "kotoko"
	allowed_domains = ['finn-neo.com']
	urls = ["https://finn-neo.com/user.cgi?pageno=%d&actmode=AblogArticleList&blogid=528" % num for num in range(1, 25+1)]
	start = 0
	
	def start_requests(self):
		url = self.urls[self.start]
		yield scrapy.Request(url=url, callback=self.parse)
	# print(start_urls)
	def parse(self, response):
		live_events = response.xpath('//div[@id="rightCon"]//div[@class="infoBox"]/dl[@class="close"]')
		# next_page = response.xpath('//*[@id="rightCon"]/div[@class="inBox"]/div[@class="infoBox"]/div[@class="indent"]/div[@class="pager"]/a/@href')
		
		for index, link in enumerate(live_events):
			# print(link.extract())
			live_element = {
				'time': link.xpath('dt/text()').extract_first(),
				'name': link.xpath('dt/p/text()').extract_first(), 
				# 'detail': link.xpath('dd').extract_first()
			}
			self.write_file(live_element)
		self.start += 1
		url = self.urls[self.start]
		yield scrapy.Request(url=url, callback=self.parse)
	
	def write_file(self, content):
		with open('result.txt', 'a', encoding='utf8') as f:
			line = "%-20s %s\n" % (content['time'], content['name'])
			f.write(line)