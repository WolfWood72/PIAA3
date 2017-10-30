import numpy as np
from  IO import *
from model import *
import matplotlib.pyplot as plt


def f(x):
    return np.array([1,x[0],x[1],x[0] * x[1],x[0] * x[0],x[1] * x[1]])
    
def Make_M(x_arr,p_arr,n,m):
    M = np.zeros((m,m))
    for k in range(len(x_arr)):
        _f = f(x_arr[k])
        for i in range(m):
                M[i] += p_arr[k] * _f[i] * _f
    return M
def Make_D(M):
    return np.linalg.inv(M)


def Make_points(n,X):
    return [ random.choice(X) for i in range(n)]

def Gradient(X,P):
    n = 6
    M = Make_M(X,P,len(X),n)
    tt = np.linalg.inv(M)**2
    gradient = []
    for i in X:
        _f = f(i)
        gradient.append(_f.T@(tt)@_f)
    return gradient


def Calc_Phi(M,x):
    _f = f(x)
    tt = np.linalg.inv(M)**2
    return  _f.T@(tt)@_f

def Calc_Crit_A(D):
    return  -1*D.trace()


n = 20
X = []
P = [1/n]*n
grid_1 = np.linspace(-1,1,11)
grid = []
for i in grid_1:
    for j in grid_1:
        grid.append((i,j))

X = Make_points(n,grid)

print('Plan un')
for i in range(n):
    print(str(X[i][0])+'\t'+ str(X[i][1]) +'\t' +str(P[i]))


s = 0
flag = True
add_plan = []
flags_grid = [True]*len(grid_1)**2
flags_gradient = [True]*n 
while flag:
    grad = Gradient(X,P)
    i_com = 0
    while True:
        M_i = Make_M(X,P,n,6)
        D_i = Make_D(M_i)
        A_i = Calc_Crit_A(D_i)
        all_phi  = [Calc_Phi(M_i,i) for i in grid]
        #x_max = grid[np.argmax(all_phi)]
        #x_min = X[np.argmin(grad)]
        ind_start = 0
        for i in range(len(flags_grid)):
            if flags_grid[i] == True:
                ind_start = i
                break



        x_max = all_phi[ind_start]
        point_max = grid[ind_start]
        index_max = ind_start
        for i in range(len(all_phi)):
            if flags_grid[i] == True and x_max < all_phi[i]:
                x_max = all_phi[i]
                point_max = grid[i]
                index_max = i

        ind_start = 0
        for i in range(len(flags_gradient)):
            if flags_gradient[i] == True:
                ind_start = i
                break


        x_min = grad[ind_start]
        index_min = ind_start
        for i in range(len(grad)):
            if flags_gradient[i] == True and x_min > grad[i]:
                x_min = grad[i]
                index_min = i


        
        #X[np.argmin(grad)] = x_max

        X[index_min] = point_max
        M_i_1 = Make_M(X,P,n,6)
        D_i_1 = Make_D(M_i_1)
        A_i_1 = Calc_Crit_A(D_i_1) 
            

        if A_i_1 > A_i:
            i_com+=1
            flags_grid[index_max] = False
            flags_gradient[index_min] = False
            #grid.remove(x_max) 
            #add_plan.append(x_max)
           # X.remove(x_max)
            #P.pop()
        elif i_com == 0:
            flag = False
            break
        else:
            s= s+1
            break

            
            
            
            




print('Plan after')
for i in range(len(X)):
    print(str(X[i][0])+'\t'+ str(X[i][1]) +'\t' +str(P[i]))