import Environment as Env
import numpy as np

bids = {"taxi1": 0.5, "taxi2": 0.6, "taxi3": 0.7}

winner_taxi = max(bids, key=bids.get)

print(winner_taxi)  # taxi3
