from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup as bs
import os
import sys
from requests import get

def write_file(contents, outname):
	with open(outname, 'w') as outfile:
		outfile.write(contents)

def make_selenium_request(URL):
	options = Options()
	options.add_argument("--headless")
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
		
	return

def fetch_title(soup):
	album_title = soup.find('h1', {'class' : 'loadedComicHeader'}).text.strip()
	return album_title

def debug_program():
	if not os.path.exists("debug.html"):
		request_url = sys.argv[1]
		req = make_selenium_request(request_url)
		soup = bs(req, 'lxml')
		write_file(soup.prettify(), "debug.html")
	with open ("debug.html", 'r') as infile:
		soup = bs(infile.read(), 'lxml')
		source_dir = os.path.expanduser('~') + r'\Documents\Mangas\\' + fetch_title(soup)
		if not os.path.exists(source_dir):
			os.makedirs(source_dir)
		fetch_images(soup, source_dir)
	
def fetch_page_source():
	source_dir = os.path.expanduser('~') + r'\Documents\Mangas'
	if not os.path.exists(source_dir):
		os.makedirs(source_dir)
	
debug_program()