import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-whitegrid')


def main():
    # ```
    # ndc = X ; a random variable drown from a normal distribution with a mean of $O_c$ and std of $whatever$
    # N = number of nodes
    # tot= 0  # total on time

    # for (n =0; n < N; n++)
    #     tot = (1 - tot) * ndc + t
    # ```

    fontSize = 16 

    ndc=0.1-0.03
    n=10

    # the average benefit of adding an INode is tot = (1-tot) * ndc +tot

    fig, ax1 = plt.subplots(figsize=(8,4))
        
    for i in np.arange(1,6):
        ax1.plot(range(1,n+1), tot(n,ndc*i), '-o', label="on/off cycle={:0.1f}".format(ndc*i))

    ax1.xaxis.set_major_locator(ticker.FixedLocator(np.arange(0,21,4)))
    # 

    y1Locs = np.arange(-0,2+0.1,step=0.1)
    y1Value = np.around(np.arange(0,2+0.1,step=0.1), decimals=1)

    def funcFormatter(val, idx):
        return "{:4d}%".format(int(val*100))

    ax1.grid(linestyle=':')
    ax1.legend( fontsize=fontSize)
    plt.xlabel('Number of Nodes',  fontsize=fontSize)
    plt.ylabel('Availability Duty Cycles',  fontsize=fontSize)

    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(funcFormatter))

    ax1.tick_params(axis='both', which='major', labelsize=14)

    plt.tight_layout()
    plt.savefig('figures/cisModel.eps')

def tot(n,ndc):
    assert (n >0 and ndc <= 1)
    t=0
    coverage=[]
    for i in range(n):
#         t = (1 - t) * (np.random.randn() * (ndc/4.) + ndc) +t
        t = t + (1 - t) * ndc
        if i == 9:
            print(t)
        coverage.append(t)
    return coverage





if __name__ == '__main__':
    main()




























