#最近地点
import sys 
sys.path
import route_api
import preprocessing_location 
import pandas as pd

def get_nearest_subway(data, location1):
	distance = float('inf')
	nearest = None
	for i in range(data.shape[0]):
		site1 = data.iloc[i]['name']
		longtitude = float(data.iloc[i]['longtitude'])
		latitude = float(data.iloc[i]['latitude'])
		# 计算距离
		temp = (float(location1[0]) - longtitude)**2 + (float(location1[1]) - latitude)**2
		if temp < distance:
			distance = temp
			nearest = site1
	return nearest

def compute(site1, site2):
	location1 = preprocessing_location.get_location(site1, city)
	location2 = preprocessing_location.get_location(site2, city)
	#print(location1)
	#print(location2)
	#计算离site1最近的
	data = pd.read_csv('./subway.csv')
	start = get_nearest_subway(data, location1)
	end = get_nearest_subway(data, location2)
	print('距离出发点{}最近的地铁站为{},距离目的地{}最近的地铁站为{}'.format(site1,start,site2,end))
	shortest_path = route_api.compute(start, end)
	if site1 != start:
		shortest_path.insert(0, site1)
	if site2 != end:
		shortest_path.append(site2)
	print('从{}到{}的最优路线：{}'.format(site1, site2, shortest_path))
city = '北京'
compute('清华大学','798')
#route_api.compute()