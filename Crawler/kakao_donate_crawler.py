# -*- coding:utf-8 -*-
from bs4 import *
from selenium import webdriver
import xlsxwriter as xlsx

# 엑셀 파일 생성
wb=xlsx.Workbook("C:/Users/roytravel/Desktop/result.xlsx")
ws=wb.add_worksheet()

# 엑셀 셀 속성 설정
format0=wb.add_format({'border':2,'bold':True,'align':'center','fg_color':'white','font_color':'black'})
format1=wb.add_format({'border':1,'bold':True,'align':'center','fg_color':'white','font_color':'black'})

# 엑셀 셀 너비 설정
ws.set_column('A:A',10)
ws.set_column('B:B',100)
ws.set_column('C:C',10)

# (x+1,y+1)의 위치에 데이터 입력 및 셀 속성 설정
ws.write(0,0,u'번호',format0)
ws.write(0,1,u'제목',format0)
ws.write(0,2,u'금액',format0)

# 엑셀 행을 바꾸기 위한 변수 init 할당
global init
init = 1

def write(count):
    ws.write(init,0,count,format1)
    ws.write(init,1,name[count-1],format1)
    ws.write(init,2,don[count-1],format1)
    init +=1

# 기부 컨텐츠 제목 및 기부 금액을 담을 리스트 할당
name = list()
don = list()

# 기부 컨텐츠 제목 및 기부 금액 추출
def extract_title_and_money():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for title in soup.find('title'):
        name.append(title)
        print u"[+] 기부 완료 : {}".format(title)
    item = soup.find('dl', {'class': 'detail_fund fund_belong'})
    for person in item.find('dt', {'class': 'tit_fund'}):
        for total in item.find('dd', {'class': 'txt_fund'}):
            persons = int(person[person.find('(') + 1:person.find(')') - 1].replace(',',''))  # 응원기부 (xxx명)
            totals = int(total.replace(u'원', '').replace(',', ''))  # xx,xxx원
            don.append(totals/persons)
            print u"\t[-] 기부 금액은 {}원 입니다".format(totals/persons)

# 크롬 웹 드라이버를 이용한 다함께 카카오 페이지 오픈
driver = webdriver.Chrome('C:/Users/roytravel/Downloads/web/chromedriver')
driver.implicitly_wait(1)
driver.get("https://together.kakao.com/fundraisings/now")

# 다함께 카카오 로그인 기능
driver.find_element_by_xpath('//*[@id="dkHead"]/div[1]/div[2]/a[2]').click()
driver.find_element_by_xpath('//*[@id="loginEmail"]').send_keys('카카오 이메일을 입력하세요')
driver.find_element_by_xpath('//*[@id="loginPw"]').send_keys('카카오 이메일의 비밀번호를 입력하세요')
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/button').click()

# 한 번에 볼 수 있는 게시물이 20개 이므로, 전체 게시물 보기 클릭.
# for i in range(7):
#     driver.find_element_by_xpath('//*[@id="mArticle"]/div[3]/div[3]/button').click()

# 실제 기부 과정을 작동시키는 중심 코드
for j in range(1,141):
    try :
        driver.find_element_by_xpath('//*[@id="mArticle"]/div[3]/div[2]/ul/li['+str(j)+']/fundraising-card/a').click()
        driver.find_element_by_xpath('//*[@id="txtCmt"]').send_keys(u'응원할게요')
        driver.find_element_by_xpath('//*[@id="mArticle"]/comments/div/div[1]/div/div[2]/div/fieldset/button[2]').click()
        extract_title_and_money()

        write(j)
        driver.back()
        driver.find_element_by_xpath('//*[@id="toast-container"]/div[2]/div/div[2]/div').click()
        if j%20==0:
            driver.find_element_by_xpath('//*[@id="mArticle"]/div[3]/div[3]/button').click()
    except :
        pass
wb.close()

print "[+] 총 기부 횟수 = {}회".format(len(name))
print "[+] 총 기부 금액 = {}원".format(sum(don))
