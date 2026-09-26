import urllib.request
import json

url = "http://localhost:5000/api/generate"
data = {"notes": "The mitochondria is the powerhouse of the cell. DNA stands for Deoxyribonucleic acid."}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as response:
    print("\n🎉 SUCCESS! HERE IS THE AI FLASHCARD JSON OUTPUT:\n")
    print(response.read().decode('utf-8'))
