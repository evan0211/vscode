import random

file = open('python\AI\sample data.txt','r')
txt = file.read()
txt = txt.split('\n')
data = []
for i in txt:
    x, y = i.split(',')
    data.append(([float(x), float(y)]))
file.close()

def random_point(data, k):
    return random.sample(data, k)

def calculate_distance(data, point, new_point):
    for i in data:
        min_distance_list = []
        for j in point:
            distance = abs(((i[0]-j[0])**2) + ((i[1]-j[1])**2))
            min_distance_list.append(distance)
        min_distance =min(min_distance_list)
        min_distance_idx = min_distance_list.index(min_distance)
        distance_list.append([i, min_distance_idx, min_distance])
    for i in range(k):
        x = 0
        y = 0
        d = 0
        c = 0
        for j in distance_list:
            if j[1] == i:
                c += 1
                x += j[0][0]
                y += j[0][1]
                d += j[2]
        x /= c
        y /= c 
        d /= c       
        new_point.append([x, y])
        new_min_distance_list.append(d)
                
k = int(input('輸入k值:'))
r = 0
distance_list = []
new_point = []
new_min_distance_list = []
point = random_point(data, k)
calculate_distance(data, point, new_point)
while k > 0:
    r += 1
    if point == new_point:
        print(distance_list)
        with open('result.txt','w',encoding='utf-8') as f:
            f.write(f'執行了{r}次')
            f.write('\n')
            c = 0
            for i in new_min_distance_list:
                c += 1
                f.write(f'第{c}圈平均距離{i}')
                f.write('\n')
            for i in distance_list:
                f.write(f'{i[0]}第{i[1]+1}群')
                f.write('\n')
        break
    else:
        print(new_point)
        point = new_point
        new_point = []
        distance_list = []
        new_min_distance_list = []
        calculate_distance(data, point, new_point)
       
        
        

