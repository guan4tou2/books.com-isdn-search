import urllib.request
import re
from bs4 import BeautifulSoup
import time

title = ''
image = ''
price = ''
authors = ''
publishedDate = ''
publisher = ''
isbn = ''

base_api_link = "https://findbook.com.tw/"
isbn = input("Enter ISBN: ").strip()
print(isbn)
with urllib.request.urlopen(base_api_link + isbn) as f:
    text = f.read()
soup = BeautifulSoup(text, 'html.parser')

if soup==None:
    print("Can't Searched")
else:
    print('Searched')
    time.sleep(1)

title = soup.find('span', class_='b_name').text
image = soup.find('img', class_='searchImg').get('src')
price = max([int(p.find('div').text.strip('$').strip()) for p in soup.find_all('td', class_='IPrice')])
bookinfo = soup.find("ul", id="prodInfo2").get_text()

authors_regex = r"作者： (\S*)"
publisher_regex = r"出版社： (\S*)"
publishedDate_regex = r"出版日期：(\d{4}-\d{2}-\d{2})"

authors = re.search(authors_regex, bookinfo) if authors is None else re.search(authors_regex, bookinfo).group(1)
publisher = re.search(publisher_regex, bookinfo) if publisher is None else re.search(publisher_regex, bookinfo).group(1)
publishedDate = re.search(publishedDate_regex, bookinfo) if publishedDate is None else re.search(publishedDate_regex, bookinfo).group(1)

print("\nTitle:", title)
print("\nSummary:")
print("Image:", image)
print("Price:", price)
print("Author(s):",authors)
print("Publisher:", publisher)
print("PublishedDate:", publishedDate)
print("ISBN:", isbn)
print("\n***")
