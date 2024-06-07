
import requests

url = 'https://www.drodd.com/images11/meme-faces8.png'
r = requests.get(url, allow_redirects=True)
open('image.png', 'wb').write(r.content)

