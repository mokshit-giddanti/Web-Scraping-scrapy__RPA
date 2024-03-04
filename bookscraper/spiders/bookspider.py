import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]


# this is to get the items data from all pages
    # def parse(self, response):
        #books=response.css('article.product_pod')
        # for book in books:
        #     yield{
        #         'name':book.css('h3 a::text').get(),
        #         'price':book.css('.product_price .price_color::text').get(),
        #         'url':book.css('h3 a').attrib['href'],
        #     }
        # nextpage=response.css('li.next a ::attr(href)').get()
        # if nextpage is not None:
        #     if 'catalogue/' in nextpage:
        #         nextpageurl='https://books.toscrape.com/'+nextpage
        #     else:
        #         nextpageurl='https://books.toscrape.com/catalogue/'+nextpage
        #     yield response.follow(nextpageurl,callback=self.parse)

# this is to get data of each book from all pages
    def parse(self, response):
        books=response.css('article.product_pod')
        for book in books:
            # yield{
            #     'name':book.css('h3 a::text').get(),
            #     'price':book.css('.product_price .price_color::text').get(),
            #     'url':book.css('h3 a').attrib['href'],
            # }
            bookpage=book.css('h3 a ::attr(href)').get()
            # if nextpage is not None:
            if 'catalogue/' in bookpage:
                bookurl='https://books.toscrape.com/'+bookpage
            else:
                bookurl='https://books.toscrape.com/catalogue/'+bookpage
            yield response.follow(bookurl,callback=self.parse_book_page)
        nextpage=response.css('li.next a ::attr(href)').get()
        if nextpage is not None:
            if 'catalogue/' in nextpage:
                nextpageurl='https://books.toscrape.com/'+nextpage
            else:
                nextpageurl='https://books.toscrape.com/catalogue/'+nextpage
            yield response.follow(nextpageurl,callback=self.parse)
    
    def parse_book_page(self,response):
        table_rows=response.css('table tr')
        yield{
            'url':response.url,
            'title':response.css('.product_main h1::text').get(),
            'Product Type':table_rows[1].css('td ::text').get(),
            'Price':table_rows[3].css('td ::text').get(),
            'Tax':table_rows[4].css('td ::text').get(),
            'Availability':table_rows[5].css('td ::text').get(),
            'reviews':table_rows[6].css('td ::text').get(),
            'rating':response.css('p.star-rating').attrib['class'],
        }
