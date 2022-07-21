import json
import datetime
import jsonpath
import pymysql
import requests

# 定义请求头
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
	'Cookie': 'wm_order_channel=default; request_source=openh5; iuuid=FFA3E5AECB339DC7341A285FCA2D3D9A0C0348DC97B213DD0BFF08C6CA2B31DF; _lxsdk_cuid=181de72834cc8-0b69dbd0e3347e-673b5753-1fa400-181de72834cc8; _lxsdk=FFA3E5AECB339DC7341A285FCA2D3D9A0C0348DC97B213DD0BFF08C6CA2B31DF; uuid=acc4ca2aca3853b6459a.1657502638.1.0.0; token=0UWJJub5o9pwC7fi-PYWiSTtxkhh8c6pVEogDwAl87s0*; bsid=4PoC8y__b8zPvbXeir6QvoJiHNs3YdmU8R7UXvb1_lqLk1In-2FXu2xmff3TXY_JCCnxYLjxamHVAKFQLczTEQ; acctId=118075493; wmPoiId=13727585; _source=PC; terminal=bizCenter; bizad_cityId=110105; bizad_second_city_id=110100; bizad_third_city_id=110105; wmPoiName=%E6%81%8B%E4%BA%BA%E9%B2%9C%E8%8A%B1%E5%BA%97%EF%BC%88%E7%8E%AB%E7%91%B0%E8%8A%B1.%E7%94%9F%E6%97%A5%E9%B2%9C%E8%8A%B1.%E5%BC%80%E4%B8%9A%E8%8A%B1%E7%AF%AE%EF%BC%89; mtcdn=K; lt=STjXCBh_0Sr4PUWZti18o8mKtZsAAAAAvRIAAIktymLmaJZ3cp2gAunxAbdDPu06I_VCzRrSexYUojT3UCLPxNa9Atg4VFCHIMHe9Q; mt_c_token=STjXCBh_0Sr4PUWZti18o8mKtZsAAAAAvRIAAIktymLmaJZ3cp2gAunxAbdDPu06I_VCzRrSexYUojT3UCLPxNa9Atg4VFCHIMHe9Q; userId=255996836; igateApp=recoanalysis; platform=0; WEBDFPID=5vwyvzu481835612z00y700955zxxw69818uu0yuy2x97958212020u7-1657937221501-; logan_session_token=eopyc79vfbzepb6vj6hm; logan_custom_report=%7B%22unionId%22%3A%2213727585%22%2C%22biz%22%3A%22waimai_ad_pc_vue%22%7D; JSESSIONID=node0lelhhiww1hlq1vewos7dvrkoe4508581.node0'
}

# 获取当前日期
today = datetime.date.today()
# 获取1天
oneday = datetime.timedelta(days=1)
# 计算昨天日期
yesterday = today - oneday
# 转换昨天日期格式
yes_format = str(yesterday).replace('-', '')

# 定义请求api
json_api = {
	# 曝光人数
	'exposure': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_POI_EXPOSE_UV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 曝光次数
	'impressions': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_POI_EXPOSE_PV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 入店率
	'clickRate': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_HOME_PAGE_EXPOSE_RATE&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 入店人数
	'clickNum': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_HOME_PAGE_UV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 入店次数
	'clickCount': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_HOME_PAGE_PV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 下单转化率
	'orderRate': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_SUBMITTED_HOME_PAGE_RATE&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 下单人数
	'orderNum': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_SUBMITTED_UV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 下单次数
	'orderCount': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_SUBMITTED_PV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 下单金额
	'orderAmount': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_SUBMITTED_ACTUAL_AMT&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 支付人数
	'payNum': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_PAY_UV&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 支付金额
	'payAmount': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_PAY_ACTUAL_AMT&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}'),
	# 支付转化率
	'payRate': 'https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20220713&hour=0&index=FLOW_PAY_SUBMITTED_RATE&source=0&wmPoiId=13727585'.replace(
		'20220713', f'{yes_format}')
}


def get_json():
	# 发送请求获取响应
	# 曝光人数
	resp_exposure = requests.get(json_api['exposure'], headers=headers)
	# 曝光次数
	resp_impressions = requests.get(json_api['impressions'], headers=headers)
	# 入店率
	resp_clickRate = requests.get(json_api['clickRate'], headers=headers)
	# 入店人数
	resp_clickNum = requests.get(json_api['clickNum'], headers=headers)
	# 入店次数
	resp_clickCount = requests.get(json_api['clickCount'], headers=headers)
	# 下单转化率
	resp_orderRate = requests.get(json_api['orderRate'], headers=headers)
	# 下单人数
	resp_orderNum = requests.get(json_api['orderNum'], headers=headers)
	# 下单次数
	resp_orderCount = requests.get(json_api['orderCount'], headers=headers)
	# 下单金额
	resp_orderAmount = requests.get(json_api['orderAmount'], headers=headers)
	# 支付人数
	resp_payNum = requests.get(json_api['payNum'], headers=headers)
	# 支付金额
	resp_payAmount = requests.get(json_api['payAmount'], headers=headers)
	# 支付转化率
	resp_payRate = requests.get(json_api['payRate'], headers=headers)
	# 返货json数据
	return resp_exposure.text, resp_impressions.text, resp_clickRate.text, resp_clickNum.text, resp_clickCount.text, resp_orderRate.text, resp_orderNum.text, resp_orderCount.text, resp_orderAmount.text, resp_payNum.text, resp_payAmount.text, resp_payRate.text


