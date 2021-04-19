from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# initiate the browser
browser  = webdriver.Chrome(ChromeDriverManager().install())

# open the Website
browser.get('https://addressify.com.au/')

# grab serachbar from the html element and enter martin place adress 
addr = "19 martin pl, sydney"
browser.find_element_by_name('address').send_keys(addr)

# grab the suggested autocomplete elements, but first we need to wait until they have loaded
# and then print them all out 
suggestions = WebDriverWait(browser, 3).until(EC.visibility_of_all_elements_located((By.ID, 'ui-id-1')))
for item in suggestions:
    print(item.text)
