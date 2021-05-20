import time
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="./chromedriver")


def test_petfriends(web_browser):
    web_browser.get("https://petfriends1.herokuapp.com/")
    time.sleep(2)

    btn_newuser = driver.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # click existing user button
    btn_exist_acc = driver.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # add email
    field_email = driver.find_element_by_id("email")
    field_email.clear()
    field_email.send_keys("natali_test@gmail.com")

    # add password
    field_pass = driver.find_element_by_id("pass")
    field_pass.clear()
    field_pass.send_keys("qwerty1234")

    # click submit button
    btn_submit = driver.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!
    if driver.current_url == 'https://petfriends1.herokuapp.com/all_pets':
        # Make the screenshot of browser window:
        driver.save_screenshot('result_petfriends.png')
    else:
        raise Exception("login error")