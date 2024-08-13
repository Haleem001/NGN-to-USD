from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Firefox
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
# from pyvirtualdisplay import Display

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-gpu')

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
from selenium.webdriver.firefox.service import Service as FirefoxService

# display = Display(visible=0, size=(1200, 800))
# display.start()



# chrome_options = Options()
# # chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--window-size=1200,800")
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-extensions")

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--headless")

service = Service('/usr/local/bin/geckodriver')
driver = webdriver.Firefox(service=service, options=firefox_options)







def get_average_value():

    
    driver.get('https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=NGN&paymentMethod=')
   

    try:
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-btn.css-7o12g0.ant-btn-primary.ant-btn-custom.ant-btn-custom-middle.ant-btn-custom-primary.bds-theme-component-light"))
        )
        confirm_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")

    values = []
    for i in range(1, 11):
       
        xpath = f"/html/body/div[8]/div[3]/div[1]/div[2]/div[2]/div/div/div/table/tbody[2]/tr[{i}]/td[2]/div/div/span"
        element = driver.find_element(By.XPATH, xpath)
        value = float(re.sub(r'[^\d.]', '', element.text))
        values.append(value)

    average_value = sum(values) / len(values)
    prnt = f"Average value: {average_value}"
    print(prnt)
    driver.quit()
    
    return average_value


