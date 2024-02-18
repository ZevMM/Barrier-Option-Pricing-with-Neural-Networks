import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#from py_vollib_vectorized import vectorized_implied_volatility as implied_vol

### want to return price, time, risk free rate, european price, barrier price/ prices

file = open(r"Simulated_Price_Data", "a")

# Simulation parameters
N = 252                # number of time steps in simulation
M = 1000               # number of simulations per trial
T = 100                # number of trials

for i in range(T):
    #all of these parameters should be randomized. Should I use ratios throughout? or normalize prices to be ~100?
    # Heston dependent parameters
    kappa = 3              # rate of mean reversion of variance under risk-neutral dynamics
    theta = 0.50**2        # long-term mean of variance under risk-neutral dynamics
    v0 = 0.25**2           # initial variance under risk-neutral dynamics
    rho = 0.8              # correlation between returns and variances under risk-neutral dynamics
    sigma = 0.8            # volatility of volatility

    # Option parameters
    K = 110                # strike price
    B = 170               # knock out price
    S0 = 150.0             # asset price
    T = 1.0                # time in years
    r = 0.04               # risk-free rate

    def heston_model_sim(S0, v0, rho, kappa, theta, sigma,T, N, M):
        """
        Inputs:
        - S0, v0: initial parameters for asset and variance
        - rho   : correlation between asset returns and variance
        - kappa : rate of mean reversion in variance process
        - theta : long-term mean of variance process
        - sigma : vol of vol / volatility of variance process
        - T     : time of simulation
        - N     : number of time steps
        - M     : number of scenarios / simulations
        
        Outputs:
        - asset prices over time (numpy array)
        - variance over time (numpy array)
        """
        # initialise other parameters
        dt = T/N
        mu = np.array([0,0])
        cov = np.array([[1,rho],
                        [rho,1]])

        # arrays for storing prices and variances
        S = np.full(shape=(N+1,M), fill_value=S0)
        v = np.full(shape=(N+1,M), fill_value=v0)

        # sampling correlated brownian motions under risk-neutral measure
        Z = np.random.multivariate_normal(mu, cov, (N,M))

        for i in range(1,N+1):
            S[i] = S[i-1] * np.exp( (r - 0.5*v[i-1])*dt + np.sqrt(v[i-1] * dt) * Z[i-1,:,0] )
            v[i] = np.maximum(v[i-1] + kappa*(theta-v[i-1])*dt + sigma*np.sqrt(v[i-1]*dt)*Z[i-1,:,1],0)
        
        return S, v

    S_p,v_p = heston_model_sim(S0, v0, rho, kappa, theta, sigma,T, N, M)


    fig, (ax1)  = plt.subplots(1, figsize=(12,5))
    time = np.linspace(0,T,N+1)
    ax1.plot(time,S_p)
    ax1.set_title('Heston Model Asset Prices')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Asset Prices')
    plt.show()

    # calculating average option values
    btotal = 0
    etotal = 0
    for n in S_p:
        counted = True
        for m in n:
            if m > B:
                counted = False
        if n[N] > K:
            if counted:
                btotal += (n[N] - K)

    for n in S_p:
        if n[N] > K:
            etotal += (n[N] - K)


    barrier_val = btotal / M
    european_val = etotal / M

    file.write( str(r) + " " + str(T) + " " + str(S0) + " " + str(K) + " " + str(B) + " " + str(european_val) + " " + str(barrier_val))
    file.write('\n')

file.close