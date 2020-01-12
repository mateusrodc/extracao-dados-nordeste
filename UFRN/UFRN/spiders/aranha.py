# -*- coding: utf-8 -*-
import scrapy
from ..items import UfrnItem
import re
from html import unescape


class AranhaSpider(scrapy.Spider):
    name = 'ufrn'
    #allowed_domains = ['https://repositorio.ufrn.br/']
    start_urls = ['https://repositorio.ufrn.br/jspui/simple-search?query=saude+mental&sort_by=score&order=desc&rpp=10&etal=0&start=0']

    def parse(self, response):
        lista = response.css('td:nth-child(2) a::attr(href)').extract()
        next_page= response.css('.pagination li:last-child a::attr(href)').get()
        for link in lista:
            yield response.follow(link, self.parse_article)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_article(self, response):
        itens = UfrnItem()
        itens["title"] = response.css('tr td.metadataFieldLabel.dc_title+ td::text').extract()[0]

        author = response.css('tr td.metadataFieldLabel.dc_contributor_author+ td > a::text').extract()[0]
        author = author.split(", ")
        author = f"{author[1]} {author[0]}"
        itens["author"] = author

        keywords = response.css('tr td.metadataFieldLabel.dc_subject+ td::text').extract()[0]
        keywords = keywords.split(";")
        itens["keywords"] = keywords

        itens["date"] = response.css('tr td.metadataFieldLabel.dc_date_issued+ td::text').extract()[0]

        itens["abstract"] = response.css('tr td.metadataFieldLabel.dc_description_resumo+ td::text').extract()[0]

        itens["uri"] = response.css('tr td.metadataFieldLabel.dc_identifier_uri+ td > a::text').extract()[0]
        
        _type = response.css('.table.itemDisplayTable tr:last-child td + td a').extract()[0]
        _type = _type.lower()
        itens["type"] = "Dissertação" if "mestrado" in _type else "Tese"

        yield itens