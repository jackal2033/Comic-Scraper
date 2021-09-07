from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup as bs
import os
import sys
from requests import get
from re import sub
import html
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def write_file(contents, outname):
	with open(outname, 'w') as outfile:
		outfile.write(contents)

def make_selenium_request(URL):
	options = Options()
	options.add_argument("--headless")
	options.binary=r"C:\Program Files\Mozilla Firefox\firefox.exe"

	driver = webdriver.Firefox(os.getcwd(), options=options)
	driver.get(URL)
	return driver.page_source

def parse_infile():
	infile = ""
	req_dict = []
	for line in infile:
		req_dict.append(line)
	return req_dict

def parse_soup(soup):
	return

def fetch_images(soup, out_dir):
	image_list = []
	for img in soup.find_all(class_="comic-page"):
		image_list.append(img['src'])


	'''
	assume all images use same extension
	if assumption is wrong, it's trivial to move down
	... why don't i do that now xd
	'''
	image_extension = image_list[0].split(".")[-1]
	for i in range(len(image_list)):
		image_name = str(i + 1) + "." + image_extension
		complete_path = out_dir + '\\' + image_name
		with open(complete_path, 'wb') as outfile:
			with get(image_list[i]) as url_image:
				outfile.write(url_image.content)

def fetch_title(soup):
	album_title = soup.find('h1', {'class' : 'loadedComicHeader'}).text.strip()
	album_title = sub('[:-<>.\"\'\\\/\|\*?]', '' , album_title)
	return album_title

def debug_program():
	for URL in sys.argv[1:]:
		print(URL)
		request_url = URL.strip()
		req = make_selenium_request(request_url)
		soup = bs(req, 'lxml')
		source_dir = os.path.expanduser('~') + r'\Documents\Mangas\\' + fetch_title(soup)
		if not os.path.exists(source_dir):
			os.makedirs(source_dir)
		fetch_images(soup, source_dir)
	
def fetch_page_source():
	source_dir = os.path.expanduser('~') + r'\Documents\Mangas'
	if not os.path.exists(source_dir):
		os.makedirs(source_dir)
	
def main():
	with open ("mangas.txt", 'r') as infile:
		for url_line in infile:
			URL = url_line.strip("\n")
			print([URL])
			page_source = make_selenium_request(URL)
			soup = bs(page_source, 'lxml')
			try:
				source_dir = os.path.expanduser('~') + r'\Documents\Mangas\\' + fetch_title(soup)
			except:
				with open("debug.html", 'w') as debug_file:
					debug_file.write(soup.prettify())
					exit()
			if not os.path.exists(source_dir):
				os.makedirs(source_dir)
			fetch_images(soup, source_dir)

if __name__ == "__main__":
	debug_program()