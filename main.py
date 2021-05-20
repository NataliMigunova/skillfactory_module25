from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get('https://google.com')
