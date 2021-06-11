import undetected_chromedriver as uc
import time
import sys
import random

cred=open('credentials.properties','r').readlines()
usr=cred[0].split('=')[1].strip()
pas=cred[1].split('=')[1].strip()
all_comments=[f.strip() for f in open('comments.txt','r').readlines()]
print(f'Username : {usr}')
print(f'Password : {pas}')



def scroller():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



if __name__ == '__main__':
    count=int(input('''
    --> Enter 1 for Course Feedback Form
    --> Enter 2 for Teacher Feedback Form
    
        Enter Choice == >'''))

    driver=uc.Chrome()
    driver.get('https://qalam.nust.edu.pk/')
    time.sleep(10)
    driver.find_element_by_xpath('''//input[@placeholder='Login ID']''').send_keys(usr)
    time.sleep(0.5)
    driver.find_element_by_xpath('''//input[@placeholder='Password']''').send_keys(pas)
    time.sleep(2)
    driver.find_element_by_xpath('''//button[@type='submit']''').click()
    time.sleep(5)
    while True:
        chk=driver.current_url
        if chk=='https://qalam.nust.edu.pk/student/dashboard':
            break
        elif chk=='https://qalam.nust.edu.pk/web/login':
            print('Login Credentials Invalid...bot shutting down.')
            driver.quit()
            sys.exit()
        else:
            time.sleep(5)
            print('Waiting for Webpage to Login into Account ...')


    driver.get('https://qalam.nust.edu.pk/student/qa/feedback')
    time.sleep(7)
    try:
        if count==1:
            driver.find_element_by_xpath('''//a[starts-with(text(),'Course Feedback')]''').click()
        elif count==2:
            driver.find_element_by_xpath('''//a[starts-with(text(),'Teacher Feedback')]''').click()
        else:
            print('Invalid Choice of Forms...')
            print('Program Shutting Down')
            sys.exit()
    except Exception as e:
        print(f'Issue Occured | {e}')
        sys.exit()
    time.sleep(1)
    scroller()
    time.sleep(2)
    all_forms=driver.find_elements_by_xpath('''//a[@class='md-list-addon-element']''')
    a=1
    links_not_submitted=[]
    for f_links in all_forms:
        val=driver.find_element_by_xpath(f'''//ul[@id='tabs_anim1']//li//div//div[{a}]//ul//li[3]//div//span''').text
        if 'completed' in val.lower():
            a+=1
            continue
        else:
            link_grabbed=f_links.get_attribute('href')
            links_not_submitted.append(link_grabbed)
            a+=1
    if len(links_not_submitted)==0:
        print('No form Found Bot Shutting down...')
        sys.exit()
    print(f'''Total {len(links_not_submitted)} Forms are not submitted.....
    Starting To Fill Form.....
    ''')
    for ur in links_not_submitted:
        try:
            driver.get(ur)
            time.sleep(5)
            for j in range(1,21):
                evaluation_list=[1,2]
                num=random.choice(evaluation_list)
                driver.find_element_by_xpath(f'''//tbody//tr[{j}]//td[{num}]//input''').click()
                time.sleep(1)
            titleofcourse=driver.find_element_by_xpath('''//div[@class='col-lg-10']//h1[1]''').text
            driver.find_element_by_xpath('''(//span[text()='*'])[2]/following::textarea''').send_keys(random.choice(all_comments))
            time.sleep(4)
            driver.find_element_by_xpath('''//button[@type='submit']''').click()
            time.sleep(10)
            print(f'{titleofcourse} Submitted Successfully...')
        except Exception as e:
            print(f'Issue Occured While Filling Form | Issue | {e}\n')
            print('Moving to next Form....')

    print('All Task Completed Successfully Bot Shutting Down')
    driver.quit()
