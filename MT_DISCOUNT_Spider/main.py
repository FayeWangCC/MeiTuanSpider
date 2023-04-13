import json
import jsonpath
import requests


# 发送请求获取json数据
def get_json_data():
    # 设置JSON数据API接口
    json_api = 'https://waimaieapp.meituan.com/reuse/activity/setting/r/getAllFoodActPolicy'

    # 读取txt文件获取负载数据
    with open('LodaData.txt', 'r', encoding='utf8') as f:
        ua_data = f.readline().strip('\n')
        cookie_data = f.readline().strip('\n')
        wmPoiId_data = f.readline().strip('\n')
        wmActPoiId_data = f.readline().strip('\n')

    # 设置请求头
    headers = {
        'User-Agent': ua_data,
        'Cookie': cookie_data
    }

    # 设置post请求参数
    data = {
        'status': '0',
        'startTime': '',
        'endTime': '',
        'itemName': '',
        'wmPoiId': wmPoiId_data,
        'wmActPoiId': wmActPoiId_data,
        'dataSource': '1',
        'wmActPolicyId': '1001'
    }

    # 发送请求获取json数据
    resp = requests.post(json_api, headers=headers, data=data)
    # 获取相应数据
    resp_data = resp.text
    # 返回获取的数据
    return resp_data


# 解析json数据
def parse_json_data(resp_data):
    # 加载json数据
    json_data = json.loads(resp_data)
    # 解析json格式数据
    data = jsonpath.jsonpath(json_data, '$..data')[0]
    print("%12s" % '商品编码', "%12s" % '商品原价', "%12s" % '商品售价')
    for i in range(len(data)):
        # 获取sku_id
        wmSkuId = jsonpath.jsonpath(data[i], '$..wmSkuId')[0]

        # 获取商品售价
        charge = jsonpath.jsonpath(data[i], '$..charge')[0]
        charge_json = json.loads(charge)
        actPrice = charge_json['actPrice']

        # 获取商品原价
        originPrice = charge_json['originPrice']

        with open('discount.txt', 'a') as f:
            f.write('{:}\t{:}\t{:}\n'.format(wmSkuId, originPrice, actPrice))

if __name__ == '__main__':
    # 打开文件清除之前的内容
    with open('discount.txt', 'w') as w:
        w.close()

    # 获取json数据
    resp_data = get_json_data()

    # 解析数据，获取折扣详情
    parse_json_data(resp_data=resp_data)
