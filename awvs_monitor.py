# author:Soufaker
# time:2023/02/24
import requests,json,socket,sys,time
from time import strftime,gmtime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from datetime import datetime
from configparser import ConfigParser
import os

# 加载配置文件
cf = ConfigParser()
cf.read('./config/config.ini')
awvs_url= cf.get('awvs','awvs_url')
awvs_key = cf.get('awvs','awvs_key')
profile_id = cf.get('awvs','profile_id')
scan_time = cf.get('awvs','scan_time')
scan_count = cf.get('awvs','scan_count')
tag = cf.get('tag','weixin_tag')
webhook_key = cf.get('webhook','webhook_key')
webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+webhook_key  #漏洞结果，企业微信漏洞通知key
headers = {'Content-Type': 'application/json',"X-Auth": awvs_key}

def target_scan(url,target_id):
    try:
        data = {"target_id": target_id, "profile_id": profile_id, "incremental": False,
                "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
        response = requests.post(awvs_url + '/api/v1/scans', data=json.dumps(data), headers=headers, timeout=30, verify=False)
        if 'profile_id' in str(response.text) and 'target_id' in str(response.text):
            print(target_id,'添加到AWVS扫描成功',url,str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        print('扫描出错了',e)
        return False


def add_target(add_list1,description='AUTO'):
    global temp_sum,temp_high_vul,temp_medium_vul,temp_low_vul
    try:
        target_id_list = []
        for url in add_list1:
            if '_' not in url:
                post_data = {"targets": [{"address": url.strip(), "description": description}], "groups": []}
                add_log = requests.post(awvs_url + '/api/v1/targets/add', data=json.dumps(post_data), headers=headers,
                                        timeout=20, verify=False)
                target_id = json.loads(add_log.content.decode())
                target_id_list.append(target_id)
        while len(target_id_list) != 0:
            #打印目前的漏洞狀態
            vul_sum,new_high_vul,new_medium_vul,new_low_vul,result,message_push_all = first_push()
            print('目前漏洞总数为',vul_sum)
            print('目前临时存储总数为',temp_sum)
            if int(vul_sum) > int(temp_sum) and len(result) != 0:
                current_date = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                message_push = str(socket.gethostname()) + '\n' + current_date + '\n'
                new_low = new_low_vul - temp_low_vul
                new_medium = new_medium_vul - temp_medium_vul
                new_high = new_high_vul - temp_high_vul
                new_sum = vul_sum - temp_sum
                if new_sum > 30:
                    message_push = message_push + '亲爱的主人,本次'+tag+'新增加漏洞数量为:'+str(new_sum)+'\n'+'新增加高危数量:'+str(new_high)+'\n'+'新增加中危数量:'+str(new_medium)+'\n'+\
                                   '新增加低危数量:'+str(new_low)+'\n'+'--------------------------\n'+message_push_all
                    temp_sum = vul_sum
                    temp_high_vul = new_high_vul
                    temp_medium_vul = new_medium_vul
                    temp_low_vul = new_low_vul
                    print(message_push)
                    message_length = int(len(message_push))
                    print('消息长度',message_length)
                    try:
                        push_wechat_group(message_push)
                    except:
                        try:
                            print('xxxxxxxxxxxxx12121')
                            mid = int(len(message_push)) // 2
                            push_wechat_group(message_push[0:mid])
                            push_wechat_group(message_push[mid:])
                        except:
                            print('xxxxxxxxxxxxx12121')
                            mid = int(len(message_push)) // 3
                            push_wechat_group(message_push[0:mid])
                            push_wechat_group(message_push[mid:mid+mid])
                            push_wechat_group(message_push[mid+mid:])

                    #push_wechat_group(message_push_all)

            #状态检测看看有没有超出扫描限制
            stats_result = requests.get(url=awvs_url + "/api/v1/me/stats", headers=headers, verify=False)
            scan_num = stats_result.json().get("scans_running_count")
            if int(scan_num) < int(scan_count):
                monitor_time_scans()
                add_url = add_list1.pop(0)
                if '_' not in add_url:
                    target_scan(add_url, target_id_list.pop(0)['targets'][0]['target_id'])
                    # 将已经扫描的数据丢入缓存
                    caches_file = open('./result/awvslist/cache.txt', 'a', encoding='utf-8')
                    caches_file.write(add_url + '\n')
                    caches_file.close()
                    time.sleep(10)
            else:
                print('当前运行的扫描任务数量已上限!')
                time.sleep(10)
                continue


    except Exception as e:
        print('配置出错了', e)
        return False



def push_wechat_group(content):
    global webhook_url
    # print('开始推送')
    # 这里修改为自己机器人的webhook地址
    resp = requests.post(webhook_url,
                         json={"msgtype": "markdown",
                               "markdown": {"content": content}})
    if 'invalid webhook url' in str(resp.text):
        print('企业微信key 无效,无法正常推送')
        sys.exit()
    if resp.json()["errcode"] != 0:
        raise ValueError("push wechat group failed, %s" % resp.text)
    # except Exception as e:
    #     print('webhook',e)

def first_push():
    init_high_count = 0
    init_medium_count = 0
    init_low_count = 0
    get_target_url = awvs_url + '/api/v1/vulnerability_types?l=100&q=status:open;severity:1,2,3;'
    r = requests.get(get_target_url, headers=headers, timeout=30, verify=False)
    result = json.loads(r.content.decode())
    if len(result) != 0:
        for r in result['vulnerability_types']:
            if str(r['severity']) == '1':
                init_low_count = int(init_low_count) + int(r['count'])
            elif str(r['severity']) == '2':
                init_medium_count = int(init_medium_count) + int(r['count'])
            else:
                init_high_count = int(init_high_count) + int(r['count'])
    vul_sum = init_low_count + init_medium_count + init_high_count
    print('当前低危数量:', init_low_count)
    print('当前中危数量:', init_medium_count)
    print('当前高危数量:', init_high_count)
    print('漏洞总数:', vul_sum)
    message_push = '目前的全漏洞细节为'+'\n'
    for r in result['vulnerability_types']:
        if int(r['severity']) > 0 and 'SSL' not in r['name'] and 'TLS' not in r['name'] and 'SPDY' not in r['name'] and 'CORS' not in r['name'] and 'Cookie' not in r['name']:
            if int(r['severity']) == 1:
                level_vul = '低危'

            elif int(r['severity']) == 2:
                level_vul = '中危'
            else:
                level_vul = '高危'
            if 'SSL' not in r['name'] and 'TLS' not in r['name']:
                message_push = message_push + '漏洞等級: ' + level_vul + '漏洞: ' + r['name'] + '数量: ' + str(
                    r['count']) + '\n'
    print(message_push)

    return vul_sum,init_high_count,init_medium_count,init_low_count,result,message_push

def monitor_time_scans():
    resp = requests.get(awvs_url + "/api/v1/scans?l=100&q=status:processing;",headers=headers,verify=False)
    scan = json.loads(resp.content.decode())
    scan_list = scan['scans']
    print(scan_list)
    scan_dict = {}
    for scan in scan_list:
        try:
            status = scan['current_session']['status']
            scan_id = scan['scan_id']
            target_address = scan['target']['address']
            if status == 'processing':
                start_time = scan['current_session']['start_date'][0:-6]
                print('start_time',start_time)
                UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
                start_time = datetime.strptime(start_time, UTC_FORMAT)
                print('start2_time',start_time)
                now_time = datetime.utcnow()
                print('now_time',now_time)
                print('num',int(str(now_time - start_time).split(":")[0])+ int(str(now_time - start_time).split(":")[1]))
                is_time_out = int(str(now_time - start_time).split(":")[0])+ int(str(now_time - start_time).split(":")[1]) > int(int(scan_time) - 10)
                print(is_time_out)
                if is_time_out is True:
                    scan_dict[scan_id] = target_address
        except Exception as e:
                print("扫描至少10分钟以上才能停止", e)
    print(scan_dict)
    if int(len(scan_dict)) > 0:
        print('1111111111111111112')
        stop_scan(scan_dict)

def stop_scan(scan_dict):
    for key in scan_dict:
        try:
            resp = requests.post(awvs_url + "/api/v1/scans/{}/abort".format(key), headers=headers, timeout=30,
                                 verify=False)
            print(resp.text)
            if resp.status_code == 204:
                print("\n", scan_dict[key], " 扫描任务超过" + str(scan_time) + "，已中止扫描任务\n")
        except Exception as e:
            print("[*] 中止扫描任务时出现错误\n", e)

def get_url_list():
    add_real_list = []
    with open('./result/awvslist/all_av_list.txt', 'r') as f:
        url_list = f.readlines()
        for url in url_list:
            if url != '':
                add_url_list.append(url.strip('\n'))
        f.close()

    file_list = open('./result/awvslist/cache.txt', 'r', encoding='utf-8').read().split('\n')
    mid_list = set(file_list).intersection(set(add_url_list))
    add_list1 = set(mid_list).symmetric_difference(set(add_url_list))
    for add in add_list1:
        add_real_list.append(add)

    return add_real_list

def main():
    global add_url_list
    global temp_sum, temp_high_vul, temp_medium_vul, temp_low_vul
    add_url_list = []
    temp_sum,temp_high_vul,temp_medium_vul,temp_low_vul,result,message = first_push()
    while True:
        add_list1 = get_url_list()
        monitor_time_scans()
        time.sleep(0.1)
        try:
            if len(add_list1) != 0:
                print('开始添加')
                print(add_list1)
                add_target(add_list1,'auto_scan')
        except Exception as e:
            print('urL',e)
        time.sleep(3600)
main()