import requests
from bs4 import BeautifulSoup

def parse_mod_data(url):
    """Парсит данные мода с сайта sims-market.ru"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлечение данных по новым селекторам
        title_element = soup.select_one('.mod__name')
        if not title_element:
            raise ValueError("Заголовок мода не найден")
        title = title_element.text.strip()

        image_element = soup.select_one('.mod__img img')
        if not image_element or not image_element.get('src'):
            raise ValueError("Изображение мода не найдено")
        image_url = image_element['src']
        if image_url.startswith('/'):
            image_url = 'https://sims-market.ru' + image_url  # Сделать абсолютным

        date_element = soup.select_one('.mod__date')
        if not date_element:
            raise ValueError("Дата публикации не найдена")
        date = date_element.text.strip()

        downloads_element = soup.select_one('.mod__downloads')
        if not downloads_element:
            raise ValueError("Количество загрузок не найдено")
        downloads = downloads_element.text.strip()

        # Извлечение ссылки для скачивания ZIP
        download_link_element = soup.select_one('#mod_download_link')
        if not download_link_element or not download_link_element.get('href'):
            raise ValueError("Ссылка для скачивания не найдена")
        download_link = download_link_element['href']
        if download_link.startswith('/'):
            download_link = 'https://sims-market.ru' + download_link  # Сделать абсолютным

        return {
            'title': title,
            'image_url': image_url,
            'link': url,
            'date': date,
            'downloads': downloads,
            'download_link': download_link  # Добавляем ссылку для скачивания
        }
    except Exception as e:
        raise ValueError(f"Ошибка парсинга: {str(e)}")