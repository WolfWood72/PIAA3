import numpy as np

class elem_plan(object):
    def __init__(self,x=None,p=None):
        self.x = x
        self.p = p




class model(object):

          

    def __init__(self,plan):
        self.plan = plan  
        self.n_plan = len(plan)
        self.m = len(self.f((0,0)))  
        self.Make_M()
        self.Make_D()
        self.Calc_Criterium()

    def f(self,x):
        return np.array([1,x[0],x[1],x[0] * x[1],x[0] * x[0],x[1] * x[1]])
    
    def Make_M(self):
        M = np.zeros((self.m,self.m))
        for k in range(self.n_plan):
            f = self.f(self.plan[k].x)
            for i in range(self.m):
                    M[i] += self.plan[k].p * f[i] * f
        self.M = M
    def Make_D(self):
        self.D = np.linalg.inv(self.M)

    def Calc_Criterium(self):
       self.crit_D = self.Calc_D()
       self.crit_A = self.Calc_A()
       self.crit_E = self.Calc_E()
       self.crit_Ф = self.Calc_Ф()
       self.crit_Lymbda = self.Calc_Lymabda()
       self.crit_MV = self.Calc_MV()
       self.crit_G = self.Calc_G()
       self.sum_crit = self.crit_D + self.crit_A + self.crit_E + self.crit_Ф + self.crit_Lymbda+   self.crit_MV + self.crit_G




    def Calc_D(self):
        return  np.linalg.det(self.M)
    def Calc_E(self):
        return np.max(np.linalg.eig(self.D)[0])
    def Calc_A(self):
        return -1*self.D.trace()
    def Calc_Ф(self, p=2):
        return ((1.0 / self.m)* (self.D**p).trace())** (1.0/p)
    def Calc_Lymabda(self):
        return np.sum((np.linalg.eig(self.D)[0] - np.average(np.linalg.eig(self.D)[0]))**2 )
    def Calc_MV(self):
        return np.max(np.diag(self.D))
    def Calc_G(self):
        def d(x):
            return self.f(x).T @ self.D @ self.f(x)
        return np.max([ d(self.plan[i].x) for i in range(self.n_plan)])
