import requests
import json

url = 'https://parseapi.back4app.com/classes/Worldzipcode_IT?limit=10&keys=adminCode2,placeName,postalCode'
headers = {
    'X-Parse-Application-Id': 'pX9BoL9aKBRWdqVp0fOmBK5ktvIiVht4lLz1tBEH',
    'X-Parse-REST-API-Key': 'wcI3cIhmOdFGPawZ39Ik6j5NlPykVkrwxmqx9ZnS'
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
print(json.dumps(data, indent=2))
