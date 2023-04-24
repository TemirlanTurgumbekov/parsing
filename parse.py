from bs4 import BeautifulSoup
import requests
import csv


count = 1
def get_html(url: str) -> str:
    '''Получает html разметку определенного сайта по url'''
    response = requests.get(url)
    return response.text

def get_soup(html: str) -> BeautifulSoup:
    '''Получает html разметку и структурирует ее в красивый bs'''
    soup = BeautifulSoup(html, "html.parser")
    return soup 

def get_last_page(soup: BeautifulSoup) -> int:
    '''Функция которая возвращает последную страницу на сайте'''
    pages = soup.find('ul', class_='pagination').find_all('a', class_='page-link')
    last_page = pages[-1].get('data-page')
    return int(last_page)       
    
def get_data(soup: BeautifulSoup) -> list:
    '''Функция получает нужные данные с сайта mashina.kg и возвращает в виде списка'''
    container = soup.find('div', class_='table-view-list')
    cars = container.find_all('div', class_='list-item')
    
    result = []
    for car in cars:
        name = car.find('h2', class_='name').text.strip()
        try:
            image = car.find('img', class_='lazy-image').get('data-src')
        except:
            image = 'No-image!'
        price_div = car.find('div', class_='block price')
        price = price_div.find('p').find('strong').text.strip()
        ls = ['year-miles', 'body-type', 'volume']
        desc = ' '.join(car.find('p', class_=x).text.strip() for x in ls)

        data = {
            'name': name,
            'desc': desc,
            'price': price,
            'image': image
        }
        
        result.append(data)
    return result

def prepare_csv() -> None:
    with open('cars.csv', 'w') as file:
        fieldnames = ['№', 'Name', 'Description', 'Price', 'Image Url']
        writer = csv.DictWriter(file, fieldnames)
        writer.writerow({
            '№': '№',
            'Name': 'Name',
            'Description': 'Description',
            'Price': 'Price',
            'Image Url': 'Image Url',      
        })

def write_to_csv(data: list) -> None:
    with open('cars.csv', 'a') as file:
        fieldnames = ['№', 'Name', 'Description', 'Price', 'Image Url']
        writer = csv.DictWriter(file, fieldnames)
        global count
        
        for car in data:
            writer.writerow({
            '№': count,
            'Name': car['name'],
            'Description': car['desc'],
            'Price': car['price'],
            'Image Url': car['image'],  
            })
            count +=1
        
def main():
    i = 1
    prepare_csv()
    while True:
        url = f'https://www.mashina.kg/search/all/?page={i}'

        html = get_html(url)
        soup = get_soup(html)
        last_page = get_last_page(soup)
        data = get_data(soup)
        write_to_csv(data)
        print(f'Спарсили {i}/{last_page} страницу')
        if i == 15:
            break
        i += 1
        
main()