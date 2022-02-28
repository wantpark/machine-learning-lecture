#!/usr/bin/env python3

import json
import requests
from requests.exceptions import HTTPError
import shortuuid

serverIP = "10.211.55.13"

ae = "ae_test_II"
cnt = "cnt"


def run(data):
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "req" + shortuuid.ShortUUID().random(length=10),
        "X-M2M-Origin": ae,
        "Content-Type": "application/json;ty=4"
    }

    data = {
        "m2m:cin": {
            "con": data
        }
    }

    try:
        response = requests.request("post",
                                    "http://" + serverIP + ":7579/Mobius/" + ae + "/" + cnt + "?rcn=1",
                                    data=json.dumps(data),
                                    headers=headers,
                                    verify=False)

        print(response.text)

    except HTTPError as error:
        print(f"HTTP error occurred: {error}")
    except Exception as error:
        print(f"Other error occurred: {error}")