# 解析并保存曝光人数
def parse_exposure(exposure_json):
	# 加载json数据
	json_data = json.loads(exposure_json)
	# 解析json数据获取曝光人数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应曝光数据
	exposure_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段曝光人数数据
	for exposure in data_list:
		# 将时段及曝光数据添加到字典
		exposure_dict[f'{time}:00'] = exposure
		time += 1
	return exposure_dict


# 解析并保存曝光次数
def parse_impressions(impressions_json):
	# 加载json数据
	json_data = json.loads(impressions_json)
	# 解析json数据获取曝光次数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应曝光次数数据
	impressions_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段曝光次数数据
	for impressions in data_list:
		# 将时段及曝光次数数据添加到字典
		impressions_dict[f'{time}:00'] = impressions
		time += 1
	# 返回曝光次数数据
	return impressions_dict


# 解析并保存入店率
def parse_clickRate(clickRate_json):
	# 加载json数据
	json_data = json.loads(clickRate_json)
	# 解析json数据获取入店率数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应入店率数据
	clickRate_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段入店率数据
	for clickRate in data_list:
		# 将时段及入店率数据添加到字典
		clickRate_dict[f'{time}:00'] = clickRate
		time += 1
	# 返回入店率数据
	return clickRate_dict


# 解析并保存入店人数
def parse_clickNum(clickNum_json):
	# 加载json数据
	json_data = json.loads(clickNum_json)
	# 解析json数据获取入店人数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应入店人数据
	clickNum_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段入店人数据
	for clickNum in data_list:
		# 将时段及入店人数据添加到字典
		clickNum_dict[f'{time}:00'] = clickNum
		time += 1
	# 返回入店人数据
	return clickNum_dict


# 解析并保存入店次数
def parse_clickCount(clickCount_json):
	# 加载json数据
	json_data = json.loads(clickCount_json)
	# 解析json数据获取入店次数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应入店次数数据
	clickCount_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段入店次数数据
	for clickCount in data_list:
		# 将时段及入店次数数据添加到字典
		clickCount_dict[f'{time}:00'] = clickCount
		time += 1
	# 返回入店次数数据
	return clickCount_dict


# 解析并保存下单转化率
def parse_orderRate(orderRate_json):
	# 加载json数据
	json_data = json.loads(orderRate_json)
	# 解析json数据获取下单转化率数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应下单转化率数据
	orderRate_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段下单转化率数据
	for orderRate in data_list:
		# 将时段及下单转化率数据添加到字典
		orderRate_dict[f'{time}:00'] = orderRate
		time += 1
	# 返回入店次数数据
	return orderRate_dict


# 解析并保存下单人数
def parse_orderNum(orderNum_json):
	# 加载json数据
	json_data = json.loads(orderNum_json)
	# 解析json数据获取下单转化率数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应下单转化率数据
	orderNum_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段下单转化率数据
	for orderNum in data_list:
		# 将时段及下单转化率数据添加到字典
		orderNum_dict[f'{time}:00'] = orderNum
		time += 1
	# 返回入店次数数据
	return orderNum_dict


# 解析并保存下单次数
def parse_orderCount(orderCount_json):
	# 加载json数据
	json_data = json.loads(orderCount_json)
	# 解析json数据获取下单次数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应下单次数数据
	orderCount_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段下单次数数据
	for orderCount in data_list:
		# 将时段及下单次数数据添加到字典
		orderCount_dict[f'{time}:00'] = orderCount
		time += 1
	# 返回下单次数数据
	return orderCount_dict


# 解析并保存下单金额
def parse_orderAmount(orderAmount_json):
	# 加载json数据
	json_data = json.loads(orderCount_json)
	# 解析json数据获取下单次数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应下单次数数据
	orderCount_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段下单次数数据
	for orderCount in data_list:
		# 将时段及下单次数数据添加到字典
		orderCount_dict[f'{time}:00'] = orderCount
		time += 1
	# 返回下单次数数据
	return orderCount_dict


# 解析并保存支付人数
def parse_payNum(payNum_json):
	# 加载json数据
	json_data = json.loads(payNum_json)
	# 解析json数据获取支付人数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应支付人数数据
	payNum_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段支付人数数据
	for payNum in data_list:
		# 将时段及支付人数数据添加到字典
		payNum_dict[f'{time}:00'] = payNum
		time += 1
	# 返回支付人数数据
	return payNum_dict


