from bs4 import BeautifulSoup
import requests
import re
import json
import time

url = "https://en.wikipedia.org/wiki/List_of_companion_plants"

results_page = requests.get(url)
results_page_html = results_page.text
soup = BeautifulSoup(results_page_html, "html.parser")
tables = soup.find_all('tbody')
time.sleep(10)

column_map = [ "Common name", "Scientific name", "Helps", "Helped by",
"Attracts", "-Repels/+distracts", "Avoid", "Comments"]

data_tr = soup.find_all('tr')

data_split = {
	'vegetables': data_tr[2:44],
	'fruit': data_tr[46:55],
	'herbs': data_tr[57:89],
	'flowers': data_tr[91:111],
	'other': data_tr[113:116]
}

def export(name):
	all_my_data = []

	for row in data_split[name]:
		my_data = {}
		data = row.find_all('td')

		for index, column in enumerate(data):
			label = column_map[index]
			my_data[label] = column.text

		all_my_data.append(my_data)

	with open(f'companion_plants_{name}.json', 'w') as f_object:
		json.dump(all_my_data, f_object, indent=2)

	print(f'Your file companion_plants_{name}.json is now ready')

for name in data_split.keys():
	export(name)
