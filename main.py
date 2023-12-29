l2 = []
wts = [(10, 5), (20, 5), (100, 15), (40, 10), (100, 35), (100, 30)]

f = open("IPmarks.txt",'r')
contents = f.readlines()
f.close()

def calc_grade(sum):
    grd = ''
    if sum > 80:
        grd = 'A'
    elif 80 >= sum > 70:
        grd = 'A-'
    elif 70 >= sum > 60:
        grd = 'B'
    elif 60 >= sum > 50:
        grd = 'B-'
    elif 50 >= sum > 40:
        grd = 'C'
    elif 40 >= sum > 35:
        grd = 'C-'
    elif 35 >= sum > 30:
        grd = 'D'
    else:
        grd = 'F'
    return grd

line = []
for i in contents:
    k = i.strip()
    line.append(k)

line2 = []
for i in line:
    line = i.split(',')
    line2.append(line)

for i in line2:
    l1 = []
    for j in range(1,len(i)):
        l1.append(int(i[j]))
    l2.append(l1)

p2 = []
for i in range(len(l2)):
    p1 = []
    sum1 = 0
    for j in range(len(l2[i])):
        sum1 += l2[i][j] * wts[j][1]/wts[j][0]
    p1.append(sum1)
    p2.append(p1)

s1 = []
for i in p2:
    s = sum(i)
    s1.append(s)

f = open('IPgrade.txt','w')

for i in range(len(l2)):
    f.write(line2[i][0] + ',' + str(s1[i]) + ',' + calc_grade(s1[i]) + '\n')