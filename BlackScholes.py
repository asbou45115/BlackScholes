import numpy as np
from scipy.stats import norm

# ----------- Black-Scholes Pricing ------------
class BlackScholes:
    '''
    S: spot price,
    K: strike price,
    r: risk-free interest rate,
    t: time to maturity,
    sigma: volatility
    '''
    def __init__(self, S, K, r, t, sigma):
        self.S = S
        self.K = K
        self.r = r
        self.t = t
        self.sigma = sigma

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.t) / (self.sigma * np.sqrt(self.t))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.t)

    def call_price(self):
        if self.t <= 0:
            return max(0, self.S - self.K)
        d1, d2 = self.d1(), self.d2()
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.t) * norm.cdf(d2)

    def put_price(self):
        if self.t <= 0:
            return max(0, self.K - self.S)
        d1, d2 = self.d1(), self.d2()
        return self.K * np.exp(-self.r * self.t) * norm.cdf(-d2) - self.S * norm.cdf(-d1)