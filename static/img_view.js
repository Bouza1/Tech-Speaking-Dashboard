document.addEventListener("DOMContentLoaded", function() {
    change_buggy_jinja_variable('bug-jinja-title');
})

function change_buggy_jinja_variable(element){
    let buggy_title = document.getElementById(element)
    let not_buggy_title = buggy_title.innerText.split('"').join('')
    buggy_title.innerText = not_buggy_title
}

let screenshot_btn = document.getElementById('screenshot_btn')
screenshot_btn.addEventListener('click', function(){
    console.log("working");
    let url = window.location.href
    let id = document.getElementById('hidden_id')
    save_screenshot(url, id.innerText)
})

function save_screenshot(url, id){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(xhttp.status == 200 && xhttp.readyState == 4 ) {
            content = JSON.parse(xhttp.response);
            alert(content['message'])
        };
    }    
    let url_obj = JSON.stringify({"url":url, "id":id})
    console.log(url_obj)
    xhttp.open("PUT", "/api/display_image/screenshot", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(url_obj);
}

function reload_page_afer_save(){
    
}