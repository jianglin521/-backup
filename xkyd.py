"""
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
星空阅读_V1.1  入口：http://mr1694245841257.uznmvev.cn/ox/index.html?mid=CS5WX5RSP
抓包http://u.cocozx.cn/api/ox/info取出un token参数
export xktoken=un@token
多账号用'===='隔开 例 账号1====账号2
cron：23 7-23/2 * * *
"""

max_concurrency = 5  # 并发线程数
money_Withdrawal = 1  # 提现开关 1开启 0关闭
key = ""  # key为企业微信webhook机器人后面的 key

# 检测文章列表
biz_list = ['Mzg2Mzk3Mjk5NQ==']
















# from dotenv import load_dotenv
# load_dotenv()


import json
import os
import random
import re
import threading
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

import requests

lock = threading.Lock()



def process_account(account, i):
    values = account.split('@')
    un, token = values[0], values[1]

    print(f"\n=======开始执行账号{i}=======")

    url = "http://u.cocozx.cn/api/ox/info"

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.41(0x1800292d) NetType/WIFI Language/zh_CN",

    }

    data = {
        "code": "XG7QUVEEH",
        "un": un,
        "token": token,
        "pageSize": 20
    }

    response = requests.post(url, json=data, headers=headers).json()
    if response['code'] == 0:
        uid = response['result']['uid']
        moneyCurrent = response['result']['moneyCurrent']
        dayCount = response['result']['dayCount']
        print(f"[{uid}]---元子余额:{moneyCurrent}\n今日有效阅读------{dayCount}篇")
        url = "http://u.cocozx.cn/api/ox/getReadHost"
        response = requests.post(url, json=data, headers=headers).json()
        if response['code'] == 0:
            host = response.get('result').get('host')
            print(f"阅读链接:{host}")

            print(f"{'-' * 40}")

            for i in range(30):
                url = "http://u.cocozx.cn/api/ox/read"
                response = requests.post(url, json=data, headers=headers).json()
                if response['code'] == 0:
                    status = response.get('result').get('status')
                    if status == 10:
                        link = response['result']['url']
                        mid = link.split('&mid=')[1].split('&')[0]
                        biz = link.split('__biz=')[1].split('&')[0]
                        print(f"获取文章成功---{mid} 来源[{biz}]")
                        if biz in biz_list:
                            print(f"发现目标[{biz}] 疑似检测文章！！！")
                            link = response['result']['url']
                            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key

                            messages = [
                                f"出现检测文章！！！\n{link}\n请在60s内点击链接完成阅读",
                            ]

                            for message in messages:
                                data_bot = {
                                    "msgtype": "text",
                                    "text": {
                                        "content": message
                                    }
                                }
                                headers_bot = {'Content-Type': 'application/json'}
                                response = requests.post(url, headers=headers_bot, data=json.dumps(data_bot))
                                print("以将该文章推送至微信请在60s内点击链接完成阅读--60s后继续运行")
                                time.sleep(60)
                                url = "http://u.cocozx.cn/api/ox/submit"
                                response = requests.post(url, json=data, headers=headers).json()

                                if response.get('code') == 0:
                                    result = response.get('result')
                                    print(f'第{i + 1}次阅读检测文章成功---获得{result.get("val")}元子')
                                    progress = result.get('progress')
                                    if progress > 0:
                                        print(f'本轮剩余{progress}篇文章，继续阅读')
                                        print('-' * 50)
                                        time.sleep(2)
                                    else:
                                        print('阅读已完成')
                                        print('-' * 50)
                                        break
                                else:
                                    print('提交任务异常')

                        else:
                            sleep = random.randint(7, 9)
                            print(f"本次模拟阅读{sleep}秒")
                            time.sleep(sleep)
                            url = "http://u.cocozx.cn/api/ox/submit"
                            response = requests.post(url, json=data, headers=headers).json()

                            if response.get('code') == 0:
                                result = response.get('result')
                                print(f'第{i + 1}次阅读成功---获得{result.get("val")}元子')
                                progress = result.get('progress')
                                if progress > 0:
                                    print(f'本轮剩余{progress}篇文章，继续阅读')
                                    print('-' * 50)
                                    time.sleep(2)
                                else:
                                    print('阅读已完成')
                                    print('-' * 50)
                                    break
                            else:
                                print('提交任务异常')
                    elif status == 30:
                        print(f'未知情况{response}')
                    elif status == 50 or status == 80:
                        print('您的阅读暂时失效，请明天再来')
                        break
                    else:
                        print('本次推荐文章已全部读完')
                        break
                else:
                    print(f"获取文章失败{response}")
                    break

            if money_Withdrawal == 1:
                url = "http://u.cocozx.cn/api/ox/info"
                response = requests.post(url, json=data, headers=headers).json()
                if response['code'] == 0:
                    txm = 0
                    moneyCurrent = response['result']['moneyCurrent']
                    moneyCurrent = int(moneyCurrent)
                    if moneyCurrent < 3000:
                        print('没有达到提现标准')
                    elif 3000 <= moneyCurrent < 10000:
                        txm = 3000
                    elif 10000 <= moneyCurrent < 50000:
                        txm = 10000
                    elif 50000 <= moneyCurrent < 100000:
                        txm = 50000
                    else:
                        txm = 100000
                    url = "http://u.cocozx.cn/api/ox/wdmoney"
                    data = {"val": txm, "un": un, "token": token, "pageSize": 20}
                    response = requests.post(url, json=data, headers=headers).json()
                    print(f"提现结果:{response}")
            elif money_Withdrawal == 0:
                print(f"{'-' * 30}\n不执行提现")
        else:
            print(f"{response}")

    else:
        print(f"获取账号信息失败{response}")
        exit()


