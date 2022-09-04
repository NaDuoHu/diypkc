#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import random
import requests
import os, time
import re
import sys
import json
import datetime
from telethon import events
from os import listdir
# from .login import user
from .. import chat_id, jdbot, logger, TOKEN, user, jk, CONFIG_DIR, readJKfile, LOG_DIR
from ..bot.utils import cmd, V4
from ..diy.utils import rwcon, myzdjr_chatIds, my_chat_id
jk_version = 'v1.2.9'
from ..bot.update import version as jk_version
bot_id = int(TOKEN.split(":")[0])

@user.on(events.NewMessage(pattern=r'^wdz[ 0-9]*$', outgoing=True))
async def wdz(event):
    try:
        await event.delete()
        num = event.raw_text.split(' ')
        count = int(num[-1])
        for i in range(count):
           fake_id = ''.join(random.choice('abcdef0123456789') for _ in range(32))
           await user.send_message(event.chat_id, f'微定制：\n`jd_task_wdz_custom="{fake_id}"`')
    except Exception as e:
        await user.send_message(event.chat_id, str(e))
        
@user.on(events.NewMessage(pattern=r'^ip$', outgoing=True))       
async def ip(event):
    try:
        url1 = "https://ip.useragentinfo.com/json"
        data1 = requests.get(url1).json()
        r1 = data1["ip"]
        r1 =  re.findall(r"(?<=\d\.)\d{1,3}\.\d{1,3}(?!\d|\.)",r1)
        r1 = ''.join(r1)
        url2 = "http://myip.ipip.net/"
        data2 = requests.get(url2).text
        await event.edit(f'外网IP：`*.*.{r1}`\n`{data2}`')
    except Exception as e:
        await user.send_message(event.chat_id, str(e))    

@user.on(events.NewMessage(pattern=r'^删除去重$', outgoing=True))
async def delqc(event):
    try:
       v_today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
       path = f'{LOG_DIR}/bot/jk-{v_today}.txt'
       if os.path.exists(path):
           os.remove(path)
           await user.send_message(event.chat_id, f'已删除今日去重文件')
       else:
           await user.send_message(event.chat_id, f'今日去重文件不存在')
    except Exception as e:
        await user.send_message(event.chat_id, str(e))

@user.on(events.NewMessage(pattern=r'^删除所有去重$', outgoing=True))
async def delqc(event):
    try:
       path = f'{LOG_DIR}/bot/'
       for file_name in listdir(path):    
           if file_name.endswith('.txt'):
               os.remove(path + file_name)
               await user.send_message(event.chat_id, f'已删除所有去重文件')
    except Exception as e:
        await user.send_message(event.chat_id, str(e))

@user.on(events.NewMessage(pattern=r'^botlog'))
async def bot_run_log(event):
    '''定义日志文件操作'''
    await user.send_message(event.chat_id,'bot运行日志',file=f'{LOG_DIR}/bot/run.log')