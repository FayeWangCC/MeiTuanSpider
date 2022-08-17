import json
import datetime
import jsonpath
import pymysql
import requests


# 设置请求头
def get_config():
	# 读取文件配置参数
	with open('_config', 'r') as f:
		cpc_api = f.readline()

	# 设置请求头
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
	}
	# 返回数据接口,请求头
	return headers, cpc_api


# 发送请求获取json数据
def get_json(headers, cpc_api):
	# 发送请求获取响应json数据
	resp = requests.get(url=cpc_api)
	json_data = resp.text
	return json_data


# 链接数据库保存数据
def connect_mysql():
	# 创建数据库链接
	conn = pymysql.connect(user='fayewong', password='4012', host='124.222.30.249', database='meituan', port=3306,
	                       charset="utf8")
	# 创建游标对象
	curs = conn.cursor()
	return conn, curs


# 解析json获取昨日推广数据
def parse_json_sum(json_data, conn, curs):
	# 加载json数据
	data = json.loads(json_data)
	# 使用jsonpath解析到昨天整体数据
	yes_Overview = jsonpath.jsonpath(data, '$..data...yesterdayOverview')[0]
	# 解析昨天的各项数据
	# 曝光次数
	yes_showCount = yes_Overview['showCount']
	# 点击次数
	yes_clickCount = yes_Overview['clickCount']
	# 推广消耗
	yes_cost = yes_Overview['cost']
	# 单次点击花费
	yes_avgPrice = yes_Overview['avgPrice']
	# 点击率
	yes_clickRate = yes_Overview['clickRate']

	# 获取当前日期
	today = datetime.date.today()
	# 获取1天
	oneday = datetime.timedelta(days=1)
	# 计算昨天日期
	yes_date = str(today - oneday)

	# 定义插入数据sql
	save_data_sql = "INSERT INTO CPC_Sum (`id`,`date`,`showCount`,`clickCount`,`cost`,`avgPrice`,`clickRate` ) VALUES (0,'%s','%s','%s','%s','%s','%s')" % (
		yes_date, yes_showCount, yes_clickCount, yes_cost, yes_avgPrice, yes_clickRate)
	# 使用游标对象执行插入操作
	curs.execute(save_data_sql)
	# 提交数据
	# 提交数据
	conn.commit()
	print(f'昨日点金推广汇总数据已更新')


# 解析json获取昨日各时段数据
def parse_json_period(json_data, conn, curs):
	# 加载json数据
	data = json.loads(json_data)
	# 使用json解析昨天全部时段数据
	yesterday = jsonpath.jsonpath(data, '$..data..yesterday')[0]
	for period in yesterday:
		# 时段
		time = str(period['time']).split('-')[0]
		# 曝光次数
		showCount = str(period['showCount'])
		# 点击次数
		clickCount = str(period['clickCount'])
		# 推广花费
		cost = str(period['cost'])
		# 单次点击消耗
		avgPrice = str(period['avgPrice'])
		# 进店率
		clickRate = str(period['clickRate'])

		# 获取当前日期
		today = datetime.date.today()
		# 获取1天
		oneday = datetime.timedelta(days=1)
		# 计算昨天日期
		yes_date = str(today - oneday)

		# 定义插入数据sql
		save_data_sql = "INSERT INTO CPC_Period (`id`,`date`,`time`,`showCount`,`clickCount`,`cost`,`avgPrice`,`clickRate` ) VALUES (0,'%s','%s','%s','%s','%s','%s','%s')" % (
			yes_date, time, showCount, clickCount, cost, avgPrice, clickRate)
		# 使用游标对象执行插入操作
		curs.execute(save_data_sql)
	# 提交数据
	conn.commit()
	print(f'昨日点金推广各时段数据已更新')


if __name__ == '__main__':
	# 获取配置参数
	headers, cpc_api = get_config()
	# 发送请求获取json数据
	json_data = get_json(headers=headers, cpc_api=cpc_api)
	# 创建数据库链接获取链接及游标对象
	conn, curs = connect_mysql()
	# 解析数据(汇总数据)
	parse_json_sum(json_data, conn=conn, curs=curs)
	# 解析数据(时段数据)
	parse_json_period(json_data, conn=conn, curs=curs)
	# 关闭数据库及游标对象链接
	curs.close()
	conn.close()
	print('昨日点金推广数据以抓取保存完成')
