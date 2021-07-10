import requests
r = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
print(r)
