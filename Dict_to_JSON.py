import requests

resp = requests.get('http://localhost:5000/p1').json()

print(type(resp))

resp = json.dumps(resp)

print(type(resp))
