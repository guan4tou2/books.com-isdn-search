import urllib.request
from bs4 import BeautifulSoup
import re
import csv
import time

with open('output.csv', 'r+', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if csvfile != '書名,封面,價錢,作者,出版日期,出版社,ISBN':
        csvfile.truncate()
        writer.writerow(['書名', '封面', '價錢', '作者', '出版日期', '出版社','ISBN'])

with open('input.csv', 'r', encoding='utf-8', newline='') as csvfile:
    reader=csv.reader(csvfile)

    for isbn in reader:
        title = ''
        image = ''
        price = ''
        authors = ''
        publishedDate = ''
        publisher = ''
        isbn = ''.join(isbn).strip()

        base_api_link = "https://findbook.com.tw/"
        print(isbn)
        with urllib.request.urlopen(base_api_link + isbn) as f:
            text = f.read()
        soup = BeautifulSoup(text, 'html.parser')
        
        
        if soup is None:
            print("Can't Searched")
            with open('./cantsearch.csv', 'a+', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Can't Searched:", isbn])
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

            authors = "None" if re.search(authors_regex, bookinfo) is None else re.search(authors_regex, bookinfo).group(1)
            publisher = "None" if re.search(publisher_regex, bookinfo) is None else re.search(publisher_regex, bookinfo).group(1)
            publishedDate = "None" if re.search(publishedDate_regex, bookinfo) is None else re.search(publishedDate_regex, bookinfo).group(1)

            print("Title:", title)
            # print("\nSummary:")
            # print("Image:", image)
            # print("Price:", price)
            # print("Author(s):",authors)
            # print("Publisher:", publisher)
            # print("PublishedDate:", publishedDate)
            # print("ISBN:", isbn)
            print("***\n")

            with open('./output.csv', 'a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([title, '[img]'+image+'[/img]', price, authors,publishedDate, publisher, isbn])

            time.sleep(1)

print("Done!!!")
