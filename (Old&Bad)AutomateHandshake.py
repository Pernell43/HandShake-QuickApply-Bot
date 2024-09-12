import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
# from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#Context, put the site in full screen just in case

context = {
    "name": os.getenv('NAME'),
    "email": os.getenv('LINKEDIN_EMAIL'),
    "phone": os.getenv('Phone_Number'),
    "location": os.getenv('Residency'),
    "currently employed": os.getenv('Employed_Currently'),
    "Need a Visa": os.getenv('Need_Visa'),
    "Years of Coding": os.getenv('YearsOfCoding'),
    "Experience": os.getenv('EXPERIENCE'),
    "Languages Known": os.getenv('LanguagesKnown'),
    "Coding Languages Known": os.getenv('CodingLanguagesKnown')
}

driver.get("https://asu.joinhandshake.com/login?ref=app-domain")
username = os.getenv("HANDSHAKE_EMAIL")
password = os.getenv("HANDSHAKE_PASSWORD")

time.sleep(2)
page2 = driver.find_element(By.XPATH, ".//div[contains(@class, 'main')]")
clickHere = page2.find_element(By.XPATH, ".//div[contains(@id, 'sso-name')]").click()

time.sleep(2)
mainArea = driver.find_element(By.TAG_NAME, "main")
signIn = mainArea.find_element(By.XPATH, ".//input[contains(@type, 'submit')]")
usernameBox = mainArea.find_element(By.XPATH, ".//input[contains(@id, 'username')]")
passwordBox = mainArea.find_element(By.XPATH, ".//input[contains(@id, 'password')]")
time.sleep(5)
usernameBox.send_keys(username)
passwordBox.send_keys(password)
signIn.click()
time.sleep(15)

driver.get("https://app.joinhandshake.com/stu/postings")
time.sleep(5)

firstDiv = driver.find_element(By.XPATH, ".//div[contains(@data-hook, 'search-results')]")
pagination = firstDiv.find_element(By.XPATH, ".//div[contains(@class, 'style__pagination___XsvKe')]")
nextPage = pagination.find_element(By.XPATH, ".//button[contains(@data-hook, 'search-pagination-next')]")
rangeDetermination = pagination.find_element(By.XPATH, ".//div[contains(@class, 'style__page___skSXd')]") #will need these pages for the for i in range loop after finishing
range_text = rangeDetermination.text
total_pages = int(range_text.split("/")[1].strip())
print(f"The total number of pages is: {total_pages}")

#this needs be to tailored to adapt for 2 or 3 different kinds of modals, same reach-portal element tho
#
script = """
document.addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default action
    let clickedElement = event.target;
    console.log('Clicked Element:', clickedElement);
    console.log('Tag Name:', clickedElement.tagName);
    console.log('Class List:', clickedElement.className);
    console.log('ID:', clickedElement.id);
    console.log('HTML Content:', clickedElement.outerHTML);
    alert('You clicked on a ' + clickedElement.tagName + ' element with class: ' + clickedElement.className);
});
# """

# driver.execute_script(script)

