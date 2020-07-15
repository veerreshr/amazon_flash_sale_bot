from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from multiprocessing import Process

options = Options()
options.page_load_strategy = 'eager'

login_url = 'https://amzn.to/38X1LHr'


def purchase(username, password, item_url, cvv):
    address_xpath = '//*[@id="address-book-entry-0"]/div[2]/span/a'
    # if its your second address in your amazon account use this address xpath='//*[@id="address-book-entry-1"]/div[2]/span/a'
    # in simple put (n-1) value in place of //*[@id="address-book-entry-___________________"]/div[2]/span/a where n is address number you want to deliver from your amazon account
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

   # for logging into amazon

    driver.get(login_url)
    driver.find_element_by_xpath(
        '//*[@id="ap_email"]').send_keys(username + Keys.RETURN)
    driver.find_element_by_xpath(
        '//*[@id="ap_password"]').send_keys(password + Keys.RETURN)

  # end of login code

  # for getting into our product page
    driver.get(item_url)

  # refresh till we find buy now button in amazon
    while not driver.find_elements_by_xpath('//*[@id="buy-now-button"]'):
        driver.refresh()

   # once the button is activated ,click the buy now button
    driver.find_element_by_xpath(
        '//*[@id="buy-now-button"]').click()

    # wait until select address button loads, once after loading click that button
    delivery_to_this = wait.until(
        presence_of_element_located((By.XPATH, address_xpath)))
    delivery_to_this.click()

    # wait till we get checkout page loaded , once after loading enter the cvv code and press enter
    wait_for_checkout_page = wait.until(
        presence_of_element_located((By.XPATH, '//*[@id="checkoutDisplayPage"]')))
    driver.find_element_by_name(
        'addCreditCardVerificationNumber0').send_keys(cvv+Keys.RETURN)

    # at the end click review oreder and we will be redirected to bank page for entering otp
    review_order = wait.until(
        presence_of_element_located((By.NAME, 'placeYourOrder1')))
    review_order.click()


if __name__ == '__main__':
    p1 = Process(target=purchase, args=[
                 "test@test.com", "test_password", "product_link", "cvv"])
    p1.start()
    p2 = Process(target=purchase, args=[
                 "test@test.com", "test_password", "product_link", "cvv"])
    p2.start()
    p1.join()
    p2.join()
