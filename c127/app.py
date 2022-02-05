
from attr import attrs
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import requests

url  = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver.exe")
#to start processing
browser.get(url)
#make the programme wait 
time.sleep(10)
newPlanetData=[]
planet_data=[]
headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity","detection_method"]
def getInfo():
    
    
    
    for i in range(0,1):
        while True:
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentPage = int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentPage<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            
            elif currentPage>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()

            else:
                break

        
        for ul_tag in soup.find_all("ul",attrs={"class" , "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index,li_tag in enumerate(li_tags):
                if index  == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])

                    except:
                        #double quotes means dont do anything
                        temp_list.append("")
                        # if it stops somewhere, write continue and continue to next block
                        continue

            hyper_link_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyper_link_li_tag.find_all("a",href=True)[0]["href"])

            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def fetchInfo(hyperLink):
    try:
        page = requests.get(hyperLink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class","fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:

                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class","value"})[0].contents[0])

                except:
                    temp_list.append("")
            newPlanetData.append(temp_list)
    
    except:
        time.sleep(10)
        fetchInfo(hyperLink)
getInfo()
for index,data in enumerate(planet_data):
    fetchInfo(data[5])

final = []
for index,data in enumerate(planet_data):
    newData = newPlanetData[index]
    newData = [i.replace("\n","")for i in newData]
    newData = newData[:7]
    final.append(data+newData)


with open("newplanetData.csv","w") as f:
    f1 = csv.writer(f)
    f1.writerow(headers)
    f1.writerows(planet_data)





 








