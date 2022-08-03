from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from auth_data import username, password
import time
import random
import json
import re
from urllib.parse import unquote
from list_of_exclusion_tags import badtags_set
import time


def instagram_login(username, password):
    global browser
    browser = webdriver.Chrome('instagram\chromedriver.exe')
    try:
        browser.get('https://instagram.com')
        time.sleep(random.randrange(2,3))

        username_input = browser.find_element(By.NAME,'username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(random.randrange(1,2))

        password_input = browser.find_element(By.NAME,'password')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(1,2))

        password_input.send_keys(Keys.ENTER)
        time.sleep(random.randrange(4,6))
    except Exception as ex:
        print (ex)
        browser.close()
        browser.quit()


def hashtaglike(hashtag):
    try:
        counter_of_likes = 0
        counter_of_repeates = 0
        counter_of_exclusion_tags = 0
        count_of_post_urls = 0

        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}')
        time.sleep(random.randrange(7,10))

        for i in range (1,3):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randrange(27,37))
            find_tags_a = browser.find_elements(By.TAG_NAME,'a')
            posts_urls = {item.get_attribute('href') for item in find_tags_a if '/p/' in item.get_attribute('href')}
                             
        for item in posts_urls:
            count_of_post_urls+=1
        print (f'Hashtag "{hashtag}" collected {count_of_post_urls} items in current session')
         
        with open ('instagram\json_list_of_liked_hrefs(countryside)', 'r') as js:
            json_file = json.load(js)

        start_time = time.time()
        posts_urls = list(posts_urls)
        for url in (posts_urls[1:count_of_post_urls]):
            if url not in json_file:
                json_file.append(url)
                browser.get(url)
                time.sleep(random.randrange(5,9))
                
                
                find_other_tags_a = browser.find_elements(By.TAG_NAME,'a')
                unquoted_tag_set = {(unquote(item.get_attribute('href'))) for item in find_other_tags_a if '/explore/tags/' in (item.get_attribute('href'))}
                tags = {(re.findall(r'\w+', item)[-1]) for item in unquoted_tag_set}
                                
                
                if (tags.isdisjoint(badtags_set) == True):
                    like_button = browser.find_element(By.CSS_SELECTOR,'section:first-child span button').click()
                    counter_of_likes +=1
                    time.sleep(random.randrange(121,130))
                else:
                    time.sleep(random.randrange(1,3))
                    counter_of_exclusion_tags +=1
                
            else:
                time.sleep(random.randrange(1,3))
                counter_of_repeates+=1

        
        with open ('instagram\json_list_of_liked_hrefs(countryside)', 'w') as lst:
            json.dump(json_file,lst)
        
        
        print (f'Hashtag "{hashtag}" has been clicked {counter_of_likes} times in {round((time.time()-start_time)/60,1)} min')
        print (f'were occured {counter_of_repeates} repeated posts of {hashtag}')
        print (f'{counter_of_exclusion_tags} posts excluded by hashtag(s)')
                            
    except Exception as ex:
        print (ex)
        browser.close()
        browser.quit()

def browser_close():
    return browser.close(),browser.quit()

def pause():
    return time.sleep(random.randint(6,12))

if __name__ == '__main__':
    instagram_login(username, password)
    pause()
    hashtaglike('трамвай')
    pause()
    # hashtaglike('гродно2022')
    # pause()
    # hashtaglike('новогрудскийзамок')
    # pause()
    # hashtaglike('сула2022')
    # pause()
    browser_close()