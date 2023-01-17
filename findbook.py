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
isbn = '9789571077611'  # input("Enter ISBN: ").strip()
print(isbn)
with urllib.request.urlopen(base_api_link + isbn) as f:
    time.sleep(1)
    text = f.read()
soup = BeautifulSoup(text, 'html.parser')
print(soup)
if soup is None:
    print("Can't Searched")
else:
    print('Searched')
    bookinfo = soup.find("ul", id="prodInfo2")
    if bookinfo is None:
        bookinfo = soup.find('table', class_='ISBNHead')
    bookinfo=bookinfo.get_text()    



title = soup.find('span', class_='b_name').text
image = soup.find('img', class_='searchImg').get('src')
price = max([int(p.find('div').text.strip('$').strip()) for p in soup.find_all('td', class_='IPrice')])

authors_regex = r"作者： ?(\S*)"
publisher_regex = r"出版社： ?(\S*)"
publishedDate_regex = r"出版日期：(\d{4}-\d{2}-\d{2})"
print(bookinfo)
authors = "None" if re.search(
    authors_regex, bookinfo) is None else re.search(authors_regex, bookinfo).group(1)
publisher = "None" if re.search(publisher_regex, bookinfo) is None else re.search(
    publisher_regex, bookinfo).group(1)
publishedDate = "None" if re.search(publishedDate_regex, bookinfo) is None else re.search(
    publishedDate_regex, bookinfo).group(1)

print("\nTitle:", title)
print("\nSummary:")
print("Image:", image)
print("Price:", price)
print("Author(s):",authors)
print("Publisher:", publisher)
print("PublishedDate:", publishedDate)
print("ISBN:", isbn)
print("\n***")
