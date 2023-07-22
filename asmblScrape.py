import pandas as pd
import numpy as py
import requests
from bs4 import BeautifulSoup

#
# GETTING ALL IMAGE URLS FOR A LISTING
#

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

def getImageURLS(inputURL, pageNum):
    r = requests.get(inputURL, headers=headers)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')

    product_list = soup.find_all('div', class_='s-item__image')

    products_site = []

    for item in product_list:
        for link in item.find_all('a', href=True):
            products_site.append(link['href'])
    products_site = list(dict.fromkeys(products_site))
    products_site = list(filter(None, products_site))
    products_site = [x for x in products_site if x.startswith('https://www.ebay.com/itm/')]
    # print("Number of results on page "+ pageNum + ": " + str(len(products_site)))

    res = []
    for link in products_site:
        r = requests.get(link, headers=headers)
        print(r)
        soup = BeautifulSoup(r.content, 'html.parser')
        Title = soup.select_one('h1', class_='x-item-title__mainTitle').get_text(strip=True)
        imageTags = soup.find_all("div", {"class": "ux-image-filmstrip-carousel"})
        if not imageTags:
            continue
        imageTags=imageTags[0]
        soup = BeautifulSoup(str(imageTags), 'html.parser')
        images = soup.find_all("img")
        imageURLS = []
        for image in images:
            temp = image["src"].replace('s-l64.jpg', 's-l1000.jpg')
            imageURLS.append(temp)
        res = res + imageURLS
    print("Number of results on page "+ pageNum + ": " + str(len(products_site)))
    print("Number of images on page "+ pageNum + ": " + str(len(res)))
    return res

searchTerm = input("Type in a search term ")
pages = int(input("# of pages of results to scrape "))
urlSkeleton = {
    "1" : ("&_sacat=0&_dmd=1&_fcid=1"),
    "2+" : ("&_sacat=0&_dmd=1&_pgn=","&_fcid=1")
}

res = []
url = "https://www.ebay.com/sch/i.html?_nkw="+searchTerm

for i in range(1,pages+1):
    if i == 1:
        res = res + getImageURLS(url+urlSkeleton["1"][0], "1")
    else:
        temp = url+urlSkeleton['2+'][0]+str(i)+urlSkeleton['2+'][1]
        res = res + getImageURLS(temp, str(i))

# count = 0
# for temp in res:
#     for key in temp:
#         count+=len(temp[key])
print(res)
print("Total number of images: "+str(len(res)))


for index in range(len(res)):
    img_data = requests.get(res[index]).content
    file_path = '/Users/alexyu/ASMBL_scrape/nvidia+geforce+rtx+3060+ti+founders+edition/nvidia+geforce+rtx+3060+ti+founders+edition-'+str(index)+'.jpg'
    with open(file_path, 'wb') as handler:
        handler.write(img_data)