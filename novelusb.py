import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def extract_article_content(url):
    # Configure Selenium to use a web driver
    driver = webdriver.Chrome()  # You will need to download the appropriate driver for your browser (e.g., Chrome driver)

    # Initialize an empty string to store the extracted content
    extracted_content = ""

    while True:
        # Load the webpage using Selenium
        driver = webdriver.Chrome()
        driver.get(url)

        # Extract the HTML content
        html_content = driver.page_source

        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the div with id=chr-content
        content_div = soup.find('div', {'id': 'chr-content'})

        if content_div:
            # Extract chapter title
            title_element = soup.select_one('div.row > div.col-xs-12 > h2 > a.chr-title > span.chr-text')
            if title_element:
                chapter_title = title_element.get_text()
                extracted_content += "\n" + chapter_title + "\n"

            # Extract chapter content from <p> tags in the div with id=chr-content
            paragraphs = content_div.find_all('p')
            for paragraph in paragraphs:
                paragraph_text = paragraph.get_text(separator='\n')
                extracted_content += paragraph_text + "\n"

            # Find the next chapter link
            next_chap_link = soup.find('a', {'id': 'next_chap'})
            if next_chap_link and 'href' in next_chap_link.attrs:
                # Update the URL to the next chapter link
                url = next_chap_link['href']
                driver.quit()
            else:
                driver.quit()
                break
            
            # Append the extracted content to the output file
            with open('/home/eusebioleite/novels/novel.txt', 'a') as f:
                f.write(extracted_content + "\n")

            # Reset the extracted_content
            extracted_content = ""

            # Wait for a short interval before processing the next page
            time.sleep(6)

        else:
            print("No article found on the webpage.")
            driver.quit()
            break

# Provide the URL of the first webpage you want to extract the article from
first_url = "https://novelusb.com/novel-book/shadow-slave-novel/chapter-831-master-naeve"

# Call the function to extract the article content
extract_article_content(first_url)
