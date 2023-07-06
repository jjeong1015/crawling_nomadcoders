from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from extractors.wwr import extract_wwr_jobs

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)

def get_page_count(keyword):
  base_url = "https://kr.indeed.com/jobs"
  browser.get(f"{base_url}?q={keyword}")

  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find("nav", attrs={"aria-label": "pagination"})
  pages = pagination.find_all("div", recursive=False)
  count = (len(pages)) # 페이지의 갯수
  if count == 0:
    return 1
  else:
    return count - 1

#print(get_page_count("python"))


def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  results = []
  for page in range(pages): # 10개의 숫자 배열을 원할 경우 숫자 10 입력
    base_url = "https://kr.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}&start={page*10}"
    #print("Requesting", final_url)
    browser.get(final_url)
    print(final_url)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_list = soup.find("ul", class_ = "jobsearch-ResultsList")
    jobs = job_list.find_all('li', recursive = False)
    for job in jobs:
      zone = job.find("div", class_ = "mosaic-zone")
    if zone == None:
      anchor = job.select_one("h2 a")
      title = anchor['aria-label']
      link = anchor['href']
      company = job.find("span", class_ = "companyName")
      location = job.find("div", class_ = "companyLocation")
    
      job_data = {
      'link' : f"http://kr.indeed.com{link}",
      'company' : company.string,
      'location' : location.string,
      'position' : title
      }
      results.append(job_data)
  return results

jobs = extract_indeed_jobs("python")
print(jobs)