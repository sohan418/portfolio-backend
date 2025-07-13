import requests

response = requests.get("http://ipinfo.io/ip")
print(response.text.strip())
