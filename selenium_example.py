from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np

# Use Webdriver Chrome
driver = webdriver.Chrome()

# URL of the webpage I want to interact with
url = 'https://www.lotto.pl/eurojackpot/wyniki-i-wygrane?plc=glowna-popularne-gry-wyniki'  

# Open driver with this url
driver.get(url)

# Close messages
button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[4]/div[2]/div[3]/div/button')
button.click()

driver.implicitly_wait(5)
button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div[2]/button')
button.click()

# After each scroll interact with button
memory = "start"
while True:
    updated_html_content = driver.page_source
    # Wait to load page
    driver.implicitly_wait(1)
    
    # I use memory, becouse I want to make sure there is no button anymore
    # Memory is double check. Must be two exception to terminate this function
    try:
        button = driver.find_element(By.CLASS_NAME, 'more-results')
        button.click()
        memory = "ok"
    except:
        if memory == "error":
            # When we have no more buttons, then we end function
            break
        memory = "error"


# Interact with all buttons responible for sorting data.
driver.execute_script("window.scrollTo(0, 0);")
buttons = driver.find_elements(By.CLASS_NAME, 'white-number-box__sign--btn')

# I used js click to interact with hidden elements
for button in buttons:
    driver.execute_script("arguments[0].click();", button)

# Wait to reload page
driver.implicitly_wait(2)

# Get the updated HTML
updated_html_content = driver.page_source

# Close the driver
driver.quit()

# Transform page into BeautifulSoup
soup = BeautifulSoup(updated_html_content, 'html.parser')

# Extract data
games = soup.find_all("div", attrs={"class":"recent-result-item EuroJackpot"})

# Save data in this list
result = []

for game in games:
    # Find raw div with score
    scores = game.find_all("div", attrs={"class":"result-item__balls-box"})

    for score in scores:
        numbers = score.find_all("div")

        new_result = []
        for number in numbers:    
            new_result.append(int(number.text))
            
        result.append(new_result)

# Convert the Python list to a NumPy array
games_data = np.array(result, dtype=np.int16)

# Sava as csv
file_name = "score.csv"
np.savetxt(file_name, games_data, fmt="%.f", delimiter=",")
        
print("END")
