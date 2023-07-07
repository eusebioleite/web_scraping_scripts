import time
import requests
from bs4 import BeautifulSoup

def extract_article_content(url):
    extracted_content = ""

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            chapter_div = soup.find('div', {'id': 'chapter'})
            chapter_title = ""

            if chapter_div:
                title_element = chapter_div.select_one('span.chapter-text')
                if title_element:
                    chapter_title = title_element.get_text()
                    print(f"Running: {chapter_title}")
                    extracted_content += "\n" + chapter_title + "\n"

            content_div = soup.find('div', {'id': 'chapter-content'})
            if content_div:
                paragraphs = content_div.find_all('p')
                for paragraph in paragraphs:
                    paragraph_text = paragraph.get_text(separator='\n')
                    if paragraph_text != chapter_title:
                        extracted_content += paragraph_text + "\n"

            next_chap_link = soup.find('a', {'id': 'next_chap'})
            if next_chap_link and 'href' in next_chap_link.attrs:
                url = "https://novelfull.com" + next_chap_link['href']
            else:
                break

            with open('/home/eusebioleite/novels/novel.txt', 'a') as f:
                if extracted_content.strip():
                    f.write(extracted_content + "\n")

            extracted_content = ""
            time.sleep(2)

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            break

first_url = "https://novelfull.com/blood-warlock-succubus-partner-in-the-apocalypse/chapter-922-founder-leader-the-one-whodecides-the-fate-of-all.html"
extract_article_content(first_url)
