from utils.testing.links import loop_all_links, loop_all_footer_links
from utils.testing.repair_form import loop_test_cases
from utils.testing.repair_form_testcases import all_cases
from utils.testing.links_testcases import footer_links
import json
import datetime

from utils.testing.user_functions import user_func_tests

def run_this_test(test, json_url):
    result = ""
    if test == "repair":
        result = loop_test_cases(all_cases)
        decision_maker(result, json_url, "Repair Form", test)
    elif test == "pages":
        result = loop_all_links()
        decision_maker(result, json_url, "Pages", test)
    elif test =="footer":
        result = loop_all_footer_links(footer_links)
        decision_maker(result, json_url, "Footer Funcs", test)
    elif test =="user_funcs":
        result = user_func_tests()
    return result

def format_obj_4_latest_test_log(test_results, scenario, json_url):
    new_id = return_new_id(json_url)
    date = generate_date()
    obj = {"test_id":new_id, "date":date, "scenario":scenario}
    if test_results['failed'] == []:
        obj['status'] = "Passed"
    else:
        obj['status'] = "Failed"
    return obj
        
def generate_date():
    current_day = datetime.date.today()
    formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
    return str(formatted_date)

def return_new_id(json_url):
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
        results_in_file = full_json_object['results']
        test_id = len(results_in_file) + 1
    return test_id

def append_result_2_json(result_object, json_url):
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
        results_in_file = full_json_object['results']
        results_in_file.append(result_object)
    with open(json_url, 'w') as json_file:
        json.dump(full_json_object, json_file, indent=4,  separators=(',',': '))

def decision_maker(result, json_url, scenario, test):
    fomatted_result = format_obj_4_latest_test_log(result, scenario, json_url)
    append_result_2_json(fomatted_result, json_url)
    update_last_ran(json_url, test, fomatted_result['date'])
    if result['failed'] != []:
       failed_tests_output(result['failed'], json_url)

def failed_tests_output(results, json_url):
    fail_obj = {'id':return_new_id(json_url)-1, 'tests':[]} # has to be minus one because the object is already appended so just need the len of latest_results and not the +1 used in id
    for fail in results:
        fail_obj['tests'].append(fail)
    print(fail_obj)

def update_last_ran(json_url, test, test_date):
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
        results_in_file = full_json_object['last_ran']
        results_in_file[test] = test_date
    with open(json_url, 'w') as json_file:
        json.dump(full_json_object, json_file, indent=4,  separators=(',',': '))


