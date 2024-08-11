from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.binary_location = '/opt/chrome-linux64/chrome'



service = Service('/usr/local/bin/chromedriver')








def get_average_value():
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
    driver.quit()
    return average_value

# This function can be called to get the average value when needed
