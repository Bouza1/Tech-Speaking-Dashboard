
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import Select
import json

def construct_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_site(driver):
    driver.get("https://techspeaking.s4820791.repl.co/repair")

def enter_name(driver, testcase):
    name_input = driver.find_element(By.ID, "name_inp")
    name_input.send_keys(testcase['name'])

def enter_contact(driver, testcase):
    contact_num_input = driver.find_element(By.ID, "contact_number_inp")
    contact_num_input.send_keys(testcase['number'])

def enter_email(driver, testcase):
    email_input = driver.find_element(By.ID, "email_address_inp")
    email_input.send_keys(testcase['email'])

def enter_dev_type(driver, testcase):
    dev_type_input = Select(driver.find_element(By.ID, "device_type_inp"))
    dev_type_input.select_by_value(testcase['device'])

def enter_dev_make(driver, testcase):
    dev_make_input = driver.find_element(By.ID, "make_inp")
    dev_make_input.send_keys(testcase['make'])

def enter_dev_model(driver, testcase):
    dev_model_input = driver.find_element(By.ID, "model_inp")
    dev_model_input.send_keys(testcase['model'])

def enter_dev_serial(driver, testcase):
    dev_serial_input = driver.find_element(By.ID, "sn_inp")
    dev_serial_input.send_keys(testcase['serial'])

def enter_issues(driver, testcase):
    issues_input = driver.find_element(By.ID, "issues_inp")
    issues_input.send_keys(testcase['issues'])

def enter_contact_prefs(driver, testcase):
    contact_prefs_input = driver.find_element(By.ID, testcase['prefs'])
    contact_prefs_input.click()

def submit_repair_form(driver):
    submit_btn = driver.find_element(By.ID, "submit-btn")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)
    submit_btn.click();

def click_alert(driver, testcase):
    alert = driver.find_element(By.ID, "alert_text")
    if testcase['expected_alert'] in alert.text:
        return {"scenario id":testcase['id'], "scenario":testcase['scenario'], "status":"Passed"}
    else:
        return {"id":testcase['id'], "scenario":testcase['scenario'], "status":"Failed"}

def full_script(driver, testcase):
    load_site(driver)
    time.sleep(2)
    enter_name(driver, testcase)
    enter_contact(driver, testcase)
    enter_email(driver, testcase)
    enter_dev_type(driver, testcase)
    enter_dev_make(driver, testcase)
    enter_dev_model(driver, testcase)
    enter_dev_serial(driver, testcase)
    enter_issues(driver, testcase)
    enter_contact_prefs(driver, testcase)
    time.sleep(2)
    submit_repair_form(driver)
    time.sleep(2)
    result = click_alert(driver, testcase)
    return result

def loop_test_cases(testcase):
    driver = construct_driver()
    results = []
    failed_results=[]
    for case in testcase:
        result = full_script(driver, case)
        if result['status'] == "Failed":
            failed_results.append(result)
        else:
            results.append(result)
    return {"passed":results,"failed":failed_results}

def append_results_2_json(results, file):
    with open(file, 'w') as json_file:
        json.dump(results, json_file, indent=4,  separators=(',',': '))