from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)


def get_page_count(keyword): # 첫 페이지로 이동해 뒤에 몇 페이지가 있는지 확인하는 함수
    base_url = "https://kr.indeed.com/jobs"
    browser.get(f"{base_url}?q={keyword}")  #{}로 변수 받으려면 f 필요

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    pages = pagination.find_all("div", recursive=False)
    count = (len(pages))  # 페이지의 갯수
    if count == 0: # 페이지가 없는 경우 1페이지가 끝
        return 1
    else:
        return count - 1


#print(get_page_count("python"))


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):  # 찾은 페이지 수만큼 코드들을 실행시키기 위해 range 사용 ex) 1개의 페이지만 찾았을 경우 range(1) -> 코드는 한 번만 실행
        base_url = "https://kr.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}" # ex) 첫 번째 페이지에는 start = 0, 두 번째 페이지에는 start = 10
        #print("Requesting", final_url)
        browser.get(final_url)
        print(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")

                job_data = {
                    'link': f"http://kr.indeed.com{link}",
                    'company': company.string.replace(",", " "), # ex) 위치가 Google, 서울일 경우 ,(콤마)를 csv가 제대로 인식하지 못해.replace()로 , 대신 띄어쓰기
                    'location': location.string.replace(",", " "),
                    'position': title.replace(",", " ")
                }
                results.append(job_data)

    return results
