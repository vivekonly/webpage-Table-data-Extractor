import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import MySQLdb
import sys


def batmat_data(list):
    print("storin batman data")
    with open("batmans.csv", "a") as bat:
        writer = csv.writer(bat, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(list)
        bat.close()

def table_data(list):
    print("storin table data")
    with open("table_data.csv", "a") as bat:
        writer = csv.writer(bat, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(list)
        bat.close()



def bowler_data(datas):
    print("storin batman data")
    with open("bowlers.csv", "a") as bat:
        writer = csv.writer(bat, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(datas)
        bat.close()


def get_links(driver):
    # print(driver.find_element_by_class_name("js-list"))
    result_buttons = driver.find_element_by_xpath('//*[@id="main-content"]/div/div/section')
    with open("page.html", "w") as fl:
        fl.write(str(result_buttons.get_attribute("innerHTML")))

    tab = result_buttons.find_elements_by_class_name("js-match")
    result_buttons = []
    for t in tab:
        link = t.find_element_by_tag_name("a").get_attribute("href")
        result_buttons.append(link)

    with open("links.txt", "w") as lnk:
        for lnl in result_buttons:
            lnk.write(lnl + "\n")


def get_data(link, driver):
    print(link)
    if bool(re.search("tab=scorecard", link)) == False:
        return 1
    print("link: " + link)
    driver.get(link)

    #   wait for connenct to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='scorecardContent']/div[1]/div[1]/div[2]/table"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='scorecardContent']/div[1]/div[1]/div[1]/div"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='scorecardContent']/div[1]/div[3]/div[1]/table"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/section[2]/header/h1/span"))
    )
    #     access team scorecard's
    team_card = driver.find_elements_by_class_name("teamScorecard")
    for team in team_card:
        print(team.find_element_by_class_name("teamHeader").text)
        team_name = team.find_element_by_class_name("teamHeader").text
        #         accesing batman detail
        match_date = team.find_element_by_xpath("/html/body/div[2]/div[1]/section[2]/header/h1/span").text
        batman = team.find_element_by_class_name("batsmen")
        batman_rows = batman.find_elements_by_tag_name("tr")
        for row in batman_rows:
            print("row :" + row.text)
            list = []
            list.append(team_name)
            list.append(match_date)
            ths = row.find_elements_by_tag_name("th")
            for th in ths:
                list.append(th.text)
            tds = row.find_elements_by_tag_name("td")
            for td in tds:
                if td.text == "":
                    continue
                print(" data: " + td.text)
                list.append(td.text)
            batmat_data(list)

        bowler = team.find_element_by_class_name("bowlers")
        bowler_row = bowler.find_elements_by_tag_name("tr")
        for row in bowler_row:
            list = []
            list.append(team_name)
            list.append(match_date)
            ths = row.find_elements_by_tag_name("th")
            for th in ths:
                list.append(th.text)
            tds = row.find_elements_by_tag_name("td")
            for td in tds:
                list.append(td.text)

            bowler_data(list)
    with open("done.txt", "a") as dn:
        dn.write(link)
    print("loop end ")


def get_db():
    db = MySQLdb.connect("localhost", "ipldata", "root", "")
    return db.cursor()


def check_db(year, name):
    print("checking data...")
    cursor = get_db()
    query = "SELECT * FROM ipldata WHERE date='" + year + "' AND name='" + name + "'"
    result = cursor.execute(query)
    if len(result) > 0:
        return 1
    else:
        return 0


def insert_data(path):
    print("inserting data...")
    #     read csv file and get it into list
    batsman = []
    bowlers = []
    with open("batmans.csv", "r") as f:
        for line in f:
            print(line)
            batsman.append(line)
        #     break list content
    for row in batsman:
        print("row data:" + row)
        data = csv.reader(row, delimiter=',')
        print(len(data))


# check availablitiy onto database

#     insert if not



def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
