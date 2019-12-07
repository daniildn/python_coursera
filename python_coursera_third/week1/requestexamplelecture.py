import json

import requests


r = requests.get("http://httpbin.org/get")
print(r.text)

r = requests.post("http://httpbin.org/post")
print(r.text)

r = requests.get("http://httpbin.org/get", params={"key": "value"})
print(r.text)

r = requests.put("http://httpbin.org/put", data={"key": "value"})
print(r.text)

r = requests.put("http://httpbin.org/put", json={"key": "value"})
print(r.text)

r = requests.post("http://httpbin.org/post", data=json.dumps({"key": "value"}))
print(r.text)

try:
    url = "http://httpbin.org/post"
    files = {"file": ("text.txt", open("", "rb"))}

    r = requests.post(url, files=files)
    print(r.text)

    headers = {"user-agent": "my-app/0.0.1"}

    r = requests.get("http://httpbin.org/get", headers=headers)
    print(r.text)
except:
    pass

r = requests.get("http://httpbin.org/get")
print(type(r.text), r.text)
print(type(r.content), r.content)
print(type(r.json()), r.json())
print("------------------ ------------------------------------------")

print(r.status_code)

cookies = dict(cookies_are="working")
r = requests.get("http://httpbin.org/cookies", cookies=cookies)

print(r.text)


s= requests.Session()
s.get("http://httpbin.org/cookies/set/sessioncookie/123456789")
r = s.get("http://httpbin.org/cookies")
print(s.cookies)
print(r.text)

s= requests.Session()
s.headers.update({"x-test2":"true"})
r = s.get("http://httpbin.org/headers", headers={"x-test2":"true"})
print(r.text)