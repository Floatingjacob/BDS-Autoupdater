# BDS-Autoupdater © 2024 by Jacob Miller is licensed under CC BY-NC-SA 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from io import BytesIO
import time
import subprocess
import sys
def download_and_extract_to_directory(url, button_aria_label):

    try:
        subprocess.check_call(["clean.bat"])
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        download_directory = os.path.join(script_directory, "updatetemp")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("prefs", {"download.default_directory": download_directory})
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        button = driver.find_element(By.XPATH, f"//*[@aria-label='{button_aria_label}']")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@aria-label='{button_aria_label}']")))
        driver.execute_script("arguments[0].click();", button)

    
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '.zip')]")))
        time.sleep(10)
        driver.quit()
        subprocess.run(["update.bat"])
        subprocess.check_call(["bedrock_server.exe"])
    except Exception as e:
        print(f"There was an error")
    
webpage_url = "https://www.minecraft.net/en-us/download/server/bedrock"
button_aria_label_to_click = "Download Minecraft Dedicated Server software for Windows"
download_and_extract_to_directory(webpage_url, button_aria_label_to_click)
