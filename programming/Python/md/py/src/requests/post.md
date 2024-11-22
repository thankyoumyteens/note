# formdata

```python
import requests

payload = {
    'key1': 'value1',
    'key2': 'value2'
}
r = requests.post("http://httpbin.org/post", data=payload)
print(r.text)
```

# json

```python
import requests
import json

url = 'https://api.github.com/some/endpoint'
payload = {
    'some': 'data'
}
r = requests.post(url, data=json.dumps(payload))
print(r.text)
```
