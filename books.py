import urllib.request
from bs4 import BeautifulSoup
import re
import csv

with open('output.csv', 'r+', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if csvfile != ['書名', '價錢', '封面', '作者', '出版日期', '出版社']:
        csvfile.truncate()
        writer.writerow(['書名', '價錢', '封面', '作者', '出版日期', '出版社'])

while True:

    base_api_link = "https://search.books.com.tw/search/query/cat/1/sort/1/v/0/page/1/spell/3/key/"
    user_input = input("Enter ISBN: ").strip()

    with urllib.request.urlopen(base_api_link + user_input) as f:   
        text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    tbody = soup.find_all("tbody", id=re.compile("itemlist_*"))
    for i in tbody: 
        booknumber=i.find('input').get('value')
    bookpage = 'https://www.books.com.tw/products/'+booknumber+'?sloc=main'
    with urllib.request.urlopen(bookpage) as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    title=soup.find('div', class_='mod type02_p002 clearfix').find('h1').text
    image=soup.find('img', class_='cover M201106_0_getTakelook_P00a400020052_image_wrap').get('src') 
    price = soup.find('ul', class_='price').find('em').text
    authors = soup.find('div', class_='type02_p003 clearfix').find(
    'ul').find('li').find('a', href=re.compile('//search.books.com.tw/search/query/key/*')).text
    publisher = soup.find('div', class_='type02_p003 clearfix').find(
    'ul').find('li').find_next_sibling('li').find('span').text
    publishedDate = soup.find('div', class_='type02_p003 clearfix').find(
    'ul').find('li').find_next_sibling('li').find_next_sibling('li').text.split('：')[-1]

    print("\nTitle:", title)
    print("\nSummary:")
    print(f"Price: {price} 元")
    print("Image:", image)
    print("Author(s):",authors)
    print("PublishedDate:", publishedDate)
    print("Publisher:", publisher)
    print("\n***")

    with open('output.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([title,price,image,authors,publishedDate,publisher])

    
    status_update = input("\nEnter another ISBN? y or n: ").lower().strip()
    if status_update == "n":
        print("\nThank you! Have a nice day.")
        break
