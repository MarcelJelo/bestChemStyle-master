import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.common.exceptions import ElementClickInterceptedException

print('Hint: Program will open maximized. You can minimize the window after the browser has opened')
player_name = input('Enter a player name: ')
card_type = input('Enter the card-type: ')
chem_or_price = int(input('Do you want the best Chemistry Style (1) or the price (2) of a player? => '))

if chem_or_price <= 0 or chem_or_price > 2:
    print('Entered number not available')
    exit()
else:
    if chem_or_price == 1:
        pref_position = input('Enter the position you want: ').upper()

option = webdriver.ChromeOptions()

option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('--headless')
option.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(executable_path='chromedriver.exe',options=option)

driver.get('https://www.futbin.com/players')
time.sleep(1)

driver.save_screenshot('screenshot.png')
accept_btn = driver.find_elements_by_class_name('css-1litn2c')

s = len(accept_btn)

if(s > 0):
   accept_btn.click()

time.sleep(1)

search_bar = driver.find_element_by_id('players_search')
search_bar.send_keys(player_name + Keys.ENTER)
time.sleep(1)

rating_order = driver.find_element_by_xpath('//*[@id="repTb"]/thead/tr/th[2]/a')
rating_order.click()

driver.execute_script('window.scrollTo(0, 400)')

rows = driver.find_elements_by_xpath('//*[@id="repTb"]/tbody/tr')

row_amount = len(rows)

for i in range(1, row_amount + 1):
    current_row = driver.find_element_by_xpath('//*[@id="repTb"]/tbody/tr['+ str(i) +']/td[4]').text
    if current_row.lower() == card_type.lower():
        player_futbin = driver.find_element_by_xpath(
            '/html/body/div[8]/div[2]/div[5]/div[4]/table/tbody/tr[' + str(i) + ']/td[1]/div[2]/div[1]/a')
        break

test = 0

try:
    player_futbin.click()
except ElementClickInterceptedException:
    driver.execute_script('window.scrollTo(0, 1050)')
    test = 1

if test == 1:
    player_futbin.click()

if chem_or_price == 1:
    driver.execute_script('window.scrollTo(0, 600)')
    driver.find_element_by_xpath('//*[@id="its_traits"]/a').click()

    for index_position in range(1, 17):
        position = driver.find_element_by_xpath('//*[@id="rpp_field"]/div[' + str(index_position) + ']/div[1]').text
        if position == pref_position:
            break

    best_rating = 0
    best_chem_style = []

    for index_chemistry_style in range(2, 21):
        driver.find_element_by_xpath('/html/body/div[8]/div[15]/div/div/div[3]/div/div[3]/div['
                                     + str(index_chemistry_style) + ']/a').click()
        position = driver.find_element_by_xpath('//*[@id="rpp_field"]/div[' + str(index_position) + ']/div[2]').text
        if best_rating < int(position):
            best_rating = int(position)
            best_chem_style.clear()
            best_chem_style.append(driver.find_element_by_xpath(
                    '/html/body/div[8]/div[15]/div/div/div[3]/div/div[3]/div[' + str(index_chemistry_style) + ']/a')
                                       .text)
        else:
            if best_rating == int(position):
                best_chem_style.append(driver.find_element_by_xpath(
                    '/html/body/div[8]/div[15]/div/div/div[3]/div/div[3]/div[' + str(index_chemistry_style) + ']/a')
                                       .text)
        time.sleep(0.5)

    print('Best Chemistry style for ' + player_name + ' ' + card_type + ' card is/are: ' +
          str(best_chem_style).strip('[]') + ' with a rating of ' + str(best_rating))
else:
    if chem_or_price == 2:
        price_ps = driver.find_elements_by_xpath(
            '/html/body/div[8]/div[13]/div[2]/div[2]/div/div[2]/div[2]/div/div[12]/div[1]')
        s = len(price_ps)

        if (s > 0):
            price_ps = driver.find_element_by_xpath(
            '/html/body/div[8]/div[13]/div[2]/div[2]/div/div[2]/div[2]/div/div[12]/div[1]').text
            price_xbox = driver.find_element_by_xpath(
                '/html/body/div[8]/div[13]/div[2]/div[2]/div/div[2]/div[3]/div/div[12]/div[1]').text
            price_pc = driver.find_element_by_xpath(
                '/html/body/div[8]/div[13]/div[2]/div[2]/div/div[2]/div[4]/div/div[12]/div[1]').text
        else:
            price_ps = driver.find_element_by_xpath('//*[@id="ps-lowest-1"]').text
            price_xbox = driver.find_element_by_xpath('//*[@id="xbox-lowest-1"]').text
            price_pc = driver.find_element_by_xpath('//*[@id="pc-lowest-1"]').text

        print('The price of ' + card_type + ' ' + player_name + ' is:\n' + price_ps +
              ' coins (PS)\n' + price_xbox + ' coins (XBox)\n' + price_pc + ' coins (PC)')

driver.close()
