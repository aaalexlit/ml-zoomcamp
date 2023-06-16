import requests

ride = {
    "PULocationID": 43,
    "DOLocationID": 151,
    "trip_distance": 1.01
}
url = 'http://127.0.0.1:9696/predict'
response = requests.post(url, json=ride)

print(response.json())