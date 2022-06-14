import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as LA
import time
start_time = time.time()

plt.title("Homoclinic trajectory")

eps = 0.01
eps0 = 5e-7

J = [[2.35, 1],[1.35,1]]
w, v = LA.eig(J)

Vu = v[:,0]     # unstable manifold
Vs = v[:,1]     # stable manifold

# Plot the unstable manifold
Hr = np.zeros(shape=(100,150))
Ht = np.zeros(shape=(100,150))
for eloop in range(0,100):

    eps = eps0*eloop

    x_n0 = eps*Vu[0]
    y_n0 = eps*Vu[1]

    Nloop = np.ceil(-6*np.log(eps0)/np.log(eloop+2))
    flag = 1
    cnt = 0

    while flag==1 and cnt < Nloop:
         # тут менять формулу надо 
         # стандарт мэп (Чириков)
        x_n1=x_n0+y_n0+1.35*x_n0*(1-x_n0)
        y_n1=y_n0+1.35*x_n0*(1-x_n0)

        x_n0 = x_n1
        y_n0 = y_n1

        if y_n1 > 4*np.pi:
            flag = 0

        Hr[eloop,cnt] = x_n0
        Ht[eloop,cnt] = y_n0
        cnt = cnt+1

# x = Hr[0:11,12]
# y = Ht[0:11,12]
x = Hr[0:99,12]
y = Ht[0:99,12]

plt.plot(x,y,linewidth=0.75,color="black", label="Unstable manifold")
plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)

# Plot the stable manifold
del Hr, Ht
del x,y
Hr = np.zeros(shape=(100,150))
Ht = np.zeros(shape=(100,150))

for eloop in range(0,100):
    eps = eps0*eloop
 
    x_n0 = eps*0.83125573
    y_n0 = eps*(-0.4438839)

    Nloop = np.ceil(-6*np.log(eps0)/np.log(eloop+2))
    flag = 1
    cnt = 0

    while flag==1 and cnt < Nloop:
         
        x_n1=x_n0-y_n0
        y_n1=y_n0-1.35*x_n1*(1-x_n1)

        x_n0 = x_n1
        y_n0 = y_n1
         
        if y_n1 > 4*np.pi:
            flag = 0 
        Hr[eloop,cnt] = x_n0
        Ht[eloop,cnt] = y_n0
        cnt = cnt+1

# x = Hr[0:9,12]
# y = Ht[0:9,12]
x = Hr[0:79,12]
y = Ht[0:79,12]

plt.plot(x,y,linewidth =0.75, color="red",label="Stable manifold")
plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)

# хитрожоперство
# plt.scatter(0.416, -0.576, color="green", s=8)      #1
# plt.scatter(0.653, -0.691, color="green", s=8)      #2
plt.scatter(1.3784, -0.0088, color="green", s=8)    #3-середина
# plt.scatter(1.58053, 0.6071, color="green", s=8)    #4
# plt.scatter(1.36841, 0.70763, color="green", s=8)   #5
# plt.scatter(0.664819, 0.41285, color="green", s=8)  #6
# plt.scatter(0.9612, -0.6199, color="green", s=8)    #7
# plt.scatter(0.96884, 0.572, color="green", s=8)     #8
# plt.scatter(0.25474, -0.407278, color="green", s=8)  #9

# plt.grid()
plt.xlim(-1.4,3.2)
plt.ylim(-2.45,2.45)
print("Time elapsed: ", (time.time() - start_time))
plt.show()
