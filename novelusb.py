import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def extract_article_content(url):
    extracted_content = ""

    while True:
        driver = webdriver.Chrome()
        driver.get(url)
        html_content = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html_content, 'html.parser')
        content_div = soup.find('div', {'id': 'chr-content'})

        if content_div:
            title_element = soup.select_one('div.row > div.col-xs-12 > h2 > a.chr-title > span.chr-text')
            if title_element:
                chapter_title = title_element.get_text()
                extracted_content += "\n" + chapter_title + "\n"
            paragraphs = content_div.find_all('p')
            for paragraph in paragraphs:
                paragraph_text = paragraph.get_text(separator='\n')
                extracted_content += paragraph_text + "\n"
            next_chap_link = soup.find('a', {'id': 'next_chap'})
            if next_chap_link and 'href' in next_chap_link.attrs:
                url = next_chap_link['href']
            else:
                break
            with open('/home/eusebioleite/novels/novel.txt', 'a') as f:
                f.write(extracted_content + "\n")
            extracted_content = ""
            time.sleep(30)
        else:
            print("No article found on the webpage.")
            break

first_url = "https://novelusb.com/novel-book/blood-warlock-succubus-partner-in-the-apocalypse-novel-novel/chapter-1015-fourth-order-rex"
extract_article_content(first_url)