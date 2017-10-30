import numpy as np
from  IO import *
from model import *
import matplotlib.pyplot as plt


def Gradient(Plan):
    M = plan.M
    tt = np.linalg.inv(M**2)
    gradient = []
    for i in plan.plan:
        f = plan.f(i.x)
        gradient.append(f.T@(tt)@f)
    return gradient

def Calc_Phi(M,x,_f):
    f = _f(x)
    tt = np.linalg.inv(M**2)
    return  f.T@(tt)@f

def write_plan(watchs):
    file = open('input.txt','w')
    for i in watchs:
        file.write(str(i.x[0])+'\t'+ str(i.x[1]) +'\t' +str(i.p)+'\n')



def read_plan(filename):
    file = open('input.txt','r')
    plan = []
    str = file.read().split('\n')
    for str in str:
        parse_str = str.split('\t')
        plan.append(elem_plan((float(parse_str[0]),float(parse_str[1])),float(parse_str[2])))

    return plan
 
def findMax(grad):
    maxfi = grad
    for i in grad:
        if i[1] > maxfi[1]:
            maxfi = i
    return maxfi

def findMin(grad):
    minfi = grad
    for i in grad:
        if i[1] <= minfi[1]:
            minfi = i
    return minfi
  
n = 20
x = np.linspace(-1,1,11)
_x  = []
for i in x:
    for j in x:
        _x.append((i,j))
watchs = IO.Make_points(20, IO.auto_plan(1/n,x))
write_plan(watchs)
#watchs = read_plan('plan')



plan = model(watchs)

print('Plan un')
for i in plan.plan:
    print(str(i.x[0])+'\t'+ str(i.x[1]) +'\t' +str(i.p))


s = 0
flag = True
while flag:
    grad = Gradient(plan)
    i = 0
    while True:
        #x_max = plan.plan[np.argmax(grad)]
        #x_min = plan.plan[np.argmin(grad)]
                
        
        all_phi  = [Calc_Phi(plan.M,i,plan.f) for i in _x]
        x_max = _x[np.argmax(all_phi)]
        x_min = plan.plan[np.argmin(grad)].x

        plan_i = plan.plan.copy()
        plan_i[np.argmin(grad)].x = x_max
        plan_i = model(plan_i)
        if plan_i.crit_A > plan.crit_A:
            i+=1
            _x.remove(x_max)            
            _x.remove(x_min)
            #plan_i.remove(x_min)
            #plan_i.plan.remove(elem_plan( x_max,1/20))
            plan =model( plan_i.plan)
        elif i == 0:
            flag = False
            break
        else:
            s= s+1
            break


print('Plan after')
for i in plan.plan:
     print(str(i.x[0])+'\t'+ str(i.x[1]) +'\t' +str(i.p))


'''
plot_x = []
plot_y = []
for q in np.arange(0,0.51,0.01):
    if q not in (0.5,-0.5,0):
        plan = np.array([elem_plan(-1, q),
                         elem_plan(-0.5, (1 - 2 * q) / 2.0),
                         elem_plan(0.5, (1 - 2 * q) / 2.0),
                         elem_plan(1, q)])
        D_crit = model(plan).crit_D
        #graphic_info.append((q,D_crit))
        plot_x.append(q)
        plot_y.append(D_crit)
a = 1'''



'''
print("q")
print((plot_y.index(max(plot_y)) + 1) * 0.01)
print("value")
print(max(plot_y))


fig = plt.figure()
plt.plot(plot_x, plot_y)'''