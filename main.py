from extractors.indeed import extract_indeed_jobs # indeed에서 extractors 가져오기
from extractors.wwr import extract_wwr_jobs # www에서 extractors 가져오기

keyword = input("What do you want to search for? ") # 유저에게 검색하고 싶은 키워드 물어보기

indeed = extract_indeed_jobs(keyword) # 4줄에서 받은 유저의 keyword 입력 값과 함께 extract_indeed_jobs 호출
wwr = extract_wwr_jobs(keyword)

jobs = indeed + wwr # indeed와 wwr 서로 list return

file = open(f"{keyword}.csv", "w", encoding = "utf-8-sig") # 괄호 안에 열거나 만드려는 파일의 이름 적기, csv -> 파일 포맷, w -> 읽기 전용

file.write("Position, Company, Location, URL\n") # csv -> 쉼표로 구분된 값들, \n 필수

for job in jobs:
  file.write(f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n")

file.close()