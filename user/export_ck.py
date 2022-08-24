#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件  :   export_ck.py
@时间  :   2022/06/15 15:42:20
@作者  :   依古比古
@说明  :   jbot插件导出ck
@版本  :   1.0
'''

# here put the import lib
# 引入库文件，基于telethon
from telethon import events
# 从上级目录引入 jdbot,chat_id变量
from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from ..diy.utils import read, write
# from .login import user
from .. import jdbot, user
import time,re,requests,asyncio,os
# 格式基本固定，本例子表示从chat_id处接收到包含hello消息后，要做的事情
@user.on(events.NewMessage(pattern=r'^导出ck$',outgoing=True))
# 定义自己的函数名称
async def export_ck(event):
    cmdtext="task /ql/scripts/write_ck.py now"        
    p = await asyncio.create_subprocess_shell(
    cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    res_bytes, res_err = await p.communicate()
    res = res_bytes.decode('utf-8') 
    msglog = await event.edit(f'CK导出脚本日志\n{res}')

    SENDER = event.sender_id
    async with jdbot.conversation(SENDER, timeout=60) as conv:
        await conv.send_message('小八嘎，请查收CK导出文件',file='/ql/scripts/cklist.txt')
        
    msg = await user.send_message(event.chat_id,'小八嘎们，CK导出文件已通过机器人私发给您，请注意查收！')    

     
