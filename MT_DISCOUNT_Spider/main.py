import json

import jsonpath
import requests


# 发送请求获取json数据
def get_json_data():
	# 设置JSON数据API接口
	json_api = 'https://waimaieapp.meituan.com/reuse/activity/setting/r/getAllFoodActPolicy'

	# 设置请求头
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
		'Cookie': '__mta=247353659.1657697454603.1658214993800.1659510642519.6; uuid=acc4ca2aca3853b6459a.1657502638.1.0.0; wmPoiId=13727585; _source=PC; terminal=bizCenter; bizad_cityId=110105; bizad_second_city_id=110100; bizad_third_city_id=110105; wmPoiName=%E6%81%8B%E4%BA%BA%E9%B2%9C%E8%8A%B1%E5%BA%97%EF%BC%88%E7%8E%AB%E7%91%B0%E8%8A%B1.%E7%94%9F%E6%97%A5%E9%B2%9C%E8%8A%B1.%E5%BC%80%E4%B8%9A%E8%8A%B1%E7%AF%AE%EF%BC%89; lt=STjXCBh_0Sr4PUWZti18o8mKtZsAAAAAvRIAAIktymLmaJZ3cp2gAunxAbdDPu06I_VCzRrSexYUojT3UCLPxNa9Atg4VFCHIMHe9Q; mt_c_token=STjXCBh_0Sr4PUWZti18o8mKtZsAAAAAvRIAAIktymLmaJZ3cp2gAunxAbdDPu06I_VCzRrSexYUojT3UCLPxNa9Atg4VFCHIMHe9Q; userId=255996836; _lxsdk_cuid=18204a65014c8-0a3eca3bee889b-673b5753-1fa400-18204a65014c8; isChain=0; _lxsdk=18204a65014c8-0a3eca3bee889b-673b5753-1fa400-18204a65014c8; bmm-uuid=dcee728b-473f-0b62-2f5a-808e884f03aa; acctId=118075493; token=0WHj5ZtCXwPECsZWI8PwgbcC1Hn-gRypRuNNHgApm14U*; bsid=E-QkfhRAiUgdwA0tzTYIykSTPv42aBXPAeC673NuPjthq3bkyHmRIkqDDjwoRNVwpcDMBLM6yeGBaJsfNHyWxw; igateApp=recoanalysis; platform=0; logan_session_token=w2izv3j4zbfm1leefudl; logan_custom_report=%7B%22unionId%22%3A%2213727585%22%2C%22biz%22%3A%22waimai_ad_pc_vue%22%7D; JSESSIONID=node0sl4v0cdl7chc1iqyqwv1sj6g939306044.node0; _lxsdk_s=18280d4ed3a-124-13d-fe%7C%7C22'
	}

	# 设置post请求参数
	data = {
		'status': '0',
		'startTime': '',
		'endTime': '',
		'itemName': '',
		'wmPoiId': '13727585',
		'wmActPoiId': '6617266635',
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
	for i in range(len(data)):
		# 获取sku_id
		wmSkuId = jsonpath.jsonpath(data[i], '$..wmSkuId')[0]
		print(wmSkuId)

		# 获取商品售价
		charge = jsonpath.jsonpath(data[i], '$..charge')[0]
		charge_json = json.loads(charge)
		actPrice = charge_json['actPrice']
		# print(actPrice)

		# 获取商品原价
		originPrice = charge_json['originPrice']
		# print(originPrice)

if __name__ == '__main__':
	# 获取json数据
	resp_data = get_json_data()
	# 解析数据，获取折扣详情
	parse_json_data(resp_data=resp_data)
