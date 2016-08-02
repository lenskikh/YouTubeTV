from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import sys, os
import pause

links = []
counter = 0

#Path to firefox profile. For using installed addons (like adblock)
fp = webdriver.FirefoxProfile("/Users/Mik/Documents/fx_profile")
driver = webdriver.Firefox(firefox_profile=fp)

#COLLECT VIDEOS
link_file = os.path.dirname(sys.argv[0]) + '/links.txt' #working correctly with pyinstaller
for line in open(link_file, "rb"):
    driver.get(line.rstrip())
    pause.seconds(1)

    #get links of videos
    select = driver.find_elements_by_xpath('//a[@class="yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2"]')
    #duration of videos
    select2 = driver.find_elements_by_xpath('//span[@class="video-time"]')
    select3 = iter(select2)
    
    for i in select:
        line = i.get_attribute('href')#get link video
        line2 = select3.next().get_attribute('innerText')#get duration video
        links.insert(counter,line+' '+line2)#Info about duration add to link in list
        counter += 2
    counter = 0

#watching videos
link_file = os.path.dirname(sys.argv[0]) + '/watched.txt'
for link in links:
    link_and_duration = link.split(' ')
    #check watched videos and ignore it
    if any(link_and_duration[0] in s for s in open(link_file, "r")):
        print "watched"
    else:
        driver.get(link_and_duration[0])
        duration = link_and_duration[1].split(":")
        wr = open(link_file,"a")
        wr.write(link+"\n")#write link to watched file
        wr.close()

        #sleep while user is watching
        pause.minutes(int(duration[0]))
        pause.seconds(int(duration[1]))

driver.quit()
