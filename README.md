# HandShake-QuickApply-Bot
Helps quick apply to a plethora of jobs available on Handshake, specifically, the ASU version. This should easily help students apply to jobs quickly, especially useful for Juniors and Seniors looking for jobs in their relevant field

This project automates job applications on the Handshake platform using Selenium and the Chrome WebDriver. It simulates user actions to log in, navigate to job postings, and apply to jobs based on certain conditions.

Features
    Login Automation: Automates the login process using credentials stored in environment variables.
    Job Posting Scraper: Navigates to job postings and extracts job details.
    Automated Application: Automatically applies to job postings where the application requirements are already satisfied or       minimal user input is needed.
    Pagination Handling: Iterates over multiple pages of job listings and applies to all available jobs.
    Dynamic Form Handling: Handles various job application forms, identifying which fields are pre-populated and which require     input.

Before running the script, make sure you have the following:

    Python 3.x installed on your system. You can achieve this by downloading python from their website (https://www.python.org/downloads/)
    Selenium for browser automation:  pip install selenium
    WebDriver Manager for automatic ChromeDriver Management: pip install webdriver-manager
    dotenv to manage environment variables: pip install python-dotenv
    Google Chrome installed on your machine. (Make sure it is the latest version as the code in the file will utilize the most recent version.

Environment Setup 
(The section below is if you add code that can utilize AI to create cover letters and things of that nature)
You'll need a .env file with the following environment variables for secure handling of credentials and user data:
# .env file
    HANDSHAKE_EMAIL=your_handshake_email
    HANDSHAKE_PASSWORD=your_handshake_password
    NAME=your_name
    LINKEDIN_EMAIL=your_linkedin_email
    Phone_Number=your_phone_number
    Residency=your_location
    Employed_Currently=employed_status (yes/no)
    Need_Visa=visa_status (yes/no)
    YearsOfCoding=number_of_years_of_experience
    EXPERIENCE=description_of_experience
    LanguagesKnown=languages_you_speak
    CodingLanguagesKnown=coding_languages_you_know
Create a .env file in the project root directory with your Handshake login details and additional context details as shown above.

To run the script, follow these steps:

    Open a terminal and navigate to the project directory.
    Run the Python script:
      python your_script_name.py
The script will:
    Open Chrome and navigate to the Handshake login page.
    Log in using your credentials.
    Iterate through job postings and apply to each job where the requirements are met.

Handling Duo Authentication
If your institution uses Duo authentication for Handshake login, you will need to authenticate manually when prompted by Duo. The script waits until the authentication is complete.

How the Script Works
Login Process:
    The script starts by logging in using the credentials from the .env file. Once logged in, it navigates to the job postings page.

Job Posting Scraper:
    The script identifies all available job postings on the current page. For each job, it opens the job details and checks if the application requirements are already satisfied.

Automated Application:
    If the job application requirements (e.g., resume, cover letter) are pre-populated, the script submits the application automatically. The script uses logic to handle multiple form fields, including dropdowns and input fields, based on the number of required fields.

Pagination: 
    After completing the applications on the current page, the script navigates to the next page and repeats the process until all jobs have been processed.

Potential Improvements
AI Integration:
    The context dictionary allows for potential integration of AI-generated cover letters or additional automation around personalized job applications.
Error Handling:
    Basic error handling is in place, but improvements can be made by adding more specific exceptions.
    
Disclaimer:
    This script is for educational and personal use only. Please ensure that automating job applications complies with the terms of service of the platforms you're using, such as Handshake. Use at your own discretion.

Author
    Developed by Pernell Louis-Pierre.
