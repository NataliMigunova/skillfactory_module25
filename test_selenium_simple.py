import time
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get('https://google.com')

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Find the field for search text input:
    search_input = driver.find_element_by_name('q')

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('first test')

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Click Search:
    search_button = driver.find_element_by_name('btnK')
    search_button.click()

    time.sleep(10)  # just for demo purposes, do NOT repeat it on real projects!

    # Make the screenshot of browser window:
    driver.save_screenshot('result.png')
