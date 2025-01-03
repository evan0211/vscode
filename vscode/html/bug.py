import requests as r
try:
    a=input('輸入日期 格式範例:2024-05-27\n')
    year,month,day=map(str,a.split('-'))
    url=f'https://api.taiwanlottery.com/TLCAPIWeB/Lottery/SuperLotto638Result?period&month={year}-{month}&pageNum=1&pageSize=50'
    data=r.get(url).json()
    results = data['content']['superLotto638Res']
    dict={}
    for i in results:
        time=i['lotteryDate'][:10]
        print(time)
        drawNumberSize = i['drawNumberSize']
        dict[time] = drawNumberSize
    drawNumberSize = dict[a]
    for i in drawNumberSize:
        print(i,end=' ')
except:
    print('請輸入正確格式')
