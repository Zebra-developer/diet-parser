import csv
import json
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randrange


#url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
}

#req = requests.get(url, headers=headers)

#src = req.text
#print(src)

#with open('index.html', 'w', encoding='utf-8') as file:
#	file.write(src)

#with open('index.html', 'r', encoding='utf-8') as file:
#	src = file.read()

#soup = BeautifulSoup(src, 'lxml')
#all_product = soup.find_all(class_='mzr-tc-group-item-href')

#product_url_dict = {}

#for item in all_product:
#	item_index = item.text
#	item_url = 'https://health-diet.ru' + item.get('href')
	
#	product_url_dict[item_index] = item_url

#with open('product_url.json', 'w', encoding='utf-8') as file:
#	json.dump(product_url_dict, file, indent=4, ensure_ascii=False)

with open('product_url.json', encoding='utf-8') as file:
	all_categories = json.load(file)

interation_count = int(len(all_categories)) - 1
count = 0
print(f'Всего: {interation_count}')

for name, url in all_categories.items():
	rep = [',', ' ', '.', '-', "'"]
	for item in rep:
		if item in name:
			name = name.replace(item, '_')
	

	req = requests.get(url=url)
	src = req.text

	with open(f'data/{count}_{name}.html', 'w', encoding='utf-8') as file:
		file.write(src)

	with open(f'data/{count}_{name}.html', 'r', encoding='utf-8') as file:
		src = file.read()

	soup = BeautifulSoup(src, 'lxml')

	# проверка страницы на наличие таблицы с продуктами 
	alert_block = soup.find(class_='uk-alert-danger')
	if alert_block is not None:
		continue

	# собираем заголовки таблицы
	table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
	product = table_head[0].text
	calories = table_head[1].text
	proteins = table_head[2].text
	fats = table_head[3].text
	carb = table_head[4].text


	with open(f'data/{count}_{name}.csv', 'w', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(
			(
				product,
				calories,
				proteins,
				fats,
				carb
				)
			)

	# собираем данные продуктов 
	products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

	product_info = []

	for item in products_data:
		product_tbs = item.find_all('td')

		title = product_tbs[0].find('a').text
		calories = product_tbs[1].text
		proteins = product_tbs[2].text
		fats = product_tbs[3].text
		carb = product_tbs[4].text


		product_info.append(
			{
			'Title': title,
			'Calories': calories,
			'Proteins': proteins,
			'Fats': fats,
			'Carb': carb
			}
		)


		with open(f'data/{count}_{name}.csv', 'a', encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerow(
				(
					title,
					calories,
					proteins,
					fats,
					carb
					)
				)

	with open(f'data/{count}_{name}.json', 'a', encoding='utf-8') as file:
		json.dump(product_info, file, indent=4, ensure_ascii=False)


	count += 1
	print(f'Итерация: {count}. {name} записан...')
	interation_count -= 1

	if interation_count == 0:
		print('Работа закончена.')
		break

	print(f'Осталоcь итераций: {interation_count}')
	sleep(randrange(2, 4))