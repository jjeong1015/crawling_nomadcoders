from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?term=" # 검색어가 없는 기본 url
  response = get(f"{base_url}{keyword}") # f를 넣어야 문자열 안에 변수 삽입 가능, 2개의 url을 모두 합치면 하나의 전체 url 생성
  if response.status_code != 200: # 상태 코드가 200이 아닌 경우 에러 출력
    print("Can't request website")
  else:
    results = [] # 비어있는 list
    soup = BeautifulSoup(response.text, "html.parser") # response.text -> 방금 얻은 웹사이트의 코드를 주고 beautifulsoup에게 던짐
    jobs = soup.find_all('section', class_= "jobs") # class가 job인 section들 찾기
    # list의 각 항목에 대한 코드를 실행하고 싶을 때 ex) ul 안에 있는 li
    for job_section in jobs: # job section 내부 검색
      # print(job_section.find_all('li')) # 모든 li 찾기
      # job의 모든 post 찾기
      job_posts = job_section.find_all('li') # job post -> list의 li
      job_posts.pop(-1) # pop은 list에서 한 항목 제거 ex) -1 : 마지막 항목 제거, -2 : 마지막에서 두 번째, 0부터 시작할 수 있음
      for post in job_posts: # list 안의 코드를 실행하고자 할 때 여기에서는 job_posts가 li
        # href, company, job title, position full-time or part-time, region
        anchors = post.find_all('a')
        anchor = anchors[1] # 2번째 anchor(url 호출 시 원하는 위치로 화면 이동하는 기능) 필요
        link = anchor['href'] # link를 엑셀 파일에 저장
        company, kind, region = anchor.find_all('span', class_="company") # find_all() list 가져옴
        title = anchor.find('span', class_='title') # find() 결과 가져옴
        job_data = {
          'link' : f"https://weworkremotely.com{link}", # 다시 검색해서 링크 받기 -> ★ 사용자들이 엑셀에서 클릭할 링크
          'company' : company.string, # .string을 사용하면 태그 안에 있는 텍스트를 줌 ex) <span class="title"> title here </span> -> beautifulsoup가 title here만 남겨줌
          'location' : region.string,
          'position' : title.string
        }
        results.append(job_data) # job을 추출할 때마다 그것들을 비어있는 list(11줄) 안에 넣음
    return results