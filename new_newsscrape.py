# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 12:40:11 2021

@author: gu zhongxiang
"""
from nonebot import on_command
import asyncio
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GROUP, Bot, GroupMessageEvent
import requests
from lxml import etree

news = on_command('最新公告', aliases={'公告'}, permission=GROUP, priority=98, block=True)


@news.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    def scrapnewsinfo(url):
        response = requests.get(url)
        text = response.text
        return etree.HTML(text)

    def parse_one_page(html1):
        result = html1.xpath("//dd/a/@href")
        return result

    def parse_one_page_text(html1):
        result = html1.xpath("//dd/a/p[@class='press-name']/text()")
        return result

    parsed = parse_one_page(scrapnewsinfo('http://sanguosha.com'))
    parsed_text = parse_one_page_text(scrapnewsinfo('http://sanguosha.com'))
    for i in range(0, len(parsed)):
        if parsed_text[i].startswith('[十周年]'):
            hyperlink = parse_one_page(scrapnewsinfo('http://sanguosha.com'))[i]
            break
        else:
            continue
    if hyperlink.startswith('http') == 1:
        await news.send(hyperlink)
    else:
        await news.send('http://www.sanguosha.com' + hyperlink)
