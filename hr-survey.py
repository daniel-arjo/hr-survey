import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import urllib
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os # Added to automatically create folders

####### INITIAL CONFIGURATION AND SECURITY
# Using relative paths to ensure the code runs on any machine
data_folder = r"data/"
input_path = f"{data_folder}offboarding_base.xlsx"

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

####### READ DATABASE AND BROWSER CHECK-IN
# The Excel file must contain the columns: "Name", "Phone", "CS"
employees_df = pd.read_excel(input_path)

## Browser initialization
browser = webdriver.Chrome()
browser.get("https://web.whatsapp.com/")

WebDriverWait(browser, 90).until(
    EC.presence_of_element_located((By.ID, "side"))
)

####### EMPLOYEE LISTING

today = datetime.now().date()
send_to = employees_df

number_of_people = send_to.shape[0]
print(f"The number of people who will receive the messages is: {number_of_people}")
input("Press Enter to start sending the messages...")

# Create a list to save the categorized data
sending_result = []

####### START SENDING SCRIPT

for i, row in send_to.iterrows():
    person = row["Name"]
    phone = row["Phone"]
    cs = row["CS"]
    
    # Anonymization of company data and virtual assistant name
    message = f'''Hello, {person}! 🌟

Welcome to the *[Your Company] Employee Experience Virtual Assistant, [Assistant Name]*!

We are currently conducting an *Offboarding Survey* and would be very grateful for your collaboration.

_This is an *anonymous survey*, therefore, there are no gains or losses associated with taking it._

*Would you like to contribute your opinion to this survey?*
_Note: Audio messages are not accepted._

_Please reply with_ *Yes* _or_ *No*'''
    
    link = f"https://web.whatsapp.com/send?phone=55{phone}&text={urllib.parse.quote(message)}"
    
    browser.get(link)
    
    try:
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p/span'))
        )
        
        browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p/span').send_keys(Keys.ENTER)
        time.sleep(7)
        
        sending_result.append({"CS": cs, "Name": person, "Phone": phone, "Status": "Sent"})
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error sending message to {person} ({phone}): {e}")
        sending_result.append({"CS": cs, "Name": person, "Phone": phone, "Status": "Not Sent"})

####### SAVE RESULT TO EXCEL FILE

result_df = pd.DataFrame(sending_result)
file_name = f"{data_folder}log_offboarding_ROUTINE_{today.strftime('%Y-%m-%d')}.xlsx"
result_df.to_excel(file_name, sheet_name="Result", index=False)
print(f"Sending completed and results saved in the file '{file_name}'.")

####### LOGOUT FROM BROWSER

# Log out of WhatsApp before closing the browser
try:
    # Click the gear button (settings)
    browser.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/header/div/div/div/div/span/div/div[3]/div[1]/button/div/span').click()
    time.sleep(2)

    # Click the 'Log out' option
    browser.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/div/span/div/div/div/div[2]/div/div/div/button[9]').click()
    time.sleep(2)

    # Confirm logout by clicking the 'Log out' button
    browser.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div/button[2]').click()
    time.sleep(2)

    print("Logout successful.")
except NoSuchElementException as e:
    print(f"Error trying to log out: {e}")
except TimeoutException as e:
    print(f"Time exceeded when trying to log out: {e}")

# Close the browser
browser.quit()