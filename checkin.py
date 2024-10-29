import requests
import json
import os

if __name__ == '__main__':
    # glados账号cookie 直接使用数组 如果使用环境变量需要字符串分割一下
    cookies = os.environ.get("COOKIES", []).split("&")
    if cookies[0] != "":
        success, fail, repeats = 0, 0, 0        # 成功账号数量 失败账号数量 重复签到账号数量

        check_in_url = "https://glados.space/api/user/checkin"        # 签到地址
        status_url = "https://glados.space/api/user/status"          # 查看账户状态

        referer = 'https://glados.space/console/checkin'
        origin = "https://glados.space"
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        payload = {
            'token': 'glados.one'
        }
        
        for cookie in cookies:
            checkin = requests.post(check_in_url, headers={'cookie': cookie, 'referer': referer, 'origin': origin,
                                    'user-agent': useragent, 'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
            state = requests.get(status_url, headers={
                                'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})
            
            if checkin.status_code == 200:
                # 解析返回的json数据
                result = checkin.json()     
                # 获取签到结果
                check_result = result.get('message')
                points = result.get('points')

                # 获取账号当前状态
                result = state.json()
                # 获取剩余时间
                leftdays = int(float(result['data']['leftDays']))
                # 获取账号email
                email = result['data']['email']
                
                print(f"账号: {email}")
                print(f"签到结果: {check_result}")
                print(f"获得点数: {points}")
                print(f"剩余天数: {leftdays}")
                print("-" * 50)

                if "Checkin! Got" in check_result:
                    success += 1
                elif "Checkin Repeats!" in check_result:
                    repeats += 1
                else:
                    fail += 1
            else:
                print("签到请求失败，请检查cookie是否有效")
                print("-" * 50)
                fail += 1

        print(f"签到统计 - 成功: {success}, 失败: {fail}, 重复: {repeats}")
    else:
        print("未找到 cookies!")
