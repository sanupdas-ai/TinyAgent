import json
import urllib.request

data = json.dumps(
  {
    "model": "gemma4:e4b",
    "messages": [{"role": "user", "content": "Hi! How's life?"}]
  }
).encode("utf-8")

req = urllib.request.Request(
  url = "http://localhost:11434/v1/chat/completions",
  data = data,
  headers = {"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as response:
  result = json.loads(response.read())
  
print(result["choices"][0])