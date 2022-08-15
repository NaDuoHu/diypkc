from telethon import events
##from .login import user
from .. import user
from .. import jdbot
from ..diy.utils import read, write
import re
import requests
@user.on(events.NewMessage(pattern=r'^jd', outgoing=True))
async def jcmd(event):
    try:
        reply = await event.get_reply_message()
        if reply:
            msg_text = reply.text
        else:
            msg_text = event.raw_text
            if len(msg_text) > 3:
                msg_text = msg_text[3:len(msg_text)]
            else:
                msg_text = None
    except ValueError:
        return await event.edit('未知错误')
    if not msg_text:
        return await event.edit('请指定要解析的口令,格式: jd 口令 或对口令直接回复jd ')
        
    data = requests.post("http://api.lolkda.top/jd/jKeyCommand",headers = {"content-type": "application/x-www-form-urlencoded;charset=utf-8",},data={"key": msg_text}).json()
    
    code = data.get("code")
    if code == 200:
        data = data["data"]
        title = data["title"]
        jump_url = data["jumpUrl"]
        activateId = re.findall("activityId=(.*?)&", data['jumpUrl'])
        lz = re.findall("(.*?)/wxTeam", data['jumpUrl'])
        wdz = re.findall("(.*?)/microDz", data['jumpUrl'])
        actId = re.findall("actId=(.*?)&", data['jumpUrl'])
        code = re.findall("code=(.*?)&", data['jumpUrl'])
        active = re.findall("active/(.*?)/", data['jumpUrl'])
        asid = re.findall("asid=(.*)", data['jumpUrl'])
        shopid = re.findall("shopid=(.*)", data['jumpUrl'])
        shareUuid = re.findall("shareUuid=(.*?)&", data['jumpUrl'])
        title = f'【活动名称】: {data["title"]}\n【分享来自】: {data["userName"]}\n【活动链接】: [点击跳转浏览器]({data["jumpUrl"]})\n【快捷跳转】: [点击跳转到京东](http://www.lolkda.top/?url={data["jumpUrl"]})'
        ## mark = f'\n   [MK2]({data["img"]})'
        
        ## 正常脚本
        if re.findall("https://cjhydz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KRCJ组队瓜分\n【活动变量】:\n`export jd_cjhy_activityId="{activateId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KRLZ组队瓜分\n【活动变量】:\n`export jd_zdjr_activityId="{activateId[0]}"`\n`export jd_zdjr_activityUrl="{lz[0]}"`'
            
        elif re.findall("https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index", data['jumpUrl']):
            msg = f'【脚本类型】: KR微定制瓜分\n【活动变量】:\n`export jd_wdz_activityId="{activateId[0]}"`\n`export jd_wdz_activityUrl="{wdz[0]}"`'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxgame/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ店铺游戏\n【活动变量】:\n`export WXGAME_ACT_ID="{activateId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxShareActivity", data['jumpUrl']):
            msg = f'【脚本类型】: KR分享有礼\n【活动变量】:\n`export jd_fxyl_activityId="{activateId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxSecond/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KR读秒拼手速\n【活动变量】:\n`export jd_wxSecond_activityId="{activateId[0]}"`'
            
        elif re.findall("https://jinggengjcq-isv.isvjcloud.com", data['jumpUrl']):
            msg = f'【脚本类型】: KR大牌联合开卡\n【活动变量】:\n`export DPLHTY="{actId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCollectCard/activity", data['jumpUrl']):
            msg = f'【脚本类型】: KR集卡抽奖\n【活动变量】:\n`export jd_wxCollectCard_activityId="{activateId[0]}"`'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/drawCenter/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ刮刮乐抽奖\n【活动变量】:\n`export jd_drawCenter_activityId="{activateId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxFansInterActionActivity/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 粉丝互动\n【活动变量】:\n`export jd_wxFansInterActionActivity_activityId="{activateId[0]}"`'
            
        elif re.findall("https://prodev.m.jd.com/mall/active", data['jumpUrl']):
            msg = f'【脚本类型】: KR邀好友赢大礼\n【脚本类型】: 船长邀好友赢大礼\n【活动变量】:\n`export yhyactivityId="{active[0]}"`\n`export yhyauthorCode="{code[0]}"`\n`export jd_inv_authorCode="{code[0]}"`'
            
        elif re.findall("https://lzkj-isv.isvjcloud.com/wxShopFollowActivity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ关注抽奖\n【活动变量】:\n`export jd_wxShopFollowActivity_activityId="{activateId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxUnPackingActivity/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 让福袋飞\n【活动变量】:\n`export jd_wxUnPackingActivity_activityId="{activateId[0]}"`'
            
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxCartKoi/cartkoi/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 购物车锦鲤\n【活动变量】:\n`export jd_wxCartKoi_activityId="{activateId[0]}"`'
            
        elif re.findall("https://happy.m.jd.com/babelDiy/zjyw", data['jumpUrl']):
            msg = f'【脚本类型】: 锦鲤红包\n【活动变量】:\n`锦鲤红包id="{asid[0]}"`'
            
        elif re.findall("https://cjhy-isv.isvjcloud.com/wxInviteActivity/openCard/invitee", data['jumpUrl']):
            msg = f'【脚本类型】: 入会开卡领取礼包\n【活动变量】:\n`export VENDER_ID="{shopid[0]}"`'
        
        ## 开卡解析
        elif re.findall("https://lzdz1-isv.isvjcloud.com/dingzhi/joinCommon/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 活动开卡\n【活动变量】:\n`activityId="{activateId[0]}"`\n`shareUuid="{shareUuid[0]}"`\n`ShopId="{shopid[0]}"`'
            
        elif re.findall("https://lzdz1-isv.isvjcloud.com/dingzhi/aug/brandUnion/activity", data['jumpUrl']):
            msg = f'【脚本类型】: 活动开卡\n【活动变量】:\n`activityId="{activateId[0]}"`\n`shareUuid="{shareUuid[0]}"`\n`ShopId="{shopid[0]}"`'
            
        else:
            msg = "【未适配变量】"
        await user.send_message(event.chat_id,title+"\n"+msg)
        if "脚本类型" in msg:
            await jdbot.send_message(-1001625033952,title+"\n"+msg)
    else:
        await user.send_message(event.chat_id,"解析出错")