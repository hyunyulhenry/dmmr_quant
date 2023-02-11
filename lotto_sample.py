from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import slack_sdk
from datetime import datetime
from tabulate import tabulate 
import re 

slack_token = 'YOUR TOKEN'
client = slack_sdk.WebClient(token = slack_token)

# 오늘 날짜 전송
dt = datetime.today().strftime('%Y-%m-%d')
client.chat_postMessage(channel = '#api_test',
                        text = f'''{dt} 로또 구매를 시작합니다.''')

url = 'https://www.dhlottery.co.kr/user.do?method=login&returnUrl='
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# 로그인
driver.find_element(By.XPATH, value = '//*[@id="userId"]').send_keys('YOUR ID')
driver.find_element(By.XPATH, value = '//*[@id="article"]/div[2]/div/form/div/div[1]/fieldset/div[1]/input[2]').send_keys('YOUR PASSWORD')
driver.find_element(By.XPATH, value = '//*[@id="article"]/div[2]/div/form/div/div[1]/fieldset/div[1]/a').click()

time.sleep(2)

# 당첨결과 전송
driver.get('https://www.dhlottery.co.kr/myPage.do?method=lottoBuyListView')
driver.find_element(By.XPATH, value = '//*[@id="frm"]/table/tbody/tr[3]/td/span[2]/a[2]').click() # 1주일
driver.find_element(By.XPATH, value = '//*[@id="submit_btn"]').click()

## iframe 내부로 접근
iframe = driver.find_element(By.CSS_SELECTOR, value = '#lottoBuyList')
driver.switch_to.frame(iframe)

tbl = driver.find_element(By.XPATH, value = '/html/body/table')
table_tr = tbl.find_elements(By.TAG_NAME, 'tr')

tbl_list = []
tbl_list.append([i.text for i in table_tr[0].find_elements(By.TAG_NAME, 'th')])
for a in range(1, len(table_tr)) :
    tbl_list.append([i.text for i in table_tr[a].find_elements(By.TAG_NAME, 'td')])

#tbl_select = []
#for j in range(0, 4):
 #   tbl_select.append(list(tbl_list[j][i] for i in [0, 4, 5 ,6]))

tbl_results = tabulate(tbl_list, tablefmt="grid")

channel_id = client.conversations_history(channel = 'CHANNEL HISTORY')
messages = channel_id.data['messages']
message_ts = messages[0]['ts']

client.chat_postMessage(channel = '#api_test',
                        text = tbl_results,
                        thread_ts = message_ts
                        )
driver.switch_to.default_content()

# 잔액 조회 
money = driver.find_element(By.XPATH, value = '/html/body/div[1]/header/div[2]/div[2]/form/div/ul[1]/li[2]/a[1]/strong').text
client.chat_postMessage(channel = '#api_test',                        
                        text = f'''현재 잔액은 {money} 입니다.''',
                        thread_ts = message_ts)


# 잔액이 만원 미만이면 5만원 충전하기
if int(''.join(re.findall('\d+', money))) <= 10000 :
    driver.find_element(By.XPATH, value = '/html/body/div[1]/header/div[2]/div[2]/form/div/ul[1]/li[2]/a[2]').click()
    driver.find_element(By.XPATH, value = '//*[@id="Amt"]/option[5]').click()
    driver.find_element(By.XPATH, value = '//*[@id="btn2"]/button').click()
    
    ## 계좌번호 복사하기
    account = driver.find_element(By.XPATH, value = '//*[@id="contents"]/table/tbody/tr[4]/td/span').text
    send = driver.find_element(By.XPATH, value = '//*[@id="contents"]/table/tbody/tr[2]/td').text    
    
    client.chat_postMessage(channel = '#api_test',
                            text = f'''{account} / {send} 입금하세요''',                            
                            thread_ts = message_ts)
    
time.sleep(2)

# 로또 구매
driver.get('https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40')

## iframe 내부로 접근
try:
    
    iframe = driver.find_element(By.CSS_SELECTOR, value = '#ifrm_tab')
    driver.switch_to.frame(iframe)
    
    driver.find_element(By.XPATH, value = '//*[@id="checkNumGroup"]/div[1]/label/span').click() # 자동선택 
    driver.find_element(By.XPATH, value = '//*[@id="amoundApply"]/option[5]').click() # 원하는 장수 구매
    driver.find_element(By.XPATH, value = '//*[@id="btnSelectNum"]').click() # 확인
    driver.find_element(By.XPATH, value = '//*[@id="btnBuy"]').click() # 구매하기
    driver.find_element(By.XPATH, value = '//*[@id="popupLayerConfirm"]/div/div[2]/input[1]').click() # 구매확인
    driver.find_element(By.XPATH, value = '//*[@id="closeLayer"]').click() # 최종확인
    
    text = '구매를 완료했습니다.' 
    
except:    
    
    text = '이번 주 구매한도를 모두 채웠습니다.'
    
client.chat_postMessage(channel = '#api_test',
                        text = text,
                        thread_ts = message_ts)

driver.quit()

# https://wikidocs.net/5857