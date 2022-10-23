from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import telepot
import os

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('start-maximized')

bot_token = os.environ.get('BOT_TOKEN')
chid = os.environ.get('CHANNEL_ID')
bot = telepot.Bot(bot_token)
link_blaze = '<a href="https://blaze.com/pt/games/crash">💻Blaze</a>'

def analise(lista):
    item_1 = float(lista[0])
    item_2 = float(lista[1])
    item_3 = float(lista[2])
    if (item_1 == 1) and (item_2 > 1):
        bot.sendMessage(chid, text=f'🚨Atenção🚨\n🎰Possível entrada...\n⏳Aguardar confirmação\n{link_blaze}', parse_mode='HTML', disable_web_page_preview=True)
    if (item_1 > 1) and (item_2 == 1):
        if item_3 != 1:
            bot.sendMessage(chid, f'😢 Entrada abortada')
    if (item_1 == 1) and (item_2 == 1):
        if item_3 == 1:
            pass
        else:
            bot.sendMessage(chid, f'☑️Entrada confirmada\n📈Entrar com auto retirada em 1.5x')

def resultado(lista):
    item_1 = float(lista[0])
    item_2 = float(lista[1])
    item_3 = float(lista[2])
    if lista[1:3] == ['1.00', '1.00']:
        if item_1 >= 1.5:
            bot.sendMessage(chid, f'🏆Win!!')
        else:
            bot.sendMessage(chid, f'❌Loss!!')

def rodarBot():
    page = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH') ,options=options)
    # page = webdriver.Chrome(service=Service(chromedriver_autoinstaller.install()) ,options=options)
    page.get('https://blaze.com/pt/games/crash')
    print('abrindo navegador')
    sleep(5)
    while True:
        for x in range(500):
            entries = page.find_element(By.XPATH, '//*[@id="crash-recent"]/div[2]/div[2]').get_attribute('textContent')
            results = entries.split('X')[:15]
            print(results)
            analise(results)
            resultado(results)
            results_b = results
            while (results_b[0] == results[0]) and (results_b[1] == results[1]):
                ppg = page.find_element(By.XPATH, '//*[@id="crash-recent"]/div[2]/div[2]').get_attribute('textContent')
                results_b = ppg.split('X')
        page.refresh()
        wait_selector = ''
        while wait_selector != '2x':
            wait_selector = page.find_element(By.XPATH, '//*[@id="crash-controller"]/div[1]/div[2]/div[1]/div[1]/button[2]').get_attribute('textContent')
            sleep(.5)
        sleep(.5)

rodarBot()