import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Context, put the site in full screen just in case
context = { #This context can be used for when you device to implement some sort of AI to generate Cover Letters
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

driver.get("https://asu.joinhandshake.com/login?ref=app-domain") #This directly accesses the login page with credentials accessed via a local .env file
username = os.getenv("HANDSHAKE_EMAIL")
password = os.getenv("HANDSHAKE_PASSWORD")

# Logging in: You are going to need to auth using Duo, Change this as necessary to suit your needs
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'main')]")) 
)
clickHere = driver.find_element(By.XPATH, ".//div[contains(@id, 'sso-name')]")
clickHere.click()

mainArea = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "main"))
)
usernameBox = mainArea.find_element(By.XPATH, ".//input[contains(@id, 'username')]")
passwordBox = mainArea.find_element(By.XPATH, ".//input[contains(@id, 'password')]")
signIn = mainArea.find_element(By.XPATH, ".//input[contains(@type, 'submit')]")
usernameBox.send_keys(username)
passwordBox.send_keys(password)
signIn.click()

# Navigating to job postings
WebDriverWait(driver, 30).until(
    EC.url_contains("https://asu.joinhandshake.com/explore")
)
time.sleep(4)
driver.get("https://app.joinhandshake.com/stu/postings")

firstDiv = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, ".//div[contains(@data-hook, 'search-results')]"))
)

#This entire pages grabs the amount of jobs available within the page, this determines how many times the page will change
pagination = firstDiv.find_element(By.XPATH, ".//div[contains(@class, 'style__pagination___XsvKe')]")
rangeDetermination = pagination.find_element(By.XPATH, ".//div[contains(@class, 'style__page___skSXd')]")
range_text = rangeDetermination.text
total_pages = int(range_text.split("/")[1].strip()) #turn ripped text into an integer to determine loop amount
print(f"The total number of pages is: {total_pages}")

for i in range(total_pages):
    jobs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, ".//a[starts-with(@id, 'posting')]")) #identify how many jobs to loop through
    )
    print(f"The number of jobs is: {len(jobs)}") #get the length of the jobs (more so for testing purposes)

    for job in jobs: #loop through each job object which will consist of static things, like it's preview, the apply button, etc
        try:
            job.click()

            secondDiv = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@aria-label, 'Job Preview')]")) #wait for the preview the populate
            )
            applyDiv = WebDriverWait(secondDiv, 5).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'style__containerV2___FWwC5')]")) #wait for the apply div to populate
            )

            requirements_text_fragments = [
                element.text.strip()
                for element in applyDiv.find_elements(By.XPATH, ".//p | .//li | .//a")
            ]
            requirements = "\n".join(requirements_text_fragments) #Again, this piece of code is for if you want to use AI to generate a cover letter.

            #print("Found job preview div.") #for testing

            applyButton = WebDriverWait(applyDiv, 5).until(
                EC.element_to_be_clickable((By.XPATH, ".//span[text()='Apply']")) #Identify the apply button (Specifically if it says 'Apply' and is clickable)
            )                                                                     #There is a case where it says apply but is greyed out because it is no longer available
            applyButton.click()

            # Handling the application modal
            application_completed = False #Set application being complete to false to control when the loop ends
            while not application_completed:
                modal = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//span[contains(@data-hook, 'apply-modal-content')]"))
                ) #A new modal is created that appears at the bottom of the <body> tag that has a data hook of apply-modal-content

                if not modal: #break out of the loop if the modal does not appear (this case rarely happens but happened once)
                    break

                submitApplication = WebDriverWait(modal, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//span[contains(@data-hook, 'submit-application')]")) #Identify the submit application button, should be unclickable at first
                )

                fieldsets = modal.find_elements(By.TAG_NAME, "fieldset") #these are the things that the job application requires, like a resume, cover letter, transcripts, etc
                amountRequired = len(fieldsets) #get the length to determine the loop amount

                # if amountRequired > 2: #Earlier implementation, leaving it here for now but originally only took into consideration jobs that required 1
                #     print(f"Job skipped because it has {amountRequired} fieldsets.")
                #     dismissButton = modal.find_element(By.XPATH, ".//button[starts-with(@class, 'style__dismiss___') and contains(@aria-label, 'dismiss')]")
                #     dismissButton.click()
                #     break

                try:
                    if amountRequired == 0:
                        print("Just asked to submit the application: submit")
                        application_completed = True
                        submitApplication.click()

                    if amountRequired == 1:
                        if fieldsets[0].find_elements(By.TAG_NAME, "svg"): #Needed to find how to determine when it has the information it needs
                                                                           #Turns out, completed fieldsets will have a green svg on them. no svg exists without it
                            print("Single fieldset, resume autopopulated. Submitting application.")
                            application_completed = True
                            submitApplication.click()
                        else:
                            print("Single fieldset, resume not autopopulated. Clicking the first span.") #This is just one way to do it, Handshake uses react, logic is below
                            recentlyAddedSection = modal.find_elements(By.XPATH, ".//div[starts-with(@class, 'style__suggested___')]")
                            first_span = recentlyAddedSection[0]
                            first_span.click()
                            application_completed = True
                            submitApplication.click()

                    elif amountRequired == 2: #each one needs time to load, no doubt.
                        # Handling the first fieldset
                        if not fieldsets[0].find_elements(By.TAG_NAME, "svg"):
                            print("First fieldset not autopopulated. Clicking the first span.")
                            recentlyAddedSection = modal.find_elements(By.XPATH, ".//div[starts-with(@class, 'style__suggested___')]")
                            recentlyAddedSection[0].click()

                        # Handling the second fieldset
                        if fieldsets[1].find_elements(By.TAG_NAME, "svg"):
                            print("Second fieldset autopopulated. Submitting application.")
                            application_completed = True
                            submitApplication.click()
                        else: #for cover letters, the below logic works 100%, for other shits, i may have to choose another type of indexing, but using if's works fine
                            print("Second fieldset not autopopulated. Handling dropdown selection.")
                            selectArrow = fieldsets[1].find_element(By.XPATH, ".//span[contains(@class, 'Select-arrow')]")
                            time.sleep(2)
                            selectArrow.click()
                            time.sleep(4)
                            item = fieldsets[1].find_element(By.XPATH, ".//div[contains(@class, 'Select-menu-outer')]")
                            time.sleep(3)
                            item.find_elements(By.XPATH, ".//*")[3].click()
                            time.sleep(2)
                            application_completed = True
                            submitApplication.click()
                    
                    else:
                        i = 0
                        for fieldset in fieldsets:  #This is the method that should exist for all cases, The question is both speed and consistency. 
                                                    #there are times where this break for no reason and by that, I mean that someones the react elements
                                                    #refuse to populate when the selectArrow object is clicked. Hopefully this can be optimized later      
                            if not fieldset.find_elements(By.TAG_NAME, "svg"):
                                print(f"fieldset{i} not populated, attempting to populate")
                                selectArrow = fieldset.find_element(By.XPATH, ".//span[contains(@class, 'Select-arrow')]")
                                time.sleep(2)
                                selectArrow.click()
                                time.sleep(4)
                                item = fieldset.find_element(By.XPATH, ".//div[contains(@class, 'Select-menu-outer')]")
                                time.sleep(3)
                                item.find_elements(By.XPATH, ".//*")[3].click()
                                time.sleep(2)
                                i += 1 # should double check if fieldset is populated before incrementing i, not implemented yet
                                if i == len(fieldsets):
                                    application_completed = True
                                    submitApplication.click() 


                except Exception as e: #Catch exceptions, used basic exceptions with a lack of specificity for now
                    print(f"There was an error processing fieldsets: {e}")

        except Exception as e: #Catch exceptions, used basic exceptions with a lack of specificity for now
            print(f"Error on page {i}: {e}")

    nextPage = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[contains(@data-hook, 'search-pagination-next')]"))
    )
    nextPage.click() #The code uses to invoke pagination.

driver.quit()
