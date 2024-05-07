from django.shortcuts import render,HttpResponse
import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin, unquote

def news(request):
    url = "https://economictimes.indiatimes.com/markets/stocks/news"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = soup.find('section', id='pageContent')
        return render(request,'debug/debug.html',{'page_content': page_content})
    else:
        return render(request, 'debug/debug.html', {'error': f"Error: {response.status_code}"})

def news_details(request):
    url = "https://economictimes.indiatimes.com/markets/stocks/news"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render(request, 'debug/news_details.html', {'error': f"Request Error: {e}"})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stories = soup.find_all('div', class_='eachStory')

        news_list = []

        for story in stories:
            img_url = story.find('img')['src']
            heading = story.find('h3').find('a').text
            article_url = story.find('h3').find('a')['href']
            timestamp = story.find('time', class_='date-format')['data-time']
            description = story.find('p').text

            # Create an absolute URL using urljoin
            absolute_url = urljoin(url, article_url)

            news_list.append({
                'img_url': img_url,
                'heading': heading,
                'article_url': absolute_url, 
                'timestamp': timestamp,
                'description': description,
            })

        return render(request, 'debug/news_details.html', {'news_list': news_list})
    else:
        return render(request, 'debug/news_details.html', {'error': f"Error: {response.status_code} - {response.reason}"})


def redirect_to_original(request, article_url):
    try:
        # Decode the URL
        decoded_url = unquote(article_url)
        
        response = requests.get(decoded_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Update class names, IDs, or tags based on the actual structure
        slide_head_sec = soup.find('div', class_='new-class-for-slideHeadSec')
        caption_description = soup.find('p', class_='new-class-for-caption-description')
        img_courtesy = soup.find('div', class_='new-class-for-imgCourtesy')
        share_bar = soup.find('div', class_='new-class-for-shareBar')
        clr = soup.find('div', class_='new-class-for-clr')
        
        # Check if the elements were found
        if slide_head_sec and caption_description and img_courtesy and share_bar and clr:
            # Convert the content to strings
            slide_head_sec_content = slide_head_sec.prettify()
            caption_description_content = caption_description.prettify()
            img_courtesy_content = img_courtesy.prettify()
            share_bar_content = share_bar.prettify()
            clr_content = clr.prettify()
        else:
            # Set messages indicating that the elements were not found
            slide_head_sec_content = "slideHeadSec not found."
            caption_description_content = "caption description not found."
            img_courtesy_content = "imgCourtesy not found."
            share_bar_content = "shareBar not found."
            clr_content = "clr not found."
        
    except requests.exceptions.RequestException as e:
        return render(request, 'debug/original_content.html', {'error': f"Request Error: {e}"})

    return render(
        request,
        'debug/original_content.html',
        {
            'slide_head_sec_content': slide_head_sec_content,
            'caption_description_content': caption_description_content,
            'img_courtesy_content': img_courtesy_content,
            'share_bar_content': share_bar_content,
            'clr_content': clr_content,
        }
    )

def news_a(request):
    url = "https://economictimes.indiatimes.com/markets/stocks/news"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        for li in soup.find_all('li'):
            title_element = li.find('a', class_='hl')
            img_element = li.find('img')
            if title_element and img_element:
                title = title_element.get('title')
                img_url = img_element.get('src')
                articles.append({'title': title, 'img_url': img_url})
        return render(request, 'debug/news_a.html', {'articles': articles})
    else:
        return render(request, 'debug/news_a.html', {'error_message': 'Failed to retrieve data'})



def news_b(request):
    url = "https://economictimes.indiatimes.com/markets/stocks/news"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render(request, 'debug/news_b.html', {'error': f"Request Error: {e}"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        most_searched_stocks = []
        most_searched_section = soup.find('section', class_='mostSearchedStocks')

        if most_searched_section:
            for row in most_searched_section.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) == 2:
                    # Check if the <a> element exists before accessing its text attribute
                    stock_name_anchor = columns[0].find('a')
                    stock_name = stock_name_anchor.text.strip() if stock_name_anchor else ""

                    stock_value = columns[1].text.strip()

                    # Check if the <span> element exists before accessing its text attribute
                    datetime_stock_span = row.find('span', class_='dateTimeStock')
                    datetime_stock = datetime_stock_span.text.strip() if datetime_stock_span else ""

                    # Check if the <span> element exists before accessing its text attribute
                    percentage_change_span = columns[1].find('span', class_='per')
                    percentage_change = percentage_change_span.text.strip() if percentage_change_span else ""

                    stock_data = {
                        'stock_name': stock_name,
                        'stock_value': stock_value,
                        'datetime_stock': datetime_stock,
                        'percentage_change': percentage_change,
                    }

                    most_searched_stocks.append(stock_data)

        return render(request, 'debug/news_b.html', {'most_searched_stocks': most_searched_stocks})
    else:
        return render(request, 'debug/news_b.html', {'error': f"Error: {response.status_code} - {response.reason}"})