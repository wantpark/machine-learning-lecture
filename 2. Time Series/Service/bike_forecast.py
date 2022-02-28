#!/usr/bin/env python3

import json

from prophet.serialize import model_from_json
from scipy.special import inv_boxcox


lam = 0.45166936452584744


def run(rain, temp):
    fin = open('bike_rental.json', 'r')

    m = model_from_json(json.load(fin))

    # next day
    future = m.make_future_dataframe(periods=1, freq='D')

    # add regressor for prediction
    future['rain'] = rain
    future['temp'] = temp

    forecast = m.predict(future)

    # Transform back to reality from Box Cox
    forecast[['yhat', 'yhat_upper', 'yhat_lower']] = forecast[[
        'yhat', 'yhat_upper', 'yhat_lower']].apply(lambda x: inv_boxcox(x, lam))

    # demand forecasting
    result = forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower']].iloc[-1:]
    # print(result)

    # to string type of JSON
    result = result.to_json(orient='records')
    result = json.dumps(result)
    result = result.replace('[', '')
    result = result.replace(']', '')
    result = result.replace('\\', '')
    result = result[1:-1]

    return result
