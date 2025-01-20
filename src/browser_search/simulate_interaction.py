import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def simulate_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay)/2)

def simulate_scroll(driver):
    scroll_pause_time = random.uniform(1, 3)/2  # Random pause for scrolling
    scroll_height = random.randint(200, 500)  # Random scroll distance
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    time.sleep(scroll_pause_time)


def simulate_interaction(driver, xpath_list):

    # Scroll multiple times
    for _ in range(random.randint(1, 4)):
        simulate_scroll(driver)

    # Find the element to interact with
    element_xpath = random.choice(xpath_list)
    element = driver.find_element(By.XPATH, element_xpath)

    # Move mouse to the element with random delay
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

    # Action click
    simulate_delay()
    element.click()
    simulate_delay()