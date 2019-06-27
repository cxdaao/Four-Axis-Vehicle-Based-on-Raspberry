import numpy as np


class filter():
    def __init__(self):
        #pass
        # intial parameters
        self.n_iter = 20
        self.sz = (self.n_iter,) # size of array
        self.x = 1.0
        self.Q = 1e-8# process variance

        # allocate space for arrays
        self.z = np.zeros(self.sz)       # observations (normal about x, sigma=0.1)
        self.xhat=np.zeros(self.sz)      # a posteri estimate of x
        self.P=np.zeros(self.sz)         # a posteri error estimate
        self.xhatminus=np.zeros(self.sz) # a priori estimate of x
        self.Pminus=np.zeros(self.sz)    # a priori error estimate
        self.K=np.zeros(self.sz)         # gain or blending factor

        self.R = 0.1**2 # estimate of measurement variance, change to see effect

    #filter start
    def usefilter(self, z):
       # intial guesses
       self.z = z
       self.xhat[0] = 0.0
       self.P[0] = 1.0
       for k in range(1, self.n_iter):
          # time update
          self.xhatminus[k] = self.xhat[k-1]  #X(k|k-1) = AX(k-1|k-1) + BU(k) + W(k),A=1,BU(k) = 0
          self.Pminus[k] = self.P[k-1]+self.Q      #P(k|k-1) = AP(k-1|k-1)A' + Q(k) ,A=1

        # measurement update
          self.K[k] = self.Pminus[k]/( self.Pminus[k]+self.R ) #Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R],H=1
          self.xhat[k] = self.xhatminus[k]+self.K[k]*(z[k]-self.xhatminus[k]) #X(k|k) = X(k|k-1) + Kg(k)[Z(k) - HX(k|k-1)], H=1
          self.P[k] = (1-self.K[k])*self.Pminus[k] #P(k|k) = (1 - Kg(k)H)P(k|k-1), H=1
       return self.xhat#[self.n_iter - 1]

    def check(self, z):
        if(len(z) < self.n_iter):
            return -1
        else:
            return 1

    def circuit(self, new):
        try:
            return self.usefilter(new)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    # ts = time.clock()
    filter = filter()
    for i in range(10):
        x = 1.0 # truth value (typo in example at top of p. 13 calls this z)
        sz = (20,)  # size of array
        z = np.random.normal(x, 0.15, size=sz) # observations (normal about x, sigma=0.1)
        #xhat = filter.usefilter(z)
        xhat = filter.circuit(z)
        #z = [0.9, 0.8, 1.1, 0.7, 0.8, 1.2]
        #xhat = filter.circuit(z)
    # te = time.clock()
    # print('time cost:', te-ts/1000000, 's')
    # plt.figure()
    # plt.plot(z, 'k+', label='noisy measurements')
    # plt.plot(xhat, 'b-', label='a posteri estimate')
    # plt.axhline(x, color='g', label='truth value')
    # plt.legend()
    # plt.xlabel('Iteration')
    # plt.ylabel('Voltage')
    # plt.show()
