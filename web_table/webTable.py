from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.common.by import By
import csv
from web_table import func_opration

driver = webdriver.Chrome()
driver.get("http://www.wsj.com/mdc/public/page/2_3024-NYSE.html")

WebDriverWait(driver,10).until(
    EC.visibility_of_element_located((By.TAG_NAME,"table"))
)

tables = driver.find_elements_by_tag_name("table")
print("table list lenght :"+ str(len(tables)))
i = 0
if len(tables)>0:
    print("exploring tables...")
    # table explore logic
    for table in tables:
        # print("table selected...")
        rows = table.find_elements_by_tag_name("tr")
        for row in rows:
            ths = row.find_elements_by_tag_name("th")
            if len(ths)>0:
                list = []
                for th in ths:
                    list.append(th.text)
                func_opration.table_data(list)
            # print("checking...")
            tds = row.find_elements_by_tag_name("td")
            list = []
            for td in tds:
                list.append(td.text)
            func_opration.table_data(list)
        # print("storing row...")
        func_opration.table_data("\n")
        i += 1
        print(str(i))
        func_opration.progress(i, len(tables), "storing table in progress")


else:
    print("no table found...\n exiting.")