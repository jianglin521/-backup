"""
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
希望云社区_V1.0  签到,抽奖 如需完成刷人头奖励联系 https://t.me/qianmo98
抓https://xwyapi.newhope.cn/customer/score/detailUser?customerId=xxxxxx 取出customerId,Authorization

export xwytoken=Authorization@customerId
多账号用'===='隔开 例 账号1====账号2
corn：0 0 3,17 * * ?
"""

key = ""  # 企业微信推送 webhook 后面的 key

##########################################################源码区域，非维护勿动##########################################################

import json
import os
import time

import requests
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取 xwytoken 环境变量值
accounts = os.getenv('xwytoken')

# 检查 xwytoken 是否存在
if accounts is None:
    print('你没有填入xwytoken，咋运行？')
else:
    # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
    accounts_list = os.environ.get('xwytoken').split('====')

    # 输出有几个账号
    num_of_accounts = len(accounts_list)
    print(f"获取到 {num_of_accounts} 个账号")

    # 遍历所有账号
    for i, account in enumerate(accounts_list, start=1):
        # 按@符号分割当前账号的不同参数
        values = account.split('@')
        xwytoken, customerId = values[0], values[1]
        # 输出当前正在执行的账号
        print(f"\n=======开始执行账号{i}=======")
        time.sleep(2)
        url = "https://xwyapi.newhope.cn/customer/score/detailUser"

        params = {
            "customerId": customerId
        }

        headers = {
            "Authorization": xwytoken,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002732) NetType/4G Language/zh_CN",
        }

        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        # 处理响应结果
        if response.status_code == 200:
            if response_data["status"]:
                mobile = response_data["body"]["mobile"]
                receive_score = response_data["body"]["receiveScore"]
                print(f"ID:{mobile}\nReceive Score: {receive_score}")
            else:
                print("请求失败")

        else:
            print("请求失败")
            print(response.text)

        print("=======开始签到=======")
        time.sleep(2)
        url = "https://xwyapi.newhope.cn/customer/score/pointsIssuance"
        data = {
            "action": "fixedSignIn",
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200:
            status = response_data["status"]
            integral = response_data["body"]["integral"]
            if status == True:
                print(f"签到成功-----[{integral}]积分")
            else:
                print(f"签到失败，错误未知{response_data}")
        else:
            print("请求失败")
            print(response.text)

        print("=======开始抽奖=======")
        time.sleep(2)

        url = "https://xwyapi.newhope.cn/xwh-mall/xwhTurntableLottery/findTurntableTitle"

        response = requests.get(url, headers=headers)
        data = response.json()
        # 创建一个新字典，用于存放提取的数据
        result_dict = {}  # 字典数据

        # 遍历settingList列表
        for item in data['body']['settingList']:
            # 取出setKey，setVal和title并放入新字典
            set_key = item['setKey']
            set_val = item['setVal']
            title = item['title']

            result_dict[set_key] = {
                'setVal': set_val,
                'title': title
            }
        if data["body"]["remain"] == 3:
            print("当前可免费抽奖1次--执行")
            url = 'https://xwyapi.newhope.cn/xwh-mall/xwhTurntableLottery/draw'
            response = requests.get(url, headers=headers)
            response_data = response.json()
            if data['message'] == "操作成功":
                setKey = response_data['body']['setKey']
                if setKey in result_dict:
                    set_val = result_dict[setKey]['setVal']
                    title = result_dict[setKey]['title']
                    print(f"抽奖获得---[{set_val}]{title}")
                else:
                    print(f"错误{setKey}")
            else:
                print(f"抽奖失败，错误未知{data}")

        else:
            print("当前无免费抽奖次数--退出")

        if key == "":
            print("key为空不执行推送")
        else:
            # 推送
            # 企业微信机器人Webhook地址
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key

            # 需要推送的消息内容
            messages = [
                f"===希望云社区_账号{i}===\nID:{mobile}\nReceive Score: {receive_score}\n@Qim_9797",
            ]

            # 循环遍历消息列表，依次执行消息推送操作
            for message in messages:
                # 拼接请求体
                data = {
                    "msgtype": "text",
                    "text": {
                        "content": message
                    }
                }
                headers = {'Content-Type': 'application/json'}

                # 发送POST请求
                response = requests.post(url, headers=headers, data=json.dumps(data))

                # 打印响应结果
                print(response.text)