# 解析并保存支付金额
def parse_payAmount(payAmount_json):
	# 加载json数据
	json_data = json.loads(payAmount_json)
	# 解析json数据获取支付人数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应支付人数数据
	payAmount_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段支付人数数据
	for payAmount in data_list:
		# 将时段及支付人数数据添加到字典
		payAmount_dict[f'{time}:00'] = payAmount
		time += 1
	# 返回支付人数数据
	return payAmount_dict


# 解析并保存支付转化率
def parse_payRate(payRate_json):
	# 加载json数据
	json_data = json.loads(payRate_json)
	# 解析json数据获取支付人数数据列表
	data_list = jsonpath.jsonpath(json_data, '$..data..chart..ring')[0]
	# 定义字典存储时段对应支付人数数据
	payRate_dict = {}
	# 定义时间
	time = 0
	# 遍历数据列表获取各时段支付人数数据
	for payRate in data_list:
		# 将时段及支付人数数据添加到字典
		payRate_dict[f'{time}:00'] = payRate
		time += 1
	# 返回支付人数数据
	return payRate_dict


# 链接数据库保存数据
def connect_mysql():
	# 创建数据库链接
	conn = pymysql.connect(user='fayewong', password='4012', host='124.222.30.249', database='meituan', port=3306,
	                       charset="utf8")
	# 创建游标对象
	curs = conn.cursor()
	return conn, curs


# 存储数据
def save_data(exposure_dict, impressions_dict, clickRate_dict, clickNum_dict, clickCount_dict, orderRate_dict,
              orderNum_dict, orderCount_dict, orderAmount_dict, payNum_dict, payAmount_dict, payRate_dict, conn, curs):
	# 转换日期为字符串
	date = str(yesterday)
	# 遍历获取各时段的数据
	for i in range(24):
		time = str(f'{i}:00')
		exposure = str(exposure_dict[time])
		impressions = str(impressions_dict[time])
		clickRate = str(clickRate_dict[time])
		if clickRate=='None':
			clickRate = '0'
		clickNum = str(clickNum_dict[time])
		clickCount = str(clickCount_dict[time])
		orderRate = str(orderRate_dict[time])
		if orderRate=='None':
			orderRate = '0'
		orderNum = str(orderNum_dict[time])
		orderCount = str(orderCount_dict[time])
		orderAmount = str(orderAmount_dict[time])
		payNum = str(payNum_dict[time])
		payAmount = str(payAmount_dict[time])
		payRate = str(payRate_dict[time])
		if payRate=='None':
			payRate = '0'
		# 定义插入数据sql
		save_data_sql = "INSERT INTO TrafficAnalysis (`id`,`date`,`time`,`exposure`,`impressions`,`clickRate`,`clickNum`,`clickCount`,`orderRate`,`orderNum`,`orderCount`,`orderAmount`,`payNum`,`payAmount`,`payRate`) VALUES (0, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
			date, time, exposure, impressions, clickRate, clickNum, clickCount, orderRate, orderNum, orderCount,
			orderAmount, payNum, payAmount, payRate)
		# 使用游标对象执行插入操作
		curs.execute(save_data_sql)
		# 提交数据
		# 提交数据
	conn.commit()
	print(f'流量分析数据已更新!')


if __name__ == '__main__':
	# 发送请求获取json数据
	exposure_json, impressions_json, clickRate_json, clickNum_json, clickCount_json, orderRate_json, orderNum_json, orderCount_json, orderAmount_json, payNum_json, payAmount_json, payRate_json = get_json()
	# 解析获取各时段曝光人数数据
	exposure_dict = parse_exposure(exposure_json)
	# 解析获取各时段曝光次数数据
	impressions_dict = parse_impressions(impressions_json)
	# 解析获取各时段入店率数据
	clickRate_dict = parse_clickRate(clickRate_json)
	# 解析获取各时段入店人数数据
	clickNum_dict = parse_clickNum(clickNum_json)
	# 解析获取各时段入店次数数据
	clickCount_dict = parse_clickNum(clickCount_json)
	# 解析获取各时段下单转化率数据
	orderRate_dict = parse_clickNum(orderRate_json)
	# 解析获取各时段下单人数数据
	orderNum_dict = parse_clickNum(orderNum_json)
	# 解析获取各时段下单次数数据
	orderCount_dict = parse_clickNum(orderCount_json)
	# 解析获取各时段下单金额数据
	orderAmount_dict = parse_clickNum(orderAmount_json)
	# 解析获取各时段支付人数数据
	payNum_dict = parse_clickNum(payNum_json)
	# 解析获取各时段支付金额数据
	payAmount_dict = parse_clickNum(payAmount_json)
	# 解析获取各时段支付转化率数据
	payRate_dict = parse_clickNum(payRate_json)
	# 创建数据库链接
	conn, curs = connect_mysql()
	# 存储数据
	save_data(exposure_dict, impressions_dict, clickRate_dict, clickNum_dict, clickCount_dict, orderRate_dict,
	          orderNum_dict, orderCount_dict, orderAmount_dict, payNum_dict, payAmount_dict, payRate_dict, conn, curs)
	print('数据存储完成！！！')
