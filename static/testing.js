document.addEventListener("DOMContentLoaded", function() {
    get_test_results_from_server()
    get_latest_test_dates_from_server()
})

function refresh_elements(){
    clear_table('t-body-results')
    get_test_results_from_server();
    get_latest_test_dates_from_server();
}
// ============================ Latest Tests Table ============================
function get_test_results_from_server() {
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if(xhttp.status == 200 && xhttp.readyState == 4 ) {
            results = JSON.parse(xhttp.response);
            for(let i = 0; i < results.length; i++){
                populate_latest_tests_table(results[i])
            }
        }
    }
    xhttp.open("GET", "/api/get_testing_results", true);
    xhttp.send();
}

function populate_latest_tests_table(test_obj){
    let table = document.getElementById('t-body-results')
    let row = document.createElement('tr')
    let id_cell = document.createElement('td')
    let date_cell = document.createElement('td')
    let scenario_cell = document.createElement('td')
    let result_cell = document.createElement('td')
    id_cell.innerText = test_obj['test_id']
    date_cell.innerText = test_obj['date']
    scenario_cell.innerText = test_obj['scenario']
    result_cell.innerText = test_obj['status']
    row.appendChild(id_cell)
    row.appendChild(date_cell)
    row.appendChild(scenario_cell)
    row.appendChild(result_cell)
    table.appendChild(row)
}

function clear_table(element){
    let table_2_clear = document.getElementById(element)
    table_2_clear.innerHTML = ""
}

// ============================ Test Date Table ============================
function get_latest_test_dates_from_server(){
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if(xhttp.status == 200 && xhttp.readyState == 4 ) {
            results = JSON.parse(xhttp.response);
            insert_latest_test_dates(results)
        }
    }
    xhttp.open("GET", "/api/get_test_dates", true);
    xhttp.send();
}

function insert_latest_test_dates(latest_dates_obj){
    let pages_date = document.getElementById('pages_date')
    let repair_date = document.getElementById('repair_date')
    let footer_date = document.getElementById('footer_date')
    let users_func_date = document.getElementById('users_func_date')
    pages_date.innerText = latest_dates_obj['pages']
    repair_date.innerText = latest_dates_obj['repair']
    footer_date.innerText = latest_dates_obj['footer']
    users_func_date.innerText = latest_dates_obj['users_funcs']
    change_date_color(pages_date)
    change_date_color(repair_date)
    change_date_color(footer_date)
    change_date_color(users_func_date)
}

function change_date_color(element){
    let expire_date = new Date()
    expire_date.setDate(expire_date.getDate() - 7);
    let test_date = new Date(element.innerText)
    if(test_date < expire_date){
        element.setAttribute('class', 'text-center')
        element.setAttribute('id', 'bad-result')
    } else {
        element.setAttribute('class', 'text-center')
        element.setAttribute('id', 'good-result')
    }
}

// ============================ Run Test ============================
let run_test_btn = document.getElementById('run_test_btn')
run_test_btn.addEventListener('click', function(){
    let test_obj = get_test_deets()
    console.log(test_obj)
    disable_test_btn()
    send_test_2_run_2_server(test_obj)
})


function get_test_deets(){
    let test_2_run = document.getElementById('test_2_run')
    let test_obj = {"Test":test_2_run.value}
    return test_obj
}


function send_test_2_run_2_server(test_obj){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
    if(xhttp.status == 200 && xhttp.readyState == 4 ) {
        content = JSON.parse(xhttp.response);
        show_alert(content['Alert'], content['Message']);
        enable_test_btn();
        refresh_elements();
        }
    };
    xhttp.open("PUT", "/api/run_test", true);
    let test = JSON.stringify(test_obj)
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(test);
}

function disable_test_btn(){
    let run_test_btn = document.getElementById('run_test_btn')
    run_test_btn.disabled = true;
}

function enable_test_btn(){
    let run_test_btn = document.getElementById('run_test_btn')
    run_test_btn.disabled = false;
}

function show_alert(type, text){
    let alert_box = document.getElementById('alert');
    let class_str = 'alert alert-dismissible fade show alert-' + type;
    alert_box.setAttribute('class', class_str);
    alert_box.setAttribute('role', 'alert');
    alert_box.innerText = text;
    let close_btn = document.createElement('button')
    close_btn.setAttribute('class', 'btn-close')
    close_btn.setAttribute('type', 'button')
    close_btn.addEventListener('click', function(){
        alert_box.style.display = "none"
    })
    alert_box.appendChild(close_btn)    
    alert_box.style.display = "block";
}