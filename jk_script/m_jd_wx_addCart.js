/*
M加购有礼

环境变量
M_WX_ADD_CART_URL  活动链接

即时任务，无需cron

*/

let mode = __dirname.includes('magic')
const {Env} = mode ? require('./magic') : require('./magic')
const $ = new Env('M加购有礼');
$.whitelist = process.env.M_WX_WHITELIST
    ? process.env.M_WX_WHITELIST
    : '1-5';
$.activityUrl = process.env.M_WX_ADD_CART_URL
    ? process.env.M_WX_ADD_CART_URL
    : '';
if (mode) {
    $.activityUrl = ''
}
$.activityUrl = $.match(
    /(https?:\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])/,
    $.activityUrl)
$.domain = $.match(/https?:\/\/([^/]+)/, $.activityUrl)
$.activityId = $.getQueryString($.activityUrl, 'activityId')
$.activityContent = ''
console.log(`活动入口: ${$.activityUrl}`);
$.logic = async function () {
    if (!$.activityId || !$.activityUrl) {
        $.expire = true;
        $.putMsg(`activityId|activityUrl不存在`);
        return
    }
    $.UA = $.ua();

    let token = await $.isvObfuscator();
    if (token.code !== '0') {
        $.putMsg(`获取Token失败`);
        return
    }
    $.Token = token?.token

    let actInfo = await $.api('customer/getSimpleActInfoVo',
        `activityId=${$.activityId}`);
    if (!actInfo.result) {
        $.expire = true;
        $.putMsg(`获取活动信息失败`);
        return
    }
    $.venderId = actInfo.data.venderId;
    $.shopId = actInfo.data.shopId;
    $.activityType = actInfo.data.activityType;

    let myPing = await $.api('customer/getMyPing',
        `userId=${$.venderId}&token=${$.Token}&fromType=APP`)
    if (!myPing.result) {
        $.putMsg(`获取pin失败`);
        return
    }
    $.Pin = $.domain.includes('cjhy') ? encodeURIComponent(
        encodeURIComponent(myPing.data.secretPin)) : encodeURIComponent(
        myPing.data.secretPin);

    await $.api(
        `common/${$.domain.includes('cjhy') ? 'accessLog' : 'accessLogWithAD'}`,
        `venderId=${$.venderId}&code=${$.activityType}&pin=${$.Pin}&activityId=${$.activityId}&pageUrl=${encodeURIComponent(
            $.activityUrl)}&subType=app&adSource=`);
    let activityContent = await $.api('wxCollectionActivity/activityContent',
        `activityId=${$.activityId}&pin=${$.Pin}`);

    if (!activityContent.result || !activityContent.data) {
        $.putMsg(activityContent.errorMessage || '活动可能已结束')
        return
    }

    $.activityContent = activityContent;
    let content = activityContent.data;
    if (![6, 7, 9, 13, 14, 15, 16].includes(
        activityContent.data.drawInfo.drawInfoType)) {
        $.putMsg(`垃圾活动不跑了`)
        $.expire = true
        return
    }
    if (1 > 2) {
        let memberInfo = await $.api($.domain.includes('cjhy')
            ? 'mc/new/brandCard/common/shopAndBrand/getOpenCardInfo'
            : 'wxCommonInfo/getActMemberInfo',
            $.domain.includes('cjhy')
                ? `venderId=${$.venderId}&buyerPin=${$.Pin}&activityType=${$.activityType}`
                :
                `venderId=${$.venderId}&activityId=${$.activityId}&pin=${$.Pin}`);
        // 没开卡需要开卡
        if ($.domain.includes('cjhy')) {
            if (memberInfo.result && !memberInfo.data?.openCard
                && memberInfo.data?.openCardLink) {
                $.putMsg('活动仅限店铺会员参与哦~')
                return
            }
        } else {
            if (memberInfo.result && !memberInfo.data?.openCard
                && memberInfo.data?.actMemberStatus === 1) {
                $.putMsg('活动仅限店铺会员参与哦~')
                return
            }
        }
        await $.api('wxActionCommon/getUserInfo', `pin=${$.Pin}`)
        if (content.needFollow && !content.hasFollow) {
            let followShop = await $.api(`wxActionCommon/followShop`,
                `userId=${$.venderId}&activityId=${$.activityId}&buyerNick=${$.Pin}&activityType=${$.activityType}`);
            await $.wait(1300, 1500)
            if (!followShop.result) {
                $.putMsg(followShop.errorMessage)
                return;
            }
        }
    }

    let needCollectionSize = content.needCollectionSize || 1;
    let hasCollectionSize = content.hasCollectionSize;
    let oneKeyAddCart = content.oneKeyAddCart * 1 === 1;
    //$.log('drawInfo', JSON.stringify(content.drawInfo));
    if (hasCollectionSize < needCollectionSize) {
        let productIds = [];
        a:for (let cpvo of content.cpvos) {
            if (oneKeyAddCart) {
                productIds.push(cpvo.skuId)
                continue
            }
            for (let i = 0; i < 5; i++) {
                try {
                    let carInfo = await $.api(`wxCollectionActivity/addCart`,
                        `activityId=${$.activityId}&pin=${$.Pin}&productId=${cpvo.skuId}`)
                    if (carInfo.result) {
                        if (carInfo.data.hasAddCartSize >= needCollectionSize) {
                            $.log(`加购完成，本次加购${carInfo.data.hasAddCartSize}个商品`)
                            break a
                        }
                        break;
                    } else {
                        await $.wxStop(carInfo.errorMessage) ? $.expire = true
                            : ''
                        $.putMsg(`${carInfo.errorMessage || '未知'}`);
                        break a
                    }
                } catch (e) {
                    $.log(e)
                } finally {
                    await $.wait(1300, 1500)
                }
            }
        }
        if (oneKeyAddCart) {
            let carInfo = await $.api('wxCollectionActivity/oneKeyAddCart',
                `activityId=${$.activityId}&pin=${$.Pin}&productIds=${encodeURIComponent(
                    JSON.stringify(productIds))}`)
            if (carInfo.result && carInfo.data) {
                $.log(`加购完成，本次加购${carInfo.data.hasAddCartSize}个商品`)
            } else {
                await $.wxStop(carInfo.errorMessage) ? $.expire = true : ''
                $.putMsg(`${carInfo.errorMessage || '未知'}`);
                return
            }
        }
    }
    if ($.expire) {
        return
    }
    let prize = await $.api('wxCollectionActivity/getPrize',
        `activityId=${$.activityId}&pin=${$.Pin}`);
    if (prize.result) {
        let msg = prize.data.drawOk ? prize.data.name : prize.data.errorMessage
            || '空气💨';
        await $.wxStop(prize.data.errorMessage) ? $.expire = true : ''
        $.putMsg(msg);
    } else {
        await $.wxStop(prize.errorMessage) ? $.expire = true : ''
        $.putMsg(`${prize.errorMessage || '未知'}`);
    }
    //await $.unfollow()
}
$.after = async function () {
    // $.msg.push(`\n${(await $.getShopInfo()).shopName}`)
    // $.msg.push(
    //     `\n加购${$.activityContent?.data?.needCollectionSize}件,${$.activityContent.data.drawInfo?.name
    //     || ''}\n`);
    // $.msg.push($.activityUrl)
}
$.run({whitelist: [$.whitelist], wait: [3000, 5000], sendON: 'false'}).catch(
    reason => $.log(reason));
