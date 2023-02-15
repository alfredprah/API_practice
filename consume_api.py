import requests;


response = requests.get('https://api.stackexchange.com/2.3/answers?order=desc&sort=activity&site=stackoverflow')

print(response.json())