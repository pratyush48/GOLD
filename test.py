import random as rnd
x = []
y = []
sol1 = [[0,0,20] for i in range(0,201)]
sol2 = [[0,0,20] for i in range(0,1)]
for i in range(0,201):
    for j in range(0,3):
        if(j==0):
            num = rnd.randint(3,255)
            while x.count(num):
                num = rnd.randint(3,255)
            sol1[i][j] = num
            x.append(sol1[i][j])
        elif(j==1):
            num = rnd.randint(3,255)
            while y.count(num):
                num = rnd.randint(3,255)
            sol1[i][j] = num
            y.append(sol1[i][j])
print(sol1)
print("end----")
for i in range(0,1):
    for j in range(0,3):
        if(j==0):
            num = rnd.randint(3,255)
            while x.count(num):
                num = rnd.randint(3,255)
            sol2[i][j] = num
            x.append(sol2[i][j])
        elif(j==1):
            num = rnd.randint(3,255)
            while y.count(num):
                num = rnd.randint(3,255)
            sol2[i][j] = num
            y.append(sol2[i][j])
print(sol2)