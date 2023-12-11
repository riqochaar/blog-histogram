# WEB SCRAPING
# Import modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Configure chrome driver
pathDriver = 'chromedriver.exe'
s = Service(pathDriver)
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service = s, options = options)

# Extract video data from channel
website = 'https://www.premierleague.com/stats/top/players/goals'
driver.get(website)

# Dictionary to locate buttons to click
buttons = {
    'Accept All Cookies' : '//*[@id="onetrust-accept-btn-handler"]',
    'Close Advert' : '//*[@id="advertClose"]',
    'Filter by Season' : '//*[@id="mainContent"]/div[2]/div[1]/section/div[2]',
    'All Seasons' : '//*[@id="mainContent"]/div[2]/div[1]/section/div[2]/div[3]/ul/li[1]',
    'Next Page' : '/html/body/main/div[2]/div[1]/div[2]/div[2]'
}

# Click the buttons above
for b in buttons.keys():
    print(b)
    if b != 'Next Page':
        button = driver.find_element(By.XPATH, buttons[b])
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

# Get player information (name and number of goals scored)
playerInfo = {}
end = False
loop = -1
while True:
    loop += 1
    playerName = driver.find_elements(By.CLASS_NAME, 'playerName')
    playerCountry = driver.find_elements(By.CLASS_NAME, 'playerCountry')
    playerGoals = driver.find_elements(By.CLASS_NAME, 'stats-table__main-stat')

    for i, (n, c, g) in enumerate(zip(playerName, playerCountry, playerGoals)):
        name = n.text
        country = c.text
        goals = int(g.text)
        index = str(loop) + str(i)
        playerInfo[index] = [name, country, goals]
        if goals == 0:
            end = True

    # Break out of loop when players on the list have scored 0 goals
    if end == True:
        break

    # Navigate to the next page
    button = driver.find_element(By.XPATH, buttons['Next Page'])
    driver.execute_script("arguments[0].click();", button)

    time.sleep(2)

# Save data into a dataframe
df = pd.DataFrame.from_dict(playerInfo, orient='index', columns=['Name', 'Country', 'Goals'])

# Close the driver
driver.quit()

# Save raw data
df.to_excel('Raw.xlsx')
