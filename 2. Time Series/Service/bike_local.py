#!/usr/bin/env python3

import bike_forecast
import bike_store

rain = 0.0
temp = 10.0

result = bike_forecast.run(rain, temp)
print(result)

# bike_store.run(result)
