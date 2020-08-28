import requests
from bs4 import BeautifulSoup
import pandas as pd
header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
# 根据request的url得到soup
def get_page_content(request_url):
    #得到页面的内容
    html = requests.get(request_url, headers = header, timeout = 10)
    content = html.text
    print(content)
    soup = BeautifulSoup(content, 'html.parser', from_encoding = 'utf-8')
    return soup
if __name__== '__main__':
    request_url = 'https://ditie.mapbar.com/beijing_line/'
    soup = get_page_content(request_url)
    
    df = pd.DataFrame(columns = ['name', 'site'])
    subways = soup.find_all('div', class_ = 'station')
    for subway in subways:
        route_name = subway.find('strong', class_ = 'bolder').text
        routes = subway.find('ul')
        routes = routes.find_all('a')
        
        #对于所有route都保存name
        for route in routes:
            temp = {'name' : route.text, 'site': route_name}
            df = df.append(temp, ignore_index = True)
            
    df['city'] = '北京'
    print(df)
    df.to_csv('subway.csv',index = False, encoding = 'utf-8')

#使用高德API
import re
#通过keyword,city得到指定location
#老师在课上给的链接失效，自己重新申请了api的key = b1d4267a269c108cb148f1b95183890c
def get_location(keyword, city):
    request_url = 'http://restapi.amap.com/v3/place/text?key=b1d4267a269c108cb148f1b95183890c&keywords='+ keyword + '&types=&city=' + city + '&children=1&offset=1&page=1&extensions=all'
    data = requests.get(request_url, headers = header, timeout = 10)
    data.encoding = 'utf-8'
    data = data.text
    #后面多了一个?表示懒惰模式
    #.*具有贪婪模式，匹配到不能匹配未知
    #。*？取消贪婪，一个匹配以后，就继续后面的正则
    pattern = 'location":"(.*?),(.*?)"'
    #得到经纬度
    result = re.findall(pattern, data)

    try:
        return result[0][0], result[0][1]
    except:
        return get_location(keyword.replace('站',''), city)

if __name__ == '__main__':
    df = pd.read_csv('./subway.csv', index_col = None)
    print(df.head())
    
    # df['longtitude'], df['latitude'] = None, None
    
    # for index, row in df.iterrows():
    #     name, city = row['name'], row['city']
    #     longtitude, latitude = get_location(name, city)    
    #     df.iloc[index]['longtitude'] = longtitude
    #     df.iloc[index]['latitude'] = latitude
    #     print(longtitude, latitude)
    # df.to_csv('subway.csv', index = False)
    
    longtitudes = []
    latitudes = []
    for index, row in df.iterrows():
        name, city = row['name'], row['city']
        longtitude, latitude = get_location(name, city)  
        longtitudes.append(longtitude)
        latitudes.append(latitude)
    longtitudes = pd.Series(longtitudes)
    latitudes = pd.Series(latitudes)
    df['longtitude'] = longtitudes
    df['latitude'] = latitudes
    df.to_csv('subway.csv', index = False)
    df.head()