import os
import json
import jsonpath
import requests
import pandas as pd

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0',
    'Cookie': '_lxsdk_cuid=186e3a74321c8-04b380ee242942-4c657b58-1fa400-186e3a74321c8; _lxsdk=186e3a74321c8-04b380ee242942-4c657b58-1fa400-186e3a74321c8; token=0V-F34GjGqVe6NAphZfHZZ2xRsAPnpj3PMQfdBO8BhUI*; bsid=j_Zz1-hLuqWi0MEXVzAklEcu_EtvfABur312ODFYzwVen-VnSjgdQs_t544btQYE3McV0PxEDt1oampfi3ePlA; acctId=118075493; wmPoiId=13727585; _source=PC; device_uuid=!7032548e-55a5-420f-bcae-0456f5473eba; igateApp=recoanalysis; bizad_cityId=110105; bizad_second_city_id=110100; bizad_third_city_id=110105; wmPoiName=%E6%81%8B%E4%BA%BA%E9%B2%9C%E8%8A%B1%E5%BA%97%EF%BC%88%E7%8E%AB%E7%91%B0%E8%8A%B1.%E7%94%9F%E6%97%A5%E9%B2%9C%E8%8A%B1.%E5%BC%80%E4%B8%9A%E8%8A%B1%E7%AF%AE%EF%BC%89; terminal=bizCenter; platform=0; showNewModal=true; logan_session_token=kzijbnum81ux0ym43x2m; logan_custom_report=%7B%22unionId%22%3A%2213727585%22%2C%22biz%22%3A%22waimai_ad_pc_vue%22%7D; JSESSIONID=node01v5oc5w2ar56f1n6389mxttqva54518932.node0; _lxsdk_s=186e99ac0c8-1be-249-669%7C%7C476'
}

# 曝光人数
api_exposure = "https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20230315&hour=18&index=FLOW_POI_EXPOSE_UV&source=0&wmPoiId=13727585";

# 入店人数
api_into = "https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20230315&hour=18&index=FLOW_HOME_PAGE_UV&source=0&wmPoiId=13727585";

# 下单人数
api_order = "https://waimaieapp.meituan.com/igate/recoanalysis/flowAnalysisV4/realTime/flowTransformationChart?acctId=118075493&compareDate=20230315&hour=18&index=FLOW_SUBMITTED_UV&source=0&wmPoiId=13727585";

# 获取曝光人数数据
resp_exposure = requests.get(api_exposure, headers=headers)
# 加载曝光人数数据
json_exposure = json.loads(resp_exposure.text)
# 解析曝光人数数据
data = jsonpath.jsonpath(json_exposure, "$..data")[0]
# 获取昨天的曝光人数数据
ring = jsonpath.jsonpath(data, "$..ring")[0]
print("分时曝光人数")
# 便利获取昨天分小时曝光数据
for value in ring:
    print(value, end=" ")
print()

# 获取入店人数数据
resp_into = requests.get(api_into, headers=headers)
# 加载入店人数数据
json_exposure = json.loads(resp_into.text)
# 解析入店人数数据
data = jsonpath.jsonpath(json_exposure, "$..data")[0]
# 获取昨天的入店人数数据
ring = jsonpath.jsonpath(data, "$..ring")[0]

print("分时进店人数")
# 便利获取昨天分小时进店数据
for value in ring:
    print(value, end=" ")
print()

# 获取下单人数数据
resp_order = requests.get(api_order, headers=headers)
# 加载下单人数数据
json_exposure = json.loads(resp_order.text)
# 解析下单人数数据
data = jsonpath.jsonpath(json_exposure, "$..data")[0]
# 获取昨天的下单人数数据
ring = jsonpath.jsonpath(data, "$..ring")[0]
print("分时下单人数")
# 便利获取昨天分小时下单数据
for value in ring:
    print(value, end=" ")
print()
