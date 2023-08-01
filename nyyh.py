"""
@Qim97 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
礼豫河南_V1.01  种植小麦，成熟可兑换20/50/100立减金，限制河南地区！
2023/8/1 updata 修复已知bug，增加答题抽奖功能
活动入口 https://s1.ax1x.com/2023/07/31/pP9gbXd.png 如果失效联系作者更换
抓https://nh.xfd365.com/api/取出cookie,token
默认助力作者 如果介意请停止使用该脚本
export nyyhtoken=cookie@token
多账号用'===='隔开 例 账号1====账号2
cron：0 0 10,20 * * ?
"""


import os

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取 nyyhtoken 环境变量值
accounts = os.getenv('nyyhtoken')

# 检查 nyyhtoken 是否存在
if accounts is None:
    print('你没有填入nyyhtoken，咋运行？')
else:
    # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
    accounts_list = os.environ.get('nyyhtoken').split('====')

    # 输出有几个账号
    num_of_accounts = len(accounts_list)
    print(f"获取到 {num_of_accounts} 个账号")

    # 遍历所有账号
    for i, account in enumerate(accounts_list, start=1):
        # 按@符号分割当前账号的不同参数
        values = account.split('@')
        cookie, token = values[0], values[1]
        # 输出当前正在执行的账号
        print(f"\n=======开始执行账号{i}=======")
        import time
        import requests


        print('================获取ID================')
        time.sleep(3)
        url = "https://nh.xfd365.com/api/wheat/user_wheat_info"

        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.6WK PSDType(1) mPaaSClient/8.2.1",
            "Cookie": cookie
        }

        data = {
            "token": token
        }

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        if response_data['errno'] == 0:
            # 获取并输出信息
            wheat_id = response_data['data']['id']
            growth_value = response_data['data']['growth_value']
            mature_num = response_data['data']['mature_num']
            user_score = response_data['data']['user_score']
            user_name = response_data['user_info']['user_name']

            print(f"ID: {user_name}---钢镚[{user_score}]")
            print(f"小麦ID: {wheat_id}")
            print(f"成熟所需成长值: {growth_value}/{mature_num}")

        else:
            print(f"获取ID失败")

        print('================开始签到================')
        url = "https://nh.xfd365.com/api/wheat/login_task_list"

        data = {
            "token": token,
        }

        response = requests.post(url, json=data, headers=headers)
        status = response.json()
        if status['errno'] == 0:
            task_id = status['today_login_num']
            time.sleep(3)
            url = "https://nh.xfd365.com/api/wheat/get_today_task"

            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.6WK PSDType(1) mPaaSClient/8.2.1",
                "Cookie": cookie
            }

            data = {
                "token": token,
                "wheat_user_id": wheat_id,
                "task_id": task_id
            }

            response = requests.post(url, json=data, headers=headers)
            status = response.json()
            errmsg = status['errmsg']  # 签到值
            if response.status_code == 200:
                print(errmsg)
            else:
                print(f"请求失败{status}")

        else:
            print("未获取到签到天数，❌❌❌❌❌")

        print("================获取任务列表================")
        time.sleep(3)
        # 请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.6WK PSDType(1) mPaaSClient/8.2.1",
            "Cookie": cookie
        }

        # 获取任务列表的请求
        url = "https://nh.xfd365.com/api/wheat/today_task_list"
        data = {
            "token": token,
            "page": 1,
            "size": 100
        }

        # 获取任务列表
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        if response_data['errno'] == 0:
            # 初始化一个列表来存放task_id
            task_id_list = []

            # 遍历每个任务，取出task_id并添加到列表中
            for task_data in response_data.get('data', []):
                task_id = task_data.get('task_id')
                task_id_list.append(task_id)
                # 领取任务
                url = "https://nh.xfd365.com/api/wheat/get_today_task"
                data = {
                    "token": token,
                    "wheat_user_id": wheat_id,
                    "task_id": task_id
                }
                response = requests.post(url, json=data, headers=headers)
                value = response.json()
                if value['errno'] == 0:
                    finished_id = value['finished_id']
                    print(f"领取任务成功---{task_id}")
                    # 完成任务
                    time.sleep(12)
                    url = "https://nh.xfd365.com/api/wheat/save_finish_browse_task"
                    data = {
                        "token": token,
                        "finished_id": finished_id
                    }
                    response = requests.post(url, json=data, headers=headers)
                    save_response = response.json()
                    if save_response['errno'] == 0:
                        errmsg = save_response['errmsg']
                        print(f"{errmsg}")
                    else:
                        print(f"完成任务失败---错误信息: {errmsg}")
                else:
                    print(f"领取任务失败---[{task_id}]  {value['errmsg']}")
                    time.sleep(3)

        url = "https://nh.xfd365.com/api/wheat/today_task_list"
        data = {
            "token": token,
            "page": 1,
            "size": 100
        }

        # 获取任务列表
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        non_zero_finished_ids = []

        # 遍历每个任务，检查finished_id是否不等于0
        for task_data in response_data.get('data', []):
            finished_id = task_data.get('finished_id')
            if finished_id != 0:
                non_zero_finished_ids.append(str(finished_id))
        # 检查是否存在未领取奖励的任务
        if len(non_zero_finished_ids) > 0:
            print("存在未领取的奖励---开始领取")
            for finished_id in non_zero_finished_ids:
                time.sleep(3)
                print(f"任务ID: {finished_id}")
                # 遍历非零的finished_id，完成任务
                for finished_id in non_zero_finished_ids:
                    url = "https://nh.xfd365.com/api/wheat/save_finish_browse_task"
                    data = {
                        "token": token,
                        "finished_id": int(finished_id)
                    }

                    response = requests.post(url, json=data, headers=headers)
                    save_response = response.json()
                    if save_response['errno'] == 0:
                        errmsg = save_response['errmsg']
                        print(f"完成任务成功---{errmsg}")
                    else:
                        errmsg = save_response['errmsg']
                        print(f"完成任务失败---错误信息: {errmsg}")


        else:
            print("所有任务奖励已领取完毕，退出。")

        print('================学堂答题================')
        for i in range(5):  # 循环运行5次
            time.sleep(3)

            url = "https://nh.xfd365.com/api/nhunion/get_jf_problem"

            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.6WK PSDType(1) mPaaSClient/8.2.1",
                "Cookie": cookie
            }

            data = {
                "token": token
            }
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            if response_data['errno'] == 0:
                question_data = response_data['data']  # 获取新的问题数据
                q_id = question_data['q_id']
                ta = question_data['ta']
                print(f"第{i + 1}题-{question_data}")

                answer_url = "https://nh.xfd365.com/api/nhunion/answer_jf_problem"
                answer_data = {
                    "token": token,
                    "q_id": q_id,
                    "user_ta": ta
                }
                time.sleep(3)

                # 发送回答问题的POST请求
                response = requests.post(answer_url, json=answer_data, headers=headers)
                answer_response_data = response.json()
                if answer_response_data['errno'] == 0:
                    score = answer_response_data['score']
                    print(f"{answer_response_data['errmsg']}---[{score}]积分")
                else:
                    print(f"Error: {answer_response_data}")
            else:
                print(f"{response_data['errmsg']}退出答题")
                break
        print("================开始施肥================")
        time.sleep(3)
        url = "https://nh.xfd365.com/api/wheat/my_friend_list"

        data = {
            "token": token,
        }

        response = requests.post(url, json=data, headers=headers)
        data = response.json()

        if data['errno'] == 0:
            found_f_id = None
            for item in data['data']:
                if item['user_name'] == '回家吃火锅':
                    found_f_id = item['f_id']
                    break

            # 判断是否找到'user_name'，并输出结果
            if found_f_id is not None:
                url = "https://nh.xfd365.com/api/wheat/fertilization_firend_wheat"

                headers = {
                    "Cookie": cookie,
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20D47 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.3WK PSDType(1) mPaaSClient/8.2.1"
                }

                data = {
                    "token": token,
                    "f_id": found_f_id
                }

                response = requests.post(url, json=data, headers=headers)
                print(response.json()['errmsg'])  # 打印响应内容
            else:
                print("❌❌❌❌❌，请与作者绑定好友关系后重试")
        else:
            print(f"❌❌❌❌❌{data}")
        print("================开始答题抽奖================")
        for i in range(2):
            time.sleep(3)
            url = "https://nh.xfd365.com/api/nhunion/get_draw_problem"

            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.6WK PSDType(1) mPaaSClient/8.2.1",
                "Cookie": cookie
            }

            data = {
                "token": token
            }

            response = requests.post(url, json=data, headers=headers)
            if response.json()['errno'] == 0:
                response_data = response.json()['data']
                q_id = response_data['q_id']

                print(response_data)  # 打印响应内容
                # 提交答案
                url = "https://nh.xfd365.com/api/nhunion/answer_draw_problem"
                data = {
                    "token": token,
                    "q_id": q_id,
                    "user_ta": 1
                }
                response_data = requests.post(url, json=data, headers=headers)
                response = response_data.json()
                time.sleep(3)
                if response["errmsg"] == "回答正确":
                    print(f"{response['errmsg']}")
                elif response["errmsg"] == "回答错误":
                    print('回答错误，尝试重新答题')
                    time.sleep(3)
                    data = {
                        "token": token,
                        "q_id": q_id,
                        "user_ta": 2
                    }
                    response_data = requests.post(url, json=data, headers=headers)
                    response = response_data.json()
                    if response["errmsg"] == "回答正确":
                        print(f"{response['errmsg']}")
                    else:
                        print(f"❌❌❌❌❌，{response}")
                else:
                    print(f"错误未知！！！{response}")

            else:
                print(f'{response.json()["errmsg"]},退出')
                break
        url = "https://nh.xfd365.com/api/nhunion/get_user_this_xfq_number"

        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 NebulaSDK/1.8.100112 Nebula Bankabc/Portal BankabciPhone/8.2.0 rv:8.2.1 iOS/16.6WK PSDType(1) mPaaSClient/8.2.1",
            "Cookie": cookie
        }

        data = {
            "token": token
        }

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        coupon_number_arr = response_data['coupon_number_arr']
        formatted_coupon_number = [str(num).zfill(6) for num in coupon_number_arr]
        print(f"获得抽奖号码：{formatted_coupon_number}")
        print(f"开奖时间：{response_data['open_day']}")