if __name__ == "__main__":
    accounts = os.getenv('xktoken')
    """
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
钢镚阅读阅读_V1.63   入口：http://2477726.lk.gbl.zn93ff8jyqd4.cloud/?p=2477726
阅读文章抓出cookie（找不到搜索gfsessionid关键词）
export ydtoken=cookie
多账号用'===='隔开 例 账号1====账号2
cron：23 7-23/3 * * *
"""

max_concurrency = 5  # 并发线程数
money_Withdrawal = 0  # 提现开关 1开启 0关闭
key = ""        #key为企业微信webhook机器人后面的 key








import re
import hashlib
import json
import os
import random

import threading
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import requests

lock = threading.Lock()


def process_account(account, i):
    values = account.split('@')
    cookie = values[0]

    print(f"\n=======开始执行账号{i}=======")
    current_time = str(int(time.time()))

    sign_str = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}'
    sha256_hash = hashlib.sha256(sign_str.encode())
    sign = sha256_hash.hexdigest()
    url = "http://2477726.neavbkz.jweiyshi.r0ffky3twj.cloud/share"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; V1923A Build/PQ3B.190801.06161913; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/5635 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
        "Cookie": cookie
    }

    data = {
        "time": current_time,
        "sign": sign
    }

    with lock:
        response = requests.get(url, headers=headers, json=data).json()
        share_link = response['data']['share_link'][0]
        p_value = share_link.split('=')[1].split('&')[0]

        url = "http://2477726.neavbkz.jweiyshi.r0ffky3twj.cloud/read/info"

        response = requests.get(url, headers=headers, json=data).json()

        if response['code'] == 0:
            remain = response['data']['remain']
            read = response['data']['read']
            print(f"ID:{p_value}-----钢镚余额:{remain}\n今日阅读量::{read}\n推广链接:{share_link}")
        else:
            print(response['message'])

    print("============开始执行阅读文章============")

    for j in range(30):
        biz_list = ['MzkyMzI5NjgxMA==', 'MzkzMzI5NjQ3MA==', 'Mzg5NTU4MzEyNQ==', 'Mzg3NzY5Nzg0NQ==',
                    'MzU5OTgxNjg1Mg==', 'Mzg4OTY5Njg4Mw==', 'MzI1ODcwNTgzNA==','Mzg2NDY5NzU0Mw==']
        # 计算 sign
        sign_str = f'key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}'
        sha256_hash = hashlib.sha256(sign_str.encode())
        sign = sha256_hash.hexdigest()
        url = "http://2477726.9o.10r8cvn6b1.cloud/read/task"

        try:
            response = requests.get(url, headers=headers, json=data, timeout=7).json()
        except requests.Timeout:
            print("请求超时，尝试重新发送请求...")
            response = requests.get(url, headers=headers, json=data, timeout=7).json()
        if response['code'] == 1:
            print(response['message'])
            break
        else:
            try:
                mid = response['data']['link'].split('&mid=')[1].split('&')[0]
                biz = response['data']['link'].split('__biz=')[1].split('&')[0]

                print(f"[{p_value}]获取文章成功---{mid} 来源[{biz}]")

                if biz in biz_list:
                    print(f"发现目标[{biz}] 疑似检测文章！！！")
                    link = response['data']['link']
                    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key

                    messages = [
                        f"出现检测文章！！！\n{link}\n请在60s内点击链接完成阅读",
                    ]

                    for message in messages:
                        data = {
                            "msgtype": "text",
                            "text": {
                                "content": message
                            }
                        }
                        headers = {'Content-Type': 'application/json'}
                        response = requests.post(url, headers=headers, data=json.dumps(data))
                        print("以将该文章推送至微信请在60s内点击链接完成阅读--60s后继续运行")
                        time.sleep(60)
                        url = "http://2477726.9o.10r8cvn6b1.cloud/read/finish"
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Linux; Android 9; V1923A Build/PQ3B.190801.06161913; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/5635 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
                            "Cookie": cookie
                        }
                        data = {
                            "time": current_time,
                            "sign": sign
                        }
                        try:
                            response = requests.get(url, headers=headers, data=data, timeout=7).json()
                        except requests.Timeout:
                            print("请求超时，尝试重新发送请求...")
                            response = requests.get(url, headers=headers, data=data, timeout=7).json()
                        if response['code'] == 0:
                            gain = response['data']['gain']
                            print(f"第{j + 1}次阅读检测文章成功---获得钢镚[{gain}]")
                            print(f"--------------------------------")
                        else:
                            print(f"过检测失败，请尝试重新运行")
                            break
                else:
                    sleep = random.randint(8, 11)
                    print(f"本次模拟阅读{sleep}秒")
                    time.sleep(sleep)
                    url = "http://2477726.9o.10r8cvn6b1.cloud/read/finish"
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Linux; Android 9; V1923A Build/PQ3B.190801.06161913; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/5635 MicroMessenger/8.0.40.2420(0x28002837) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
                        "Cookie": cookie
                    }
                    data = {
                        "time": current_time,
                        "sign": sign
                    }
                    try:
                        response = requests.get(url, headers=headers, data=data, timeout=7).json()
                    except requests.Timeout:
                        print("请求超时，尝试重新发送请求...")
                        response = requests.get(url, headers=headers, data=data, timeout=7).json()
                    if response['code'] == 0:
                        gain = response['data']['gain']
                        print(f"第{j + 1}次阅读文章成功---获得钢镚[{gain}]")
                        print(f"--------------------------------")
                    else:
                        print(f"阅读文章失败{response}")
                        break
            except KeyError:
                print(f"获取文章失败,错误未知{response}")
                break
    if money_Withdrawal == 1:
        print(f"============开始微信提现============")
        url = "http://2477726.84.8agakd6cqn.cloud/withdraw/wechat"

        response = requests.get(url, headers=headers, json=data).json()
        if response['code'] == 0:
            print(response['message'])
        elif response['code'] == 1:
            print(response['message'])
        else:
            print(f"错误未知{response}")
    elif money_Withdrawal == 0:
        print(f"{'-' * 30}\n不执行提现")


if __name__ == "__main__":
    accounts = os.getenv('ydtoken')
    response = requests.get('https://gitee.com/shallow-a/qim9898/raw/master/label.txt').text
    print(response)
    if accounts is None:
        print('你没有填入ydtoken，咋运行？')
    else:
        accounts_list = os.environ.get('ydtoken').split('====')
        num_of_accounts = len(accounts_list)
        print(f"获取到 {num_of_accounts} 个账号")
        with Pool(processes=num_of_accounts) as pool:
            thread_pool = ThreadPool(max_concurrency)
            thread_pool.starmap(process_account, [(account, i) for i, account in enumerate(accounts_list, start=1)])

    if accounts is None:
        print('你没有填入xktoken，咋运行？')
    else:
        accounts_list = os.environ.get('xktoken').split('====')
        num_of_accounts = len(accounts_list)
        print(f"获取到 {num_of_accounts} 个账号")
        with Pool(processes=num_of_accounts) as pool:
            thread_pool = ThreadPool(max_concurrency)
            thread_pool.starmap(process_account, [(account, i) for i, account in enumerate(accounts_list, start=1)])
