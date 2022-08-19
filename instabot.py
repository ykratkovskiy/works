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


browser = webdriver.Chrome('instagram\chromedriver.exe')


def instagram_login(username, password):
    
    try:
        browser.get('https://instagram.com')
        time.sleep(random.randrange(2,4))

        username_input = browser.find_element(By.NAME,'username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(random.randrange(1,4))

        password_input = browser.find_element(By.NAME,'password')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(1,4))

        password_input.send_keys(Keys.ENTER)
        time.sleep(random.randrange(1,4))
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
        time.sleep(random.randrange(5,9))

        posts_urls = []
        for i in range (1,3):
            browser.execute_script('window.scrollBy(0, 1300);')
            time.sleep(random.randrange(11,15))
            find_tags_a = browser.find_elements(By.TAG_NAME,'a')
            for item in find_tags_a:
                post_href = item.get_attribute('href')
                if '/p/' in post_href:
                    posts_urls.append(post_href)
                    
        posts_urls = set(posts_urls)
        posts_urls = list(posts_urls)
                  
        for item in posts_urls:
            count_of_post_urls+=1
        print (f'Hashtag "{hashtag}" collected {count_of_post_urls} items in current session')
         
        with open ('instagram\json_list_of_liked_hrefs(countryside)', 'r') as js:
            json_file = json.load(js)

        start_time = time.time()
        for url in (posts_urls[1:count_of_post_urls+1]):
            if url not in json_file:
                json_file.append(url)
                browser.get(url)
                time.sleep(random.randrange(3,7))
                
                find_other_tags_a = browser.find_elements(By.TAG_NAME,'a')
                unquoted_tag_set = {(unquote(item.get_attribute('href'))) for item in find_other_tags_a if '/explore/tags/' in (item.get_attribute('href'))}
                tags = {(re.findall(r'\w+', item)[-1]) for item in unquoted_tag_set}
                
                                
                if (tags.isdisjoint(badtags_set) == True):
                    like_button = browser.find_element(By.CSS_SELECTOR,'section:first-child span button').click()
                    counter_of_likes +=1
                    print (f'Clicked {counter_of_likes} posts from {count_of_post_urls} ({(round(counter_of_likes/count_of_post_urls*100,1))}%)')
                    time.sleep(random.randrange(180,192))
                else:
                    time.sleep(random.randrange(1,3))
                    counter_of_exclusion_tags +=1
                    print (f'{counter_of_exclusion_tags} tags passed')
                
            else:
                time.sleep(random.randrange(1,3))
                counter_of_repeates+=1
                print (f'Repeat! ({counter_of_repeates} for {hashtag})')

        
        with open ('instagram\json_list_of_liked_hrefs(countryside)', 'w') as lst:
            json.dump(json_file,lst)
        
        
        print (f'Hashtag "{hashtag}" has been clicked {counter_of_likes} times in {round((time.time()-start_time)/60)} min')
        print (f'were occured {counter_of_repeates} repeated posts of {hashtag}')
        print (f'{counter_of_exclusion_tags} posts excluded by hashtag(s)')
                            
    except Exception as ex:
        print (ex)
        browser.close()
        browser.quit()


def check_myfollowers():
    browser.get(f'https://www.instagram.com/{username}/followers')
    time.sleep(random.randrange(3,5))
    
    follower_ul = browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]')
    follower_urls = []
    followers_count = 0
    
    for i in range (0,13):
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',follower_ul)
        time.sleep(random.randrange(3,5))
        
        find_tag_a = follower_ul.find_elements(By.TAG_NAME,'a')
        for item in find_tag_a:
            follower_href = item.get_attribute('href')
            follower_urls.append(follower_href)
    
    follower_urls = set(follower_urls)
   
    for item in follower_urls:
        followers_count +=1
    print (f'У аккаунта "{username}" {followers_count} подписчиков')
       
 
    with open (f'instagram\json_list_of_followers({username})', 'r') as js_followers:
        json_follower = json.load(js_followers)
        json_follower = set(json_follower)
    
    difference = json_follower.difference(follower_urls)
    if len(difference)!=0:
        print (f'Из аккаунта "{username}" удалились(сменили id) следующие пользователи: {difference}')   
    
    follower_urls = list(follower_urls)
    with open (f'instagram\json_list_of_followers({username})', 'w') as lst:
        json.dump(follower_urls,lst)


def browser_close():
    return browser.close(),browser.quit()

def pause():
    return time.sleep(random.randint(6,12))

if __name__ == '__main__':
    instagram_login(username, password)
    pause()
    # check_myfollowers()
    
    hashtaglike('турпобеларуси')
   
        
    browser_close()
