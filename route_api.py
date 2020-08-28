import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}


#计算两点距离
def compute_dis(longtitude1, latitude1, longtitude2, latitude2):
    #默认访问接口
    request_url = 'http://restapi.amap.com/v3/distance?key=b1d4267a269c108cb148f1b95183890c&origins='+str(longtitude1)+',' + str(latitude1) + '8&destination=' + str(longtitude2) + ',' + str(latitude2) + '&type=1'
    data = requests.get(request_url, headers = header, timeout = 10)
    data.encoding = 'utf-8'
    data = data.text
    pattern = "distance\":\"(.*?)\",\"duration\":\"(.*?)\""
    result = re.findall(pattern, data)
    #返回距离 result[0][0], 时间result[0][1]
    return result[0][0]
print(compute_dis(116.491242, 39.807005,116.517029, 39.923417))

from collections import defaultdict
graph = defaultdict(dict)

#数据加载
data = pd.read_csv('./subway.csv', index_col = None)
# 创建图中两点之间的距离


for i in range(data.shape[0]):
    site1 = data.iloc[i]['site']
    #print(site1)
    if i < data.shape[0] - 1 :
        site2 = data.iloc[i+1]['site']
        #如果是同一条线路
        if site1 == site2:
            longtitude1, latitude1 = data.iloc[i]['longtitude'], data.iloc[i]['latitude']
            longtitude2, latitude2 = data.iloc[i+1]['longtitude'], data.iloc[i+1]['latitude']
            name1, name2 = data.iloc[i]['name'], data.iloc[i+1]['name']
            distance = compute_dis(longtitude1, latitude1, longtitude2, latitude2)
            graph[name1][name2] = distance
            graph[name2][name1] = distance
            print(name1, name2, distance)
    #保存python对象
if __name__ == '__main__':   
    import pickle
    output = open('graph.pkl', 'wb')
    pickle.dump(graph, output)
    print(graph)
#使用pickle对象
# import pickle
# file = open('graph.pkl', 'rb')
# graph = pickle.load(file)
# print(graph)

#找到开销最小的节点
def find_lowest_cost_node(costs):
    #初始化数据
    lowest_cost = float('inf')
    lowest_cost_node = None
    #遍历所有节点
    for node in costs:
        if not node in processed:
            #如果当前节点的cost比已经存在的cost小，那么擂主更新，即更新最小节点
            if costs[node] < lowest_cost:
                lowest_cost = costs[node]
                lowest_cost_node = node
    return lowest_cost_node

#找到最短路径,从end到start的完整路径
def find_shortest_path():
    node = end
    shortest_path = [end]
    print('parents:',parents[node])
    while parents[node] != start:
        shortest_path.append(parents[node])
        node = parents[node]
    shortest_path.append(start)
    return shortest_path

#计算图中从start到end的最短路径
def dijkstra():
    node = find_lowest_cost_node(costs)
    print('当前cost最小节点：', node)
    #只要有cost最小的节点，就进行路径计算，如果所有节点都在processed里面，结束
    while node is not None:
        #获取节点目前cost
        cost = costs[node]
        neighbors = graph[node]
        #遍历所有邻居，看是否可以通过这个node进行cost更新
        for neighbor in neighbors.keys():
            #计算经过当前节点，到达邻居节点的cost
            new_cost = cost + float(neighbors[neighbor])
            #通过node, 可以更新start -> neighbor的cost
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = node
        #将当前节点标记为处理过
        processed.append(node)
        
        #找出接下来要处理的节点，并循环
        node = find_lowest_cost_node(costs)
    #循环完毕，所有节点处理完毕
    shortest_path = find_shortest_path()
    #shortest_path = shortest_path.reverse()
    print('从{}到{}的shortest_path：{}'.format(start, end, shortest_path))
    return shortest_path


def compute(site1, site2):
    global start, end, parents, costs, processed
    start = site1
    end = site2

    costs = {}
    parents = {}
    parents[end] = None
    processed = []

    #获取节点的邻居节点：初始化损失集合
    for node in graph[start].keys():
        costs[node] = float(graph[start][node])
        parents[node] = start
    
    costs[end] = float('inf')
    shortest_path = dijkstra()
    print('最短路径长度站点数为：', len(shortest_path))
    print('最短路径距离：', costs[end])
    return shortest_path

if __name__ == '__main__':
    site1 = '北京南站'
    site2 = '五道口站'
    shortest_path = compute(site1, site2)