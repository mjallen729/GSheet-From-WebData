from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

default_link = 'https://www.airbnb.com/wishlists/v/1250433647?s=67&unique_share_id=26a5887d-15af-4bc3-92ef-fa74ea9da81f'

def fetch(airbnb_wishlist= default_link):
	print('Configuring driver...')

	ops = Options()
	ops.add_argument('--headless')
	driver = webdriver.Chrome(options= ops)
	driver.get(airbnb_wishlist)
	driver.implicitly_wait(20)

	df = pd.DataFrame(columns=['Name', 'Location', 'Guests', 'Bedrooms', 'Beds',
							'Baths', 'Price (Night)', 'Price (Total)', 'Link'])

	parent = driver.find_element(By.XPATH, '//*[@id="FMP-target"]/div[1]/div')
	children = parent.find_elements(By.XPATH, '*')

	links = list()

	for element in children:
		link = element.find_element(By.XPATH, './/div[1]/div[1]/a').get_attribute('href')
		links.append(link)

	def get_data(xpath):
		try:
			data = driver.find_element(By.XPATH, xpath).text
		except Exception as e:
			print(e)
			return ''
		
		return data.strip() if data else ''

	print('Fetching data...')

	for link in links:
		driver.get(link)
		data = list()
		
		print(link)

		# Put data into the frame
		data.append(get_data('//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/section/div[1]/span/h1'))
		data.append(driver.find_element(By.CLASS_NAME, '_9xiloll').text.strip()[:-15])  # special case for location (super host badge)
		data.append(int(get_data('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[1]/span[1]')[:-7].strip('+')))
		data.append(int(get_data('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[2]/span[2]')[:-9]))
		data.append(int(get_data('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[3]/span[2]')[:-5]))
		data.append(float(get_data('//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/section/div/div/div/div[1]/ol/li[4]/span[2]')[:-6]))
		data.append(int(get_data('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[1]/div[1]/span[1]/div/button/div')[:6].strip('$').replace('x','').replace(',','')))
		data.append(int(get_data('//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div[3]/div/section/div[2]/div/span[2]/span[1]').strip('$').replace(',','')))
		data.append(link)

		df.loc[len(df)] = data  # append to dataframe

	print('Exporting...')

	df.describe().loc[['count', 'mean', 'min', 'max']].to_csv('./exports/describe.csv')
	df.to_csv('./exports/available_listings.csv')

if __name__ == '__main__':
	fetch()