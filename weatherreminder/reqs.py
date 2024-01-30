import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2NjA4MDk4LCJpYXQiOjE3MDY2MDc3OTgsImp0aSI6IjBmMWE5Yzc5MGJiZDQ2ZWE4NGJjOTZkMTJkZGUwN2Q3IiwidXNlcl9pZCI6MX0.b-5jimM4Oe6cYbSGHUzDvsy-CrSHgfu62Exz2fzedsA"

headers = {"Authorization": f"Bearer {token}"}

# data = {"period_notifications": 1}
# response = requests.post("http://localhost/api/subscription/", headers=headers, data=data)
# data = {"period_notifications": 3}
# response = requests.post("http://localhost/api/subscription/", headers=headers, data=data)
# data = {"period_notifications": 6}
# response = requests.post("http://localhost/api/subscription/", headers=headers, data=data)
#
# data = {'name': 'Kyiv'}
# response = requests.post("http://localhost/api/subscription/1/cities/", headers=headers, data=data)
# data = {'name': 'Dnipro'}
# response = requests.post("http://localhost/api/subscription/2/cities/", headers=headers, data=data)
# data = {'name': 'Nikopol'}
# response = requests.post("http://localhost/api/subscription/2/cities/", headers=headers, data=data)
# data = {'name': 'London'}
# response = requests.post("http://localhost/api/subscription/3/cities/", headers=headers, data=data)
# data = {'name': 'Berlin'}
# response = requests.post("http://localhost/api/subscription/3/cities/", headers=headers, data=data)


response = requests.get("http://localhost/api/subscription/2/get_weather/Nikopol", headers=headers)
print(response.json())
