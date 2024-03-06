from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
edge_service = Service(edge_driver_path)
edge_options = Options()

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
edge_options.add_argument(f'user_agent={user_agent}')
edge_options.add_argument('--disable-infobars')
edge_options.add_argument('--disable-logging')
edge_options.add_argument('--disable-extensions')

driver = webdriver.Edge(service=edge_service, options=edge_options)
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 20)

url = "https://offshoreleaks.icij.org/search?q=china&c=&j=&d="
driver.get(url)

# probar donde está el boton
# checkbox = wait.until(EC.presence_of_element_located((By.ID, "accept")))
# checkbox.click()

# submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-block btn-lg"]')))
# submit_button.click()
# time.sleep(3)


# loadMoreButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/search?c=&cat=Entity&d=&from=100&j=&q=china"]')))
# loadMoreButton.click()

try:
    checkbox = wait.until(EC.presence_of_element_located((By.ID, "accept")))
    checkbox.click()

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-block btn-lg"]')))
    submit_button.click()

    wait.until(EC.invisibility_of_element_located((By.ID, "__BVID__68")))
except NoSuchElementException:
    pass

res = []
while True:
    try:
        loadMoreButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-dark font-weight-bold"]')))
        ActionChains(driver).move_to_element(loadMoreButton).perform()
        loadMoreButton.click()
        #time.sleep(5)
    except (NoSuchElementException, TimeoutException):
        print("No more pages found")
        break
    try:
        table = driver.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')  # obtener todas las filas de la tabla

        headers_row = rows[0].find_elements(By.TAG_NAME, 'th')
        tableheaders = [th.text for th in headers_row]

        tabledata = [[td.text for td in row.find_elements(By.TAG_NAME, 'td')] for row in rows[1:]]  # obtener todos los datos de cada fila
        res.extend([dict(zip(tableheaders, t)) for t in tabledata])
    except StaleElementReferenceException:
        pass

with open('table.json', 'w') as f:
    json.dump(res, f)

driver.quit()
