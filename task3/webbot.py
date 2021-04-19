from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Initiate the browser
browser  = webdriver.Chrome(ChromeDriverManager().install())

# Open the Website
browser.get('https://addressify.com.au/')
# grab serachbar and enter martin place
addr = "19 martin pl, sydney"
browser.find_element_by_name('address').send_keys(addr)

suggestions = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.ID, 'ui-id-1')))
for item in suggestions:
    print(item.text)
