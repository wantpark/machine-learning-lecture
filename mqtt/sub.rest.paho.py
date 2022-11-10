import json
import requests
from requests.exceptions import HTTPError
import shortuuid

serverIP = "192.168.0.18"

ae = "ae_test"
cnt = "cnt_test"
sub = "sub_test"

data = {
    "m2m:sub": {
        "rn": sub,
        "enc": {
            "net": [3],
        },
        "nu": ["mqtt://" + serverIP + ":1883/" + ae + "/" + cnt + "/" + sub],
        "nct": 1,
        "pn": 1
    }
}


if __name__ == "__main__":
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "req" + shortuuid.ShortUUID().random(length=10),
        "X-M2M-Origin": ae,
        "Content-Type": "application/json;ty=23"
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
