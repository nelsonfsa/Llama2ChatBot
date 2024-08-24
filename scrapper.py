from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from chatbot import answer_question
from typing import List
import time


bot_name = "Nelson" #Your name displayed in the discord channel
target_name = "nownz1"
discord_channel_url = "https://discord.com/channels/@me/689819417185484840"


options = webdriver.ChromeOptions() 
options.add_argument('--user-data-dir=C:/Users/Nelson/AppData/Local/Google/Chrome/User Data')
options.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(options=options)
driver.get(discord_channel_url)

all_msgs_class = "messageListItem_d5deea"
msg_class = "messageContent_f9f2ca"
username_class= "username_f9f2ca"
input_class = "editor_a552a6"


def send_message(msg):
    #Gets send input and sends a message
    search = driver.find_element(By.CLASS_NAME, input_class)
    search.send_keys(msg)
    search.send_keys(Keys.RETURN)
    return True

def get_last_message(messages_list : List[WebElement]) -> str:
    #Reads the last message
    last_msg_div = messages_list.pop()
    message = ""

    if has_today_at_in_second_line(last_msg_div.text):
        #Cuts the first two lines which are 
        #Target Name
        #Today at 3:53 PM
        lines = last_msg_div.text.splitlines()
        message = "\n".join(lines[2:])
    else:
        message = last_msg_div.text

    return message

def has_today_at_in_second_line(string):
    """
    Checks if the second line of a string starts with "Today at".

    Args:
        string: The input string.

    Returns:
        True if the second line starts with "Today at", False otherwise.
    """

    lines = string.splitlines()
    if len(lines) >= 2 and lines[1].startswith("Today at"):
        return True
    else:
        return False

def get_last_author(msg_list : List[WebElement]) -> str:
    if len(msg_list) == 0:
        return ""
    msg_index = len(msg_list) - 1

    has_found = False
    while(not has_found or msg_index == 0):
        try:
            msg_list[msg_index].find_element(By.CLASS_NAME, username_class)
            return msg_list[msg_index].find_element(By.CLASS_NAME, username_class).text
        except NoSuchElementException:
            msg_index -= 1
            print("Element not found")

    if msg_index == 0:
        return ""

def get_author(message : WebElement):
    return  message.find_element(By.CLASS_NAME, username_class).text

timer = 0
while True:

    try:
        # Wait for the initial list of messages
        all_msgs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, all_msgs_class))
        )

        current_author = get_last_author(all_msgs)
        current_message = get_last_message(all_msgs)
        
        if current_author == target_name:
            ai_answer = answer_question(current_message)
            send_message(ai_answer)
            timer = 0
        else:
            print("Waiting for new message from target...  timer: " + str(timer)+" seconds.")
            timer += 5
            time.sleep(5)  # Add a 5-second delay    

    except StaleElementReferenceException:
         all_msgs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, all_msgs_class))
        )
        




