import urllib.request
from bs4 import BeautifulSoup
import re

title = ''
image = ''
price = ''
authors = ''
publishedDate = ''
publisher = ''
user_input = ''

base_api_link = "https://www.kingstone.com.tw/search/key/"
user_input = input("Enter ISBN: ").strip()
base_api_link_post = '/dis/list/zone/book'
print(user_input)
with urllib.request.urlopen(base_api_link + user_input+base_api_link_post) as f:   
    text = f.read()
soup = BeautifulSoup(text, 'html.parser')

bookpage = soup.find("section", class_='searchresultnofield resultno')

if bookpage!=None:
    print("Can't Searched")
else:
    ('Searched')

bookpage = soup.find("h3", class_='pdnamebox').find('a').get('href')
pagelink = 'https://www.kingstone.com.tw'+bookpage

with urllib.request.urlopen(pagelink) as f:
    text = f.read()
soup = BeautifulSoup(text, 'html.parser')

title = soup.find('h1', class_='pdname_basic').text
image = soup.find('a', class_='glightbox').get('href')
price = soup.find('div', class_='basicfield').find('b').text
bookData = soup.select('div.beta_main>div.basicarea>div.basiccolumn>ul.basiccol>li.basicunit')
Data=''
for i in bookData:
    Data+=i.text
    
authors_regex = r"作者： (\S*)\s* 追蹤作者"
publisher_regex = r"出版社： (\w*)\s* 追蹤出版社"
publishedDate_regex = r"出版日：(\d+\/\d+\/\d+)"

authors = re.search(authors_regex, Data) if authors!=None else re.search(authors_regex, Data).group(1)
publisher = re.search(publisher_regex, Data) if publisher != None else re.search(publisher_regex, Data).group(1)
publishedDate = re.search(publishedDate_regex, Data) if publishedDate != None else re.search(publishedDate_regex, Data).group(1)

print("\nTitle:", title)
print("\nSummary:")
print("Image:", image)
print(f"Price: {price} 元")
print("Author(s):",authors)
print("PublishedDate:", publishedDate)
print("Publisher:", publisher)
print("\n***")

