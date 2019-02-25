import matplotlib.pyplot as plt
import numpy as np

if __name__=="__main__":
    dc = 0.8
    dt = 0.025
    T = 1
    Stroke = 12

    Xs = []
    Ys = []

    t = np.array(range(0,10))/1.0

    for t_current in t:
        x = Stroke/2 + Stroke/dc*(-t_current)
        print(x)
        Xs.append(x)
        Ys.append(t)
        # plt.scatter(t,x)

    plt.scatter(Xs,Ys)

    plt.show()
