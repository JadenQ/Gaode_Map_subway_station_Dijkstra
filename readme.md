### Shortest path traveling by Beijing(or other cities) subway
### 北京地铁（或其它城市地铁）最短路径出行规划

#### What it is? 这是什么？❓

-Using Gaode Map API for location information and scrap subway station information online.
-使用高德地图API获取经纬度信息，网络爬取地铁站信息。

-Find the nearest station given a name from a map.
-根据给定地图上的点确定距离最近的地铁站

-Dijkstra method for shortest path planning among subway stations.
-Dijkstra方法进行地铁站点之间地最短路径规划。

#### How to use? 如何使用？❓
-Python 3.7, Windows
-Required packages 需要的包 : requests, re, pandas, bs4

-All the python files should be put under one directory
-所有python文件放在同一个路径下

-Run preprocessing_location.py to get the data from api and websites
-运行preprocessing_location.py进行数据爬取

-Run route_api.py to to test the dijkstra method, this file contains necessary functions for test.py
-运行 route_api.py 测试dijkstra算法，其中包含了运行test.py必须的函数

-Run test.py to for full functions: identify the nearest subway station, use dijkstra method to find the shortest path and output.
-运行test.py找到距离输入的起点与终点最近的地铁站以及最短路径路线。

-Iutput: start - Your start point. end - Your destination.
-输入：start - 起点 end - 目的地

-Key function: test.compute() 
-主运行函数： test.compute()

#### Extensions 拓展 ⭐ 
1. Try to use information of different cities, change the variable 'city' from '北京' to others.
The website I use https://ditie.mapbar.com/beijing_line/
-试着换用其他城市地铁信息
2. Try to use time consumed as a factor instead of distance or the number of nodes, or consider both of the factors.
-试着使用最短用时而不是最短的路径或节点进行规划， 试着综合考虑


