# -*- coding: utf-8 -*-
import scrapy
from ..items import UfpeItem
import re
from html import unescape


class UfpeSpider(scrapy.Spider):
    name = 'ufpb'
    start_urls = [
        'https://repositorio.ufpb.br/jspui/simple-search?location=&query=saude+mental']

    def parse(self, response):
        links = response.css('td:nth-child(2) a::attr(href)').extract()
        next_page = response.css(
            '.pagination li:last-child a::attr(href)').get()
        for link in links:
            yield response.follow(link, self.parse_article)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        itens = UfpeItem()
        content = unescape(response.body.decode("utf-8")).replace("\xa0", " ")

        regex_title = re.compile(
            'Title: </td><td class=\"metadataFieldValue\">([^<]+)')
        regex_author = re.compile(
            'metadata.dc.creator: </td><td class=\"metadataFieldValue\">(?:<\s*a[^>]*>(.*),(.*)<\s*/\s*a>)')
        regex_keywords = re.compile(
            'Keywords: </td><td class=\"metadataFieldValue\">(.*)(?:</td>)')
        regex_date = re.compile(
            'Issue Date: </td><td class=\"metadataFieldValue\">([^<]+)')
        regex_abstract = re.compile(
            'metadata.dc.description.resumo: </td><td class=\"metadataFieldValue\">([^<]+)')
        regex_uri = re.compile(
            'URI: </td><td class=\"metadataFieldValue\">(?:<\s*a[^>]*>(.*?)<\s*/\s*a>)')
        regex_type = re.compile(
            'program:\s?</td><td class=\"metadataFieldValue\">(?:<\s*a[^>]*>)(.*)</a>')

        title = regex_title.search(content)
        author = regex_author.search(content)
        keywords = regex_keywords.search(content)
        date = regex_date.search(content)
        abstract = regex_abstract.search(content)
        uri = regex_uri.search(content)
        _type = regex_type.search(content)

        itens["title"] = title.group(1) if title else None
        itens["author"] = f"{author.group(2).strip()} {author.group(1).capitalize()}" if author else None
        itens["keywords"] = [keyword.strip()
                             for keyword in keywords.group(1).split("<br />")] if keywords else None
        itens["date"] = date.group(1) if date else None
        itens["abstract"] = abstract.group(1) if abstract else None
        itens["uri"] = uri.group(1) if abstract else None
        itens["type"] = _type.group(1) if _type else None
        # itens["type"] = None

        yield itens