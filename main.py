from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import csv
import pandas as pd

driver_path = "C:\Developer\chromedriver.exe"

ai_link = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=2&fos=3&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&q=artificial%20intelligence&limit=10&offset=&display=list'
robotics_link = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=2&fos=3&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&q=robotics&limit=10&offset=&display=list'
automation_link = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=2&fos=3&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&q=automation&limit=10&offset=&display=list'
mechatronics_link = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=2&fos=3&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&q=mechatronics&limit=10&offset=&display=list'
data_science_link = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=2&fos=3&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=11&subjects%5B%5D=15&q=data%20science&limit=10&offset=&display=list&lvlEn%5B%5D='

type_of_courses = [data_science_link, ai_link, robotics_link, automation_link, mechatronics_link]
deadline, tuition_fees, semester_contribution, submit_to, university_link = None, None, None, None, None


def create_excel_file():
    heading = ['Course', 'University', 'City', 'Deadline', 'Tuition fees', 'Semester Contribution', 'Submit Application to', 'Link']
    with open('universities_info.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(heading)


def check_if_already_present(details):
    file = pd.read_csv('universities_info.csv', encoding='unicode_escape')
    course = file['Course'].tolist()
    university = file['University'].tolist()
    if details[0] in course and details[1] in university:
        return True
    else:
        return False


def collection_of_courses(passed_info):
    with open('universities_info.csv', 'a', newline='', encoding="utf-8") as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerows(passed_info)


def collect_info():
    global deadline, tuition_fees, semester_contribution, submit_to, university_link
    stored_info = []
    courses = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.c-ad-carousel__visual > div.o-mixed > div > a.list-inline-item'))
    )
    time.sleep(5)
    for selected in courses:
        selected.click()
        dynamic_content = driver.page_source
        soup = BeautifulSoup(dynamic_content, 'html.parser')
        title = soup.find('span', class_='d-sm-block').text
        city = soup.find('span', class_='c-detail-header__info').text.strip().split('•')[1].strip()
        tex = soup.find('h3', class_='c-detail-header__subtitle')
        university = tex.span.previous_sibling.strip()

        info_table1 = soup.select_one(selector='div#overview > div > dl.c-description-list')
        for info in info_table1:
            if info.get_text(strip=True) == 'Application deadline':
                deadline = info.find_next('dd').get_text()
            if info.get_text(strip=True) == 'Tuition fees per semester in EUR':
                tuition_fees = info.find_next('dd').get_text().strip()

        info_table2 = soup.select_one(selector='div#costs > div > dl.c-description-list')
        for info in info_table2:
            if info.get_text(strip=True) == 'Semester contribution':
                semester_contribution = info.find_next('dd').get_text()

        info_table3 = soup.select_one(selector='div#registration > div > dl.c-description-list')
        for info in info_table3:
            if info.get_text(strip=True) == 'Submit application to':
                submit_to = info.find_next('dd').get_text()
                if info.find_next('dd').a:
                    university_link = info.find_next('dd').find('a')['href']
                else:
                    university_link = 'No link found'
        details = [title, university, city, deadline, tuition_fees, semester_contribution, submit_to, university_link]
        # Checking if university already added in the file or not and if added it is not appended in the main list
        if check_if_already_present(details):
            pass
        else:
            stored_info.append(details)
        time.sleep(5)
        driver.back()

    # Add to file
    collection_of_courses(stored_info)


def find_course(link):
    more_page = True
    driver.get(link)
    # This mechanism click the next button so that next page renders until end of pages has been reached
    while more_page:
        time.sleep(3)
        # Find details about course on the current page
        collect_info()
        time.sleep(2)
        try:
            next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-result-pagination-next')))
            next_page.click()
        except ElementClickInterceptedException and TimeoutException:
            more_page = False


def find_ai_course():
    driver.get('https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=&fos=&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&q=&limit=10&offset=&display=list')
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'qa-cookie-consent-accept-all')))
    element.click()
    for course in type_of_courses:
        find_course(course)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    create_excel_file()
    find_ai_course()
    driver.quit()

