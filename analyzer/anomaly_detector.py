from collections import deque
import statistics

class SlidingWindowZScore:
    def __init__(self, window_size=10, threshold=3):
        self.window = deque(maxlen=window_size)
        self.threshold = threshold

    def add_value(self, value):
        self.window.append(value)
        if len(self.window) < 3:  
            return False

        mean = statistics.mean(self.window)
        std = statistics.stdev(self.window)
        if std == 0:  
            return False

        z_score = (value - mean) / std
        return abs(z_score) > self.threshold
