import numpy

# moving average cross crossovers                
class Indicators(object):
    def __init__(self, log=None):
        self.logger = log
        self.state = (int(), int(), int(), int(), int(), int(), int(), int())

    def get_states(self, quotes):
        self.quotes = quotes
        self.state = (self.crossover_indicator(self.quotes, 5, 7),
                      self.crossover_indicator(self.quotes, 5, 20),
                      self.crossover_indicator(self.quotes, 7, 30),
                      self.crossover_indicator(self.quotes, 12, 26),
                      self.crossover_indicator(self.quotes, 50, 100),
                      self.crossover_indicator(self.quotes, 50, 200),
                      self.MACD_sig_line(self.quotes, 12, 26, 9),
                      self.MACD_zero_cross(self.quotes, 12, 26),
                      self.RSI(self.quotes, 14, 25))
        return self.state

    def moving_average(self, size, sliced):
        multiplier = (2/(size + 1))
        ema = 0
        for value in sliced:
            ema = (multiplier*value) + ((1-multiplier)*ema)
        return ema

    def crossover_indicator(self, q, x, y):
        if self.moving_average(x, q[-x:]) < self.moving_average(y, q[-y:]):
            if self.moving_average(x, q[-x-1:-1]) > self.moving_average(y, 
                                                                    q[-y-1:-1]):
                return -1
        elif self.moving_average(x, q[-x:]) > self.moving_average(y, q[-y:]):
            if self.moving_average(x, q[-x-1:-1]) < self.moving_average(y, 
                                                                    q[-y-1:-1]):
                return 1
        return 0

    def print_quotes(self):
        print(crossover_indicator(5, 10))

#https://en.wikipedia.org/wiki/MACD#Mathematical_interpretation
    def MACD(self, q, m1, m2):
        signal = self.moving_average(m1, q[-m1:]) - self.moving_average(m2, q[-m2:])
        return signal

    def MACD_series(self, q, m1, m2):
        series = []
        i = 0
        for quotes in q:
            if m2 < i:
                series[i] = self.moving_average(m1, q[-m1-i:-i]) - self.moving_average(m2, q[-m2-i:-i])
            i += 1
        if m2 < i:                                                
            series[i] = self.MACD(q,m1,m2)                                               
        return series

    def MACD_sig_line(self, q, m1, m2, m3):
        self.MACD_series = self.MACD_series(q, m1, m2)
        if self.MACD(q, m1, m2) < self.moving_average(m3, self.MACD_series[-m2:]):
            if self.MACD(q[:-1], m1, m2) > self.moving_average(m3, self.MACD_series[-m2-1:-1]):
                return -1
        elif self.MACD(q, m1, m2) > self.moving_average(m3, self.MACD_series[-m2:]):
            if self.MACD(q[:-1], m1, m2) < self.moving_average(m3, self.MACD_series[-m2-1:-1]):
                return 1
        return 0

    def MACD_zero_cross(self, q, m1, m2):
        if self.MACD(q[:-1], m1, m2) > 0 and self.MACD(q, m1, m2) < 0:
            return -1
        elif self.MACD(q[:-1], m1, m2) < 0 and self.MACD(q, m1, m2) > 0:
            return 1
        return 0

    def RSI(self, q, period, threshold):
        i = 0
        upcount = 0
        downcount = 0
        updays = []
        downdays = []
        while (upcount <= period and downcount <= period) and i < len(q) - 1:
            if q[1+i] < q[i]:
                updays[upcount] = q[1+i]
                upcount += 1
            elif q[1+i] > q[i]:
                downdays[downcount] = q[1+i]
                downcount += 1
            i += 1
        RS = self.moving_average(period, updays) / self.moving_average(period, downdays)
        RSI = (100-(100/(1+RS)))
        
        if RSI < threshold:
            return 1
        elif RSI > (1-threshold):
            return -1
        return 0
    
                
                
        

    

