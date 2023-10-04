from urllib.request import urlopen
import requests
from urllib.request import Request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'#每个爬虫必备的伪装
          }

import requests
from bs4 import BeautifulSoup

# Initialize a session
session = requests.Session()

# Add cookies to the session
cookies_dict = {
    'pl_authn': 'NzFjY2I1ZTk0OTdmZjUwMmRlNGI3YWVhNmY1YTI3NmYxZmQwYzg0MDhjMTYxNjZmY2E2Yzc4MTk3YjM5ODQ0YQ.lmf8qhmf.eyJ1c2VyX2lkIjoiMzUzMjU0IiwiYXV0aG5fcHJvdmlkZXJfbmFtZSI6IlNBTUwifQ',

    # Add other cookies here
}

session.cookies.update(cookies_dict)

# Use the session to get the page content
response = session.get('https://ca.prairielearn.com/pl/course_instance/4288/assessments')

# If the GET request is successful, the status code will be 200
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    from bs4 import BeautifulSoup




    # Find all rows in the table
    all_rows = soup.find_all('tr')

    # Initialize variables to keep track of the current assessment type
    current_assessment_type = None

    # Loop through each row
    for row in all_rows:
        # Try to find an assessment type in the row
        potential_assessment_type = row.find('th', {'data-testid': 'assessment-group-heading'})
        
        # Update the current assessment type if found
        if potential_assessment_type:
            current_assessment_type = potential_assessment_type.get_text(strip=True)
            print(f"------ {current_assessment_type} Info ------")
            continue  # Skip to the next iteration

        # Extract details (regardless of the type of assessment)
        badge_element = row.find('a', {'data-testid': 'assessment-set-badge'})
        title_element = row.find('td', {'class': 'align-middle'}).find_next_sibling('td') if row.find('td', {'class': 'align-middle'}) else None
        available_credit_element = row.find('td', {'class': 'text-center align-middle'})
        score_element = row.find('div', {'class': 'progress-bar bg-success'})

        # Print out details
        if badge_element and title_element and available_credit_element:
            print("------ Assessment Info ------")
            print(f"Assessment Type: {current_assessment_type}")
            print(f"Badge: {badge_element.get_text(strip=True)}")
            print(f"Link: {badge_element['href']}")
            print(f"Title: {title_element.get_text(strip=True)}")
            available_credit_text = available_credit_element.get_text(strip=True)
            first_line_of_credit = available_credit_text.split('\n')[0]
            print(f"Available Credit: {first_line_of_credit}")
            
            if score_element:
                print(f"Score: {score_element['style'].split(':')[1]}")
                
        print()


    # Your code to find and extract data goes here
else:
    print(f"Failed to retrieve the page, status code: {response.status_code}")

# Close the session
session.close()


