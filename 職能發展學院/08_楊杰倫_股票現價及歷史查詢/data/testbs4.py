import requests


def line():
    headers = {"Authorization": "Bearer " + "ZWS0kiaxXS3aKyW0wAhjgBbnsLoV5q5DZMcicm5D1Ke","Content-Type" : "application/x-www-form-urlencoded"}

    params = {"message": "hell"}

    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)

    return r.status_code

a = "15345654"

print(a.find("a"))