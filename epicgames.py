#For Gmail API
import  os
import  pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

import base64
import email
#For Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import names
import time
import re
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



#GMAIL API PART

SCOPES = ['https://mail.google.com/']
our_email = 'randomemail@gmail.com'


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service
service = gmail_authenticate()


def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def read_message(service, message_id):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)

def get_mime_message(service, msg_id):
  try:
    message = service.users().messages().get(userId='me', id=msg_id['id'],
                                             format='raw').execute()
    print('Message snippet: %s' % message['snippet'])
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
    mime_msg = email.message_from_string(msg_str)

    return message['snippet']
  except Exception as error:
    print('An error occurred: %s' % error)



def filter_number(text):
    #function to get verification code
    message = re.findall('[0-9]+', text)
    
    return message[0]

# results = search_messages(service,"Epic Games - Email Verification worki4@jhitsthose.shop")
# for msg in results:
#         #read_message(service, msg)
#         x= get_mime_message(service, msg)
#         print(filter_number(x))
#READ FILES
def read_proxy_list(list):
    a_file = open(list, "r")
    lines = a_file.readlines()
    a_file.close()
    
    return lines[0].strip()

def delete_proxy_one(list1,list2):
    a_file = open(list1, "r")

    lines = a_file.readlines()
    a_file.close()
    x = lines[0].strip()
    del lines[0]

    new_file = open(list1, "w+")

    for line in lines:
        new_file.write(line)
    new_file.close()

    b_file = open(list2,"r")
    lines2 = b_file.readlines()
    b_file.close()

    new_file2 = open(list2,'w+')
    new_file2.write('\n'+x)

    
    for linex in lines2:
        print("here" + linex)
        new_file2.write(linex)
    
    
   
    new_file2.close()




#Web Driver
def create_driver(proxy_ip):
    '''Takes in a given Ip adrres:port and creates a webdriver'''
    PROXY = proxy_ip
    PATH_CHANGED = 'path to web driver'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s'%PROXY)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36')
    options.add_argument('--start-maximized')
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    return webdriver.Chrome(options=options, executable_path=PATH_CHANGED)

############WEBSCRAPER PART########
###################################
###################################
###################################
# PROXY = "166.1.157.199:5416"


proxy_list_new=['166.1.150.88:8594', '166.1.154.85:6121', '166.1.144.191:6234', '166.1.153.12:5119', '166.1.154.111:6984', '166.1.148.132:5019', '166.1.145.159:8237', '166.1.146.87:8532', '166.1.158.70:8809', '166.1.151.190:8766', 
'166.1.148.80:7016', '166.1.152.104:9017', '166.1.144.138:7782', '166.1.154.127:8542', '166.1.158.32:7940', '166.1.144.101:7245', '166.1.156.202:5455', '166.1.148.9:7113', '166.1.150.17:7067', '166.1.148.152:5986', '166.1.149.14:5660', '166.1.145.124:6332', '166.1.158.43:8547', '166.1.146.5:7135', '166.1.154.185:8582', '166.1.155.208:5948', '166.1.155.148:8342', '166.1.144.122:8773', '166.1.149.203:5684', '166.1.150.229:7670', '166.1.155.18:8402', '166.1.157.192:7371', '166.1.151.46:5458', '166.1.153.108:5546', '166.1.156.69:9078', '166.1.153.26:5366', '166.1.157.86:6736', '166.1.152.28:5606', '166.1.148.142:8201', '166.1.150.82:6857', '166.1.146.217:8617', '166.1.152.252:7119', '166.1.148.226:8511', '166.1.147.26:6016', '166.1.154.247:6503', '166.1.155.232:5836', '166.1.150.92:6659', '166.1.157.19:8901', '166.1.146.105:9075', '166.1.157.199:5416']

proxy_list_trash = []
account_count = 101
def make_account():
    #Authenticate gmail
    service = gmail_authenticate()

    global account_count
    randomNum = random.randint(1000, 9999)
    randomNum2 = random.randint(10, 99)
    generated_FirstName = names.get_first_name()
    generated_LastName = names.get_last_name()
    generated_email = generated_FirstName + generated_LastName +str(account_count) + "@jhitsthose.shop"
    generated_DisplayName = generated_FirstName + str(randomNum) + str(randomNum2)
    
    proxt_to_use = read_proxy_list("proxylistgood.txt")
    print("Current Proxy" + proxt_to_use)
    driver = create_driver(proxt_to_use)

    actions = ActionChains(driver)

    google_signup_page = 'https://www.google.com/search?q=epic+games+sign+up&oq=epic+games+sig&aqs=chrome.1.0i433j0j69i57j0l2j69i60l3.4093j0j7&sourceid=chrome&ie=UTF-8'
    sign_up_page = 'https://www.epicgames.com/id/register'

    driver.get(google_signup_page)
    time.sleep(2)

    sign_up_link = driver.find_element_by_partial_link_text('Register for an Epic')

    sign_up_link.click()
    time.sleep(2)

    sign_up_by_email = driver.find_element_by_id('login-with-epic')
    sign_up_by_email.click()
    time.sleep(3)


    ####FOR AMERICAN IP
    try:
        month_field = driver.find_element_by_id('month')
        month_field.click()
        time.sleep(1)

        random_month = random.randint(0,11)
        month_path = "//li[@data-value=" + "'"+str(random_month) + "']"
        specific_month = driver.find_element_by_xpath(month_path)
        specific_month.click()
        time.sleep(1)

        day_field = driver.find_element_by_id('day')
        day_field.click()
        time.sleep(1)

        random_date = random.randint(1,31)
        date_path = "//li[@data-value=" + "'"+str(random_month) + "']"
        date = driver.find_element_by_xpath(date_path)
        date.click()
        time.sleep(0.5)

        random_year = random.randint(1990,2000)
        year=driver.find_element_by_id('year')
        year.send_keys(str(random_year))
        time.sleep(0.5)

        continue_btn = driver.find_element_by_id('continue')
        continue_btn.click()
        time.sleep(1)
    except:
        pass  




    first_name = driver.find_element_by_id('name')
    first_name.send_keys(generated_FirstName)
    time.sleep(1.7)
    last_name = driver.find_element_by_id('lastName')
    last_name.send_keys(generated_LastName)
    time.sleep(1.5)
    display_name = driver.find_element_by_id('displayName')
    display_name.send_keys(generated_DisplayName)
    time.sleep(3)
    email_address = driver.find_element_by_id('email')
    email_address.send_keys(generated_email)
    time.sleep(1)
    password = driver.find_element_by_id('password')
    password.send_keys('Th1sWi11W0rk!!')
    time.sleep(2)
    tos = driver.find_element_by_id('tos')
    tos.click()
    time.sleep(1.5)
    continue_button = driver.find_element_by_id('btn-submit')
    continue_button.click()
    time.sleep(6)
    
    print('Waiting 20 seconds')

   
    verification_box = driver.find_element_by_name('code-input-0')
   
    time.sleep(23)

    account_count +=1
    ######Part to get verification from Gmail Api
    search_paramiter = "Epic Games - Email Verification" + " " + generated_email
    results = search_messages(service, search_paramiter)
    verification_Code = ""
    for msg in results:
        #read_message(service, msg)
        x= get_mime_message(service, msg)
        print(x)
        verification_Code += filter_number(x)
        
    print(verification_Code + "hereeeeeee")

    count = 0
    attempt_ver = 0
    waitingTime_ver = 90
    while((len(verification_Code)) != 6):
        print(count)
        search_paramiter = "Epic Games - Email Verification" + " " + generated_email
        results = search_messages(service, search_paramiter)
        
        for msg in results:
             #read_message(service, msg)
            x= get_mime_message(service, msg)
            print(x)
            verification_Code += filter_number(x)
        if(len(verification_Code) ==6):
                break
        time.sleep(10)   
        if (attempt_ver ==waitingTime_ver):
            break         
        attempt_ver += 10
        count+= 1

    print("typing code now")
    try:
        verification_box.send_keys(verification_Code)
        time.sleep(1.5)
        verify_continue = driver.find_element_by_id('continue')
        verify_continue.click()
    except: 
        reSend = driver.find_element_by_id('resend-email')
        reSend.click()

        attemps = 0
        waitingTime = 18
        while((len(verification_Code)) != 6):

            search_paramiter = "Epic Games - Email Verification" + " " + generated_email
            results = search_messages(service, search_paramiter)
            verification_Code = ""
            for msg in results:
                #read_message(service, msg)
                x= get_mime_message(service, msg)
                print(x)
                verification_Code += filter_number(x)
            if(len(verification_Code) ==6):
                break
            time.sleep(5)
            attemps += 1
            print(attemps)
            if(attemps == waitingTime):
                attemps = 0
                waitingTime += waitingTime
                reSend = driver.find_element_by_id('resend-email')
                reSend.click()
            #leave if takes longer than 3 mins
            if(attemps == 37):
                break
        verification_box.send_keys(verification_Code)    
        time.sleep(1)
        verify_continue = driver.find_element_by_id('continue')
        verify_continue.click()    

    else:
        print("Verification bypassed") 
    
    time.sleep(5)


    ####################
    ##NOW TO GET FREE NITRO##
    #########################
    new_url = 'https://www.epicgames.com/store/en-US/p/discord--discord-nitro'
    driver.execute_script("window.open('');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)
    driver.get(new_url)
    time.sleep(3)

    try:
        Get = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/main/div/div[3]/div/div/div[2]/div[2]/div/aside/div/div/div[4]/div/button")
        Get.click()

        time.sleep(1.5)

        acceptTOS = driver.find_element_by_id('agree')
        acceptTOS.click()

        time.sleep(1)
        
        acceptButton = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[2]/div/div[2]/button')
        location_of_acceptButton = acceptButton.location
        # actions.move_to_element_with_offset(acceptButton,50,100).perform()
        time.sleep(1)
        acceptButton.click()

        time.sleep(4)
        print("clicked")

        x_int = location_of_acceptButton['x']
        y_int = location_of_acceptButton['y']
        actions.move_by_offset(x_int + 50, y_int+ 100)

        actions.click().perform()
        time.sleep(2)
        account_count+= 1
        driver.quit()
    except:
        driver.quit()
        



def main():
    make_money = True
    while (make_money):
        try:
            make_account()
        except:
            delete_proxy_one("proxylistgood.txt","proxyused.txt")
        print("New Driver")

if __name__ == "__main__":
    main()