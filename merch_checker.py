#selenium for frontend web scraping
#pickle for file storage
#plyer for notification
from selenium import webdriver
import pickle
from plyer import notification

#U#RL of estore you want to keep track of
url = 'https://annapurnainteractive.com/store'

#Use a webdriver to load up a window of store
wd = webdriver.Chrome(executable_path='chromedriver.exe')
wd.get(url)

#THIS SECTION NEEDS TO BE CUSTOMIZED BY SITE
#we find and click the show more button
try:
    show_more = wd.find_element_by_css_selector('a.button:nth-child(1)')
    show_more.click()
#we expanded as much as possible
except:
    pass

#get list of products
merch_list = wd.find_element_by_css_selector('.store__list')

items = merch_list.find_elements_by_xpath("*")

#Formatting Item List
curr_item_list = [item.get_attribute('innerText') for item in items]
curr_item_list = [item[item.index('\n\n')+2:] for item in curr_item_list]

#Trying to load previous item list for comparison
#previous item list exists, load
try:
    with open("prev_item_list", "rb") as fp: 
        prev_item_list = pickle.load(fp)
#previous item list doesn't exist, use curr item list as prev item list until one can be written
except:
    prev_item_list = curr_item_list

#finding new items and discont items
new_items = list(set(curr_item_list) - set(prev_item_list))
discont_items = list(set(prev_item_list) - set(curr_item_list))

#write previous item list for future use
with open("prev_item_list", "wb") as fp:  
    pickle.dump(curr_item_list, fp)

#send notifications for new/discont items
if new_items:
    for item in new_items:
        notification.notify(title= 'NEW ANNAPURNA ITEM',
                        message= item,
                        app_icon = None,
                        toast=False)
if discont_items:
    for item in discont_items:
        notification.notify(title= 'DISCONTINUED ANNAPURNA ITEM',
                        message= item,
                        app_icon = None,
                        toast=False)

wd.quit()

