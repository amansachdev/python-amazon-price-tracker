import requests
import random
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)
url = 'https://httpbin.org/headers'
p = requests.get(url, headers={
	'useragent':random_line('user-agents.txt') })
		#'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36' })
print(p.text)