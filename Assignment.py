
from selenium import webdriver
from selenium.webdriver.common import alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# credential on lambdatest
USERNAME = "nannawareakshay990"
ACCESS_KEY = "LT_ZSQOSTppEA04RK1Jd4utRkC8sKmT4Ya8VKMcpZuuuSuPVXU"

LT_GRID_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"

chrome_options = Options()
chrome_options.browser_version = "119.0"
chrome_options.platform_name = "Windows 10"
chrome_options.set_capability("resolution", "1920x1080")
chrome_options.set_capability("name", "Flipkart iPhone Cart Test")
chrome_options.set_capability("build", "LambdaTest-Selenium-Python")
chrome_options.set_capability("network", True)
chrome_options.set_capability("visual", True)
chrome_options.set_capability("video", True)


driver = webdriver.Remote(
    command_executor=LT_GRID_URL,
    options=chrome_options
)

from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode

# driver = webdriver.Chrome(options=chrome_options)
try:
    # Open Flipkart
    driver.get("https://flipkart.com")
    time.sleep(5)

    # Search for iphone 16
    search_box = driver.find_element(By.XPATH, "//*[contains(@placeholder,'Search for Products, Brands and More')]")
    search_box.send_keys("iphone 16")
    search_box.send_keys(Keys.RETURN)

    # wait for loading the result of ipone
    time.sleep(3)

    # click on the first iphone displayed
    first_product = driver.find_element(By.XPATH, "(//a[contains(@href, '/apple-iphone')])[1]")
    first_product.click()

    #this is opening in another tab so below we are navigating to the new tab which has created after clicking on the first product

    # switch to new tab
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)

    wait = WebDriverWait(driver, 10)


    # Click on "Add to Cart"
    add_to_cart_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Add to cart')]")
    assert add_to_cart_btn.is_displayed(), "Add to Cart button is not visible"
    add_to_cart_btn.click()

    cart_price = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='container']/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[2]/span/div/div/div[2]/span")))
    print("cart price is: ", cart_price.text)

    cart_items = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(text(),'iPhone')]")))

    # checking for if iphone is added in the cart or not
    assert len(cart_items) > 0, "iphone is NOT added in the cart"

    print("IPHONE is added in the cart successfully")
    driver.execute_script("lambda-status=passed")
except Exception as e:
    print("failure in: ", e)
    driver.execute_script("lambda-status=failed")
finally:
    driver.quit()