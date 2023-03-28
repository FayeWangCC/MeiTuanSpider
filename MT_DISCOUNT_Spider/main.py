import json
import jsonpath
import requests


# 发送请求获取json数据
def get_json_data():
    # 设置JSON数据API接口
    json_api = 'https://waimaieapp.meituan.com/reuse/activity/setting/r/getAllFoodActPolicy'

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Cookie': '__mta=247185339.1679289503788.1679891372030.1679891521509.4; _lxsdk_cuid=186ee3527ccc8-0123675bd25401-26031851-1fa400-186ee3527ccc8; acctId=126621366; _source=PC; virtual=0; vacctId=0; acctName=null; device_uuid=!0739735c-9483-4c41-a843-dd56f5f2e607; terminal=bizCenter; WEBDFPID=96zw8x9vuux95u31yv0x5163703y6y0v813vv4xzu8997958uz0x203v-1994396297449-1679036297255AYYMWICfd79fef3d01d5e9aadc18ccd4d0c95074223; bmm-uuid=fcc150d0-1f1e-9da5-6d6a-a497cf7c8e62; token=0iaKnw1QEq5zzGFFa-GlB4xeJdxAFugf7nd95QfvW9Ao*; bsid=Np-fQgWErRApDIVxzIrzFUE_5SIujVRFUS-lv8GAj7qb212b5kE18OJO5WyRv__CpassCBBYM_8rAR0BSG6gDw; uuid=820b2dbc7f871c2176dd.1679386053.1.0.0; _lxsdk=C7721A10C48D11EDBC5F1D40F7C070E3B0A91A74CC354FA1A3F23927F5F83F77; qruuid=3e1ea83f-2874-4312-a1d4-f78d73c8479b; token2=AgF1IYDdwrJ13znwDOq85UFZ7fSHGgG9l_6AZ5TrSs_nhPe2QGeXkAP_wb2HqiuBGlcDzZGIe6tR_wAAAABsFwAAGgctLJ0K2fGUfnLHJnU0yavVfXQnvynjvGtZexbdlesohyMw0zmUHaEWoCmPobTb; oops=AgF1IYDdwrJ13znwDOq85UFZ7fSHGgG9l_6AZ5TrSs_nhPe2QGeXkAP_wb2HqiuBGlcDzZGIe6tR_wAAAABsFwAAGgctLJ0K2fGUfnLHJnU0yavVfXQnvynjvGtZexbdlesohyMw0zmUHaEWoCmPobTb; lt=AgF1IYDdwrJ13znwDOq85UFZ7fSHGgG9l_6AZ5TrSs_nhPe2QGeXkAP_wb2HqiuBGlcDzZGIe6tR_wAAAABsFwAAGgctLJ0K2fGUfnLHJnU0yavVfXQnvynjvGtZexbdlesohyMw0zmUHaEWoCmPobTb; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; wmPoiName=%E6%81%8B%E4%BA%BA%E9%B2%9C%E8%8A%B1%E5%BA%97%EF%BC%88%E7%8E%AB%E7%91%B0%E8%8A%B1.%E7%94%9F%E6%97%A5%E9%B2%9C%E8%8A%B1.%E5%BC%80%E4%B8%9A%E8%8A%B1%E7%AF%AE%EF%BC%89; igateApp=recoanalysis; platform=0; bizad_cityId=420100; bizad_second_city_id=420100; bizad_third_city_id=420104; logan_session_token=abbjgl2pfl9vhbuakl7r; logan_custom_report=%7B%22unionId%22%3A%2215548542%22%2C%22biz%22%3A%22waimai_ad_pc_vue%22%7D; JSESSIONID=node07svr9i3x1cjooi3ns8h9manp13165201.node0; wmPoiId=15548542; _lxsdk_s=1872769f5b8-54b-e79-a5f%7C%7C2'
    }

    # 设置post请求参数
    data = {
        'status': '0',
        'startTime': '',
        'endTime': '',
        'itemName': '',
        'wmPoiId': '15548542',
        'wmActPoiId': '8776815241',
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

        print("%12s" % wmSkuId, "%12s" % originPrice, "%12s" % actPrice)


if __name__ == '__main__':
    # 获取json数据
    resp_data = get_json_data()
    # 解析数据，获取折扣详情
    parse_json_data(resp_data=resp_data)
