from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv


def extract_numbers(string):
    # search for all numerical ranges (e.g., "1000 to 3000")
    ranges = re.findall(r'\d+\s*to\s*\d+', string)

    # get the minimum and maximum values from the string
    nums = []
    for r in ranges:
        start, end = map(int, r.split(" to "))
        nums.extend([start, end])
    nums.extend(list(map(int, re.findall(r'\d+', string))))
    if nums:
        return [min(nums), max(nums)]
    else:
        return []

def clea_csv(filename, copy):
    with open(filename, newline='\n') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='@')
        rows = []
        for row in csvreader:
            clean_row = []
            for item in row:
                clean_item = item.replace(",", "")
                clean_row.append(clean_item)
            rows.append(clean_row)
    with open(copy, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='@')
        for row in rows:
            csvwriter.writerow(row)

def read_file_size(filename):
    with open(filename, 'r') as file:
        text = file.read()
        size = text.split(',')
        return len(size)

def read_ID(filename, index):
    with open(filename, 'r') as file:
        text = file.read()
        first_word = text.split(',')[index]
        return first_word

def append_to_csv(filename, df):
    try:
        with open(filename, 'a') as f:
            df.to_csv(f, sep='@', encoding='utf-8', index=False, header=False)
        print(f"Data appended to {filename} successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

def append_to_file(item, filename):
    with open(filename, 'a') as f:
        if(item != "\n"):
            f.write(item + ',')
        else:
            f.write(item)

def callPage(url):
    response = requests.get(url)
    response = response.content
    """driver = webdriver.Chrome("chromedriver")
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    response = driver.page_source
    time.sleep(5)
    driver.quit()"""
    soup = bs(response, features="html.parser")
    return soup

def get_urls(soup: bs):
    lis = soup.find_all(class_= "a52608cc")
    hrefs = list()
    for row in list(lis):
        hrefs.append(row.a)
    Id = list()
    for row in hrefs:
        urls = row['href']
        match = re.search(r'ID(\d+)\.html', urls)
        print(match.group())
        append_to_file(match.group(), "id.txt")


def allUrls(url):
    urlreal = url
    i =1

    while i <=74 :
        if i != 1:
            delimiter = "?"
            page = url.split(delimiter)
            add = "?page=" + str(i)+"&"
            url = add.join(page)
        soup = callPage(url)
        print(url, "\n")
        try:
            get_urls(soup)
            append_to_file("\n", "id.txt")
        except Exception as e:
            print(f"Error: {e}")
        url = urlreal
        i +=1


def createCarUrl(ID):
    url = "https://www.olx.com.eg/en/ad/" + "-" + ID
    return url


def parsePhoneNumber(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    time.sleep(1)
    button = driver.find_element(By.CLASS_NAME, "_1b04dcc1")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)
    access = driver.find_elements(By.CLASS_NAME, "c6ce5164._31a14546._42207ab4")
    for j in access:
        if j.text == "Continue with Email":
            access = j
            break
    driver.execute_script("arguments[0].click();", access)
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys("ahmedmoamen246@gmail.com")
    next = driver.find_elements(By.CLASS_NAME, "_5fd7b300.f3d05709")
    for j in next:
        if j.text == "Next":
            driver.execute_script("arguments[0].click();", j)
    time.sleep(3)
    driver.find_element(By.ID, "password").send_keys("Am123456")
    time.sleep(2)
    login = driver.find_elements(By.CLASS_NAME, "_5fd7b300.f3d05709")
    for j in login:
        if j.text == "Log in":
            driver.execute_script("arguments[0].click();", j)
    time.sleep(3)
    show = driver.find_element(By.CLASS_NAME, "_09eb0c84._79855a31")
    driver.execute_script("arguments[0].click();", show)
    time.sleep(1)
    number = driver.find_element(By.CLASS_NAME, "_45d98091._2e82a662")
    phoneNumber = number.text
    driver.quit()
    return phoneNumber

def check(sDate):
    if "month" in sDate:
        splitted = sDate.split(" ")
        if splitted[0] == 1:
            return True
        else:
            return False
    elif "year" in sDate:
        return False
    return True

def getDate(soup: bs):
    date = soup.find(class_="_8918c0a8")
    return check(str(date.text))

def parseSeller(soup: bs):
    seller = soup.find(class_= "_1075545d _6caa7349 _42f36e3b d059c029")
    Name = seller.contents[0].text
    sellerDate = seller.contents[-1].text
    fullName = Name.split(" ")
    date_str = sellerDate.split()[-2:]
    date_str = " ".join(date_str)
    date = datetime.strptime(date_str, "%b %Y")
    dateJoined = date.date()
    return fullName, dateJoined

def parseCarDetails(soup: bs, carDict):
    location = soup.find(class_="_8918c0a8")
    location = location.text
    carDict['Location'].append(location)
    table = soup.find(class_="_241b3b1e")
    rows = table.contents
    keys = list()
    values = list()
    description = soup.find(class_="_0f86855a")
    if description:
        description = description.text
        description = re.sub(r'\n',". " ,str(description))
        description = re.sub(r',', " ", str(description))
        carDict['Description'].append(description)
    for row in rows:
        key = str(row.next_element.next_element.next_element)
        value = str(row.next_element.next_element.next_element.next_element.next_element)
        value = re.sub(r'"', "", str(value))
        value = re.sub(r',', "", str(value))
        if key == "Kilometers" or key == "Engine Capacity (CC)":
            value = extract_numbers(value)
            key1 = key + " Low"
            key2 = key + " High"
            keys.append(key1)
            keys.append(key2)
            if len(value) == 1:
                values.append(value[0])
                values.append(value[0])
            else:
                values.append(value[0])
                values.append(value[1])
        else:
            keys.append(key)
            values.append(value)
    for i in range(len(keys)):
        carDict[keys[i]].append(values[i])
    for key in carDict:
        if len(carDict[key]) < 1:
            carDict[key].append(None)

def carParseFeatures(soup: bs):
    table = soup.find(class_ = "_27f9c8ac")
    features = list()
    if table:
        for feat in table.contents:
            features.append(feat.text)
    return features


def parsePage(ID):
    url = createCarUrl(ID)
    ID = ID[2:11]
    soup = callPage(url)
    if getDate(soup):
        keys = ['ID', 'Brand', 'Model', 'Year', 'Phone Number' ,'Location', 'Ad Type', 'Fuel Type', 'Price', 'Price Type', 'Payment Options',
                'Kilometers Low', 'Kilometers High', 'Transmission Type', 'Condition', 'Body Type', 'Color', 'Engine Capacity (CC) Low', 'Engine Capacity (CC) High','Video',
                'Virtual Tour', 'Description']
        dictCarAdvert = {key: list() for key in keys}
        parseCarDetails(soup, dictCarAdvert)
        Full_name, dateJoined = parseSeller(soup)
        if dictCarAdvert['Condition'][0] != "New":
            phone = parsePhoneNumber(url)
            dictCarAdvert['Phone Number'] = phone
            dictCarAdvert['ID'] = ID
            del dictCarAdvert['Price Type']
            del dictCarAdvert['Condition']
            del dictCarAdvert['Video']
            del dictCarAdvert['Virtual Tour']
            del dictCarAdvert['Ad Type']
            df_ad = pd.DataFrame(dictCarAdvert)
            append_to_csv("car_ad.csv", df_ad)
            carDict = {k: v for i, (k, v) in enumerate(dictCarAdvert.items()) if 1 <= i <= 3}
            features = carParseFeatures(soup)
            carDict['Phone Number'] = phone
            df_car = pd.DataFrame(carDict)
            print(df_car)
            append_to_csv("car.csv", df_car)
            FeatureKey = ['AdId', 'Feature']
            featuresDict = {key: list() for key in FeatureKey}
            if len(features) > 0:
                i =0
                for feat in features:
                    featuresDict['AdId'].append(ID)
                    featuresDict['Feature'].append(feat)
                    i +=1
                df_features = pd.DataFrame(featuresDict)
                append_to_csv("features.csv", df_features)
            if len(Full_name) == 1:
                SellerDict = {'Phone Number': phone, 'first name': Full_name[0], 'last name': None, 'date joined': dateJoined}
            else:
                SellerDict = {'Phone Number': phone, 'first name': Full_name[0], 'last name': Full_name[1], 'date joined': dateJoined}
            df_seller = pd.DataFrame(SellerDict, index=[0])
            append_to_csv("seller.csv", df_seller)

def parseAllPages(indexs):
    error = list()
    for i in indexs:
        try:
            ID = read_ID("id.txt", i)
            print(i, "\n")
            parsePage(ID)
        except Exception as e:
            print(f"Error: {e}")
            error.append(i)
        time.sleep(1)
    if len(error) >= 2000:
        parseAllPages(error)


def createInsertStatement(filename, function,de):
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=de)
        # Open the output file for appending
        with open('output.sql', 'a', encoding="utf-8-sig") as outfile:
            # Loop through each row in the CSV file
            for row in reader:
                outfile.write("CALL "+ function + "('" + row[0] + "'")
                for col in row[1:]:
                    if col == "":
                        col = ",NULL"
                        outfile.write(col)
                    else:
                        col = re.sub("\'", "", col)
                        col = ",'"+col+"'"
                        outfile.write(col)
                outfile.write(");\n")

#allUrls("https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page=76&filter=new_used_eq_2%2Cyear_between_2000_to_2023")
size = read_file_size("id.txt")
print(size)
indexs = list(range(1187,size))
parseAllPages(indexs)