for i in range(total_pages):
    time.sleep(3)
    jobs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, ".//a[starts-with(@id, 'posting')]"))
    )
    number_of_jobs = len(jobs)
    print(f"the number of jobs is: {number_of_jobs}")

    for job in jobs:
        try:
            job.click()

            secondDiv = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@aria-label, 'Job Preview')]"))
            )
            applyDiv = WebDriverWait(secondDiv, 5).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'style__containerV2___FWwC5')]"))
            )

            requirements_text_fragments = []
            elements_to_extract = applyDiv.find_elements(By.XPATH, ".//p | .//li | .//a") #need to double check, but this would edit the requirement global variable for 
            for element in elements_to_extract:                                             #the cover letter creation.
                requirements_text_fragments.append(element.text.strip())
            requirements = "\n".join(requirements_text_fragments)

            print("Found job preview div.")
            applyButton = WebDriverWait(applyDiv, 5).until(
                EC.element_to_be_clickable((By.XPATH, ".//span[text()='Apply']"))
            )
            applyButton.click()
            #Need to check if the modal opened or not, if the modal is not detected, it should not go through that loop
            application_completed = False
            #run the application now set it equal to true after the submit application button is clicked
            while not application_completed:
                try:
                    modal = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ".//span[contains(@data-hook, 'apply-modal-content')]"))
                    )#necessary modal

                    if not modal:
                        break
                    else:
                        submitApplication = WebDriverWait(modal, 10).until(
                            EC.element_to_be_clickable((By.XPATH, ".//span[contains(@data-hook, 'submit-application')]"))
                        )#submit application button identified
                        
                        fieldsets = modal.find_elements(By.TAG_NAME, "fieldset")

                        amountRequired = len(fieldsets)

                        if amountRequired == 1:
                            try:
                                if fieldsets[0].find_element(By.TAG_NAME, "svg"):
                                    print("There is only 1 fieldset, which is the resume, and the resume is autopopulated. Submitting the application.")
                                    application_completed = True
                                    submitApplication.click()
                            except NoSuchElementException:
                                #if no svg is found, handle the span click scenario
                                print("There is only 1 fieldset, but the resume is not autopopulated. Clicking the first span.")
                                recentlyAddedSection = modal.find_elements(By.XPATH, ".//div[starts-with(@class, 'style__suggested___')]")
                                first_span = recentlyAddedSection[0]
                                first_span.click()
                                application_completed = True
                                submitApplication.click()

                        elif amountRequired == 2:
                            
                            try:
                                if fieldsets[0].find_element(By.TAG_NAME, "svg"):
                                    print("There is only 1 fieldset, which is the resume, and the resume is autopopulated.")
                            except NoSuchElementException:
                                #if no svg is found, handle the span click scenario
                                print("There is only 1 fieldset, but the resume is not autopopulated. Clicking the first span.")
                                recentlyAddedSection = modal.find_elements(By.XPATH, ".//div[starts-with(@class, 'style__suggested___')]")
                                first_span = recentlyAddedSection[0]
                                first_span.click()

                            try:
                                if fieldsets[1].find_element(By.TAG_NAME, "svg"):
                                    print("second fieldset, which is the cv/other docs/anything else, and it is autopopulated. Submitting the application.")
                                    application_completed = True
                                    submitApplication.click()
                            except NoSuchElementException:
                                #if no svg is found, handle the span click scenario
                                print("second fieldset, but the cv/other docs/anything else is not autopopulated. drop down operation")
                                selectArrow = fieldsets[1].find_element(By.XPATH, ".//span[contains(@class, 'Select-arrow')]")
                                time.sleep(1)
                                selectArrow.click()
                                time.sleep(2)
                                item = fieldsets[1].find_element(By.XPATH, ".//div[contains(@class, 'Select-menu-outer')]")
                                time.sleep(2)
                                child_elements = item.find_elements(By.XPATH, ".//*")
                                # time.sleep(1)
                                # for index, child in enumerate(child_elements):
                                #     print(f"Child {index + 1}:")
                                #     print(f"Tag Name: {child.tag_name}")
                                #     print(f"Text: {child.text}")
                                #     print(f"Class: {child.get_attribute('class')}")
                                #     print(f"ID: {child.get_attribute('id')}")
                                #     print("\n" + "="*50 + "\n")
                                # time.sleep(20)
                                # first_option = item.find_element(By.ID, "react-select-12--option-0")
                                child_elements[0].click() #for the first option
                                # options = item.find_elements(By.XPATH, ".//div[starts-with(@id, 'react-select-12--option')]")
                                # for option in options:
                                #     print(f"If exists: {option}")
                                # options[0].click()
                                time.sleep(1)
                                # recentlyAddedSection = fieldsets[1].find_elements(By.XPATH, ".//div[starts-with(@class, 'style__suggested___')]")
                                # first_span = recentlyAddedSection[0]
                                # first_span.click()
                                application_completed = True
                                submitApplication.click()

                        else:
                            dismissButton = modal.find_element(By.XPATH, ".//button[starts-with(@class, 'style__dismiss___') and contains(@aria-label, 'dismiss')]")
                            dismissButton.click() #eventually this needs to be changed to handle ones that ask another questions, and there are at least 3 different cases.
                            break
                        #     try:        
                        #         prompt = f"Come up with a cover leter for me that given the following context of {context} and the requirements of the job which are the follow: {requirements}"
                        #         #trying to incorporate grammaly.py
                        #         for question in fieldsets:
                        #             time.sleep(2)
                        #             first_span = question.find_elements(By.TAG_NAME, "span")[0]
                        #             time.sleep(1)
                        #             first_span.click()
                        #             time.sleep(1)
                        #     except Exception as e:
                        #         print(f"There was an error: {e}")

                except Exception as e:
                    print(f"shit crashed on page {i}")
                    print(f"there was an error: {e}")
            #Loop Split##############################################################################################################
        except Exception as e:
            print(f"shit crashed on page {i}")
            print(f"There was an error: {e}")

    firstDiv = driver.find_element(By.XPATH, ".//div[contains(@data-hook, 'search-results')]")
    pagination = firstDiv.find_element(By.XPATH, ".//div[contains(@class, 'style__pagination___XsvKe')]")
    nextPage = pagination.find_element(By.XPATH, ".//button[contains(@data-hook, 'search-pagination-next')]")
    time.sleep(5)
    nextPage.click()
    


time.sleep(100)


#I should be waiting for the modal to disappear before going to the next application
