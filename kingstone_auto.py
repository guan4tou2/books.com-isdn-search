import urllib.request
from bs4 import BeautifulSoup
import re
import csv

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
        user_input = ''.join(isbn).strip()

        base_api_link = "https://www.kingstone.com.tw/search/key/"
        base_api_link_post = '/dis/list/zone/book'
        print(user_input)
        with urllib.request.urlopen(base_api_link + user_input+base_api_link_post) as f:   
            text = f.read()
        soup = BeautifulSoup(text, 'html.parser')
        
        bookpage = soup.find("section", class_='searchresultnofield resultno')
        if bookpage!=None:
            print("Can't Searched")
            with open('./cantsearch.csv', 'a+', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Can't Searched:", user_input])
        else:
            print('Searched')

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

            authors = re.search(authors_regex, Data)
            if authors != None:
                authors = re.search(authors_regex, Data).group(1)

            publisher = re.search(publisher_regex, Data)
            if publisher != None:
                publisher = re.search(publisher_regex, Data).group(1)

            publishedDate = re.search(publishedDate_regex, Data)
            if publishedDate != None:
                publishedDate = re.search(publishedDate_regex, Data).group(1)

            # print("\nTitle:", title)
            # print("\nSummary:")
            # print("Image:", image)
            # print(f"Price: {price} 元")
            # print("Author(s):",authors)
            # print("PublishedDate:", publishedDate)
            # print("Publisher:", publisher)
            # print("\n***")

            with open('./output.csv', 'a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([title, '[img]'+image+'[/img]', price, authors,
                                publishedDate, publisher, user_input])
