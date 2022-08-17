import requests

# 设置请求头
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
	'Host': 'waimaieapp.meituan.com',
	'Origin': 'https://waimaieapp.meituan.com',
	'Referer': 'https://waimaieapp.meituan.com/igate/recoanalysis/dist/pc?_source=PC&token=0CQ7oLkUVH_jVTqgK0-8ycCeQazfOicwweWCQSyP10Vg*&acctId=118075493&wmPoiId=13727585&region_id=1000110100&bsid=nszDEUxDyQg-09cbObjpUdeOWlA-neZCDAev9PBjEje_APlwWccYLSWAzPQADMjt-kCjueKU3XZf4yN4E4yg2A&appType=3&fromPoiChange=false',
	'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"macOS"',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-origin',
	'Cookie': 'uuid=9d90a64e1dde1954dec6.1657756390.1.0.0; _lxsdk_cuid=181f9fb16ffc8-0c67b775ac40af-51500a11-1aeaa0-181f9fb16ffc8; _lxsdk=181f9fb16ffc8-0c67b775ac40af-51500a11-1aeaa0-181f9fb16ffc8; bizad_cityId=110105; bizad_second_city_id=110100; bizad_third_city_id=110105; wmPoiName=%E6%81%8B%E4%BA%BA%E9%B2%9C%E8%8A%B1%E5%BA%97%EF%BC%88%E7%8E%AB%E7%91%B0%E8%8A%B1.%E7%94%9F%E6%97%A5%E9%B2%9C%E8%8A%B1.%E5%BC%80%E4%B8%9A%E8%8A%B1%E7%AF%AE%EF%BC%89; terminal=bizCenter; bmm-uuid=f46d1291-6aa3-e2cc-3aa8-e11913354732; acctId=118075493; wmPoiId=13727585; _source=PC; virtual=0; vacctId=0; acctName=null; token=0CQ7oLkUVH_jVTqgK0-8ycCeQazfOicwweWCQSyP10Vg*; bsid=nszDEUxDyQg-09cbObjpUdeOWlA-neZCDAev9PBjEje_APlwWccYLSWAzPQADMjt-kCjueKU3XZf4yN4E4yg2A; igateApp=recoanalysis; platform=0; logan_session_token=4za3992g9sgfwu1h9yre; logan_custom_report=%7B%22unionId%22%3A%2213727585%22%2C%22biz%22%3A%22waimai_ad_pc_vue%22%7D; JSESSIONID=node011yr96j1d4rre69tmqpk2w2cp63650231.node0; _lxsdk_s=182a71019bf-eeb-89d-2da%7C%7C30'
}

# 定义api
api = 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysis/searchword/searchWordRank'

# 设置请求参数
data = {
	'acctId': '118075493',
	'categoryIds': '[200001481]',
	'peerType': '0',
	'recentDays': '7',
	'searchWordType': 'searchWordRankHot',
	'source': '0',
	'wmPoiId': '13727585'
}

# 发送请求获取数据

resp = requests.post(api, data=data, headers=headers)

print(resp.text)
