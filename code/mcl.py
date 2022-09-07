import csv
import time
from bs4 import BeautifulSoup as bs
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

chromedriver_autoinstaller.install() 

class mcl():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('lang=ko_KR')
        options.add_argument("window-size=960x540")
        options.add_argument('--mute-audio')
        options.add_argument("disable-gpu") 
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('incognito')

        prefs = {
            'profile.default_content_setting_values': {
                'cookies': 2,
                'images': 2,
                'plugins': 2,
                'popups': 2,
                'geolocation': 2,
                'notifications': 2,
                'auto_select_certificate': 2,
                'mouselock': 2,
                'mixed_script': 2,
                'media_stream': 2,
                'media_stream_mic': 2,
                'media_stream_camera': 2,
                'protocol_handlers': 2,
                'ppapi_broker': 2,
                'automatic_downloads': 2,
                'midi_sysex': 2,
                'push_messaging': 2,
                'ssl_cert_decisions': 2,
                'metro_switch_to_desktop': 2,
                'protected_media_identifier': 2,
                'app_banner': 2,
                'site_engagement': 2,
                'durable_storage': 2
            }
        }
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)
    
    def scrap(self, link, cliptime):
        origin = []
        try:
            self.driver.get(link)
            time.sleep(5)

            origin_xpath = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[3]/div/div/div/a')
            origin_href = origin_xpath.get_attribute('href').split('?')
            temp = origin_href[1].split('&')[-1]
            datetime_format = "t=%Hh%Mm%Ss"
            datetime_result = datetime.strptime(temp, datetime_format)
            origin_time = datetime_result.strftime("%H:%M:%S") + '~' + (datetime_result + timedelta(seconds=cliptime)).strftime("%H:%M:%S")
        
            origin_broad = origin_href[0]
            origin_link = origin_href[0] + '?' + origin_href[1].split('&')[-1]
        
            origin.append(origin_time)
            origin.append(origin_broad)
            origin.append(origin_link)
        except Exception as error:
            print(error)
            origin.append("~")
            origin.append("err")
            origin.append("err")
        return origin

    def makecliplist(self):
        page = open('./IO/target.html','rt', encoding='utf-8').read()
        soup = bs(page, 'html.parser')
        clips = soup.select("div.ScTextWrapper-sc-14f6evl-1.fejGga")
        clipdetails = soup.select("div.ScTransformWrapper-sc-uo2e2v-1.ghrhyx > a > div")
        cliplist = []
        count = 0
        for clip, clipdetail in zip(clips, clipdetails):
            # informations
            temp = []
            cliptime = 0
            count += 1
            title = clip.select_one("div:nth-child(1) > div > a > h3")["title"]
            temp_selected = clip.select_one("div:nth-child(1) > div > a")["href"]
            link = 'https://clips.twitch.tv/' + temp_selected.split('/')[3].split('?')[0]
            maker = clip.select_one("div:nth-child(2) > p:nth-child(2) > a")["href"]
            
            # details
            temp_selected = clipdetail.select("div.ScPositionCorner-sc-1iiybo2-1.eHqCXd > div")
            view = str(temp_selected).split('>')[1].split('회 시청<')[0]
            temp_selected = clipdetail.select("div.ScPositionCorner-sc-1iiybo2-1.gtpTmt > div")
            ct = str(temp_selected).split('>')[1].split('<')[0]
            if ct == '1:00':
                cliptime = 60
            else:
                cliptime = int(ct.split(':')[1])

            origin = self.scrap(link, cliptime)
            temp.append(count)
            temp.append(title)
            temp.append(link)
            temp.append(origin[0])
            temp.append(origin[1])
            temp.append(origin[2])
            temp.append(maker)
            temp.append(view)
            cliplist.append(temp)
            print(str(count))

        with open('./IO/result/cliplist.csv', 'w', encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['#','title','link', 'time', 'number', 'origin', 'maker', 'view'])
            writer.writerows(cliplist)

if __name__ == '__main__':
    mcl().makecliplist()
        