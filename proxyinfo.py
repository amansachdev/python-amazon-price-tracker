import proxies
import requests
from proxies import random_proxy
from scraper_api import ScraperAPIClient
import random
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

client = ScraperAPIClient('d0224166b175ddca1f18dd5b5cca66a5')
result = client.get(url = 'http://httpbin.org/headers', 
	headers={
	'useragent':random_line('user-agents.txt') }
	)
print(result.text);


