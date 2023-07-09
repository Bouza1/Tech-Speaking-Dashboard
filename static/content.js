document.addEventListener("DOMContentLoaded", function(){
    getNewArticles();
    console.log("Working")
})
  

//======================== Add Article ========================
let addArticleBtn = document.getElementById('addNewArticle')
addArticleBtn.addEventListener('click', function(){
  sendNewArticle2Server(addNewArticle())
})

function sendNewArticle2Server(article){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
    if(xhttp.status == 200 && xhttp.readyState == 4 ) {
        content = JSON.parse(xhttp.response);
        alert(content['message'])
        clearAddArticleInputs()
        }
    };
    xhttp.open("PUT", "/api/add_article", true);
    let articleObj = JSON.stringify({"article":article})
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(articleObj);
  }
  
function addNewArticle(){
    let title = document.getElementById('headlineInp')
    let content = formatArticleContent()
    let image = document.getElementById('imageInp')
    let articleObj = {"title":title.value, "content":content, "imagelink":image.value}
    return articleObj
}

function formatArticleContent(){
    let article = document.getElementById('articleInp')
    console.log(article.value)
    let preContent = article.value.split("\n")
    let content= []
    for(let i = 0; i < preContent.length; i++){
        if(preContent[i] !== ""){
            content.push(preContent[i])
        }
    }
    return content
}

let addArticleTextArea = document.getElementById('articleInp')
addArticleTextArea.addEventListener('paste', handlePaste);

function handlePaste(e) {
    var clipboardData, pastedData;
    e.stopPropagation();
    e.preventDefault();
    clipboardData = e.clipboardData || window.clipboardData;
    pastedData = clipboardData.getData('Text');
    let addArticleTextArea = document.getElementById('articleInp')
    addArticleTextArea.value = pastedData
    textAreaAdjust('articleInp')
}

function clearAddArticleInputs(){
    let title = document.getElementById('headlineInp')
    let article = document.getElementById('articleInp')
    let image = document.getElementById('imageInp')
    title.value = ""
    title.innerText = ""
    article.value = ""
    article.innerText = ""
    image.value = ""
    image.innerText = ""
    textAreaAdjust('articleInp')
}

function textAreaAdjust(element) {
    let textArea = document.getElementById(element)
    textArea.style.height = "1px";
    textArea.style.height = (textArea.scrollHeight)+"px";
}

//======================== New Potential Future Articles ========================
function getNewArticles(){
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if(xhttp.status == 200 && xhttp.readyState == 4 ) {
          content = JSON.parse(xhttp.response);
          fillContentTable(content)
        }
    }
    xhttp.open("GET", "/api/get_new_articles", true);
    xhttp.send();
}

function fillContentTable(articles){
    for(let i=0; i<articles.length; i++){
        let article = articles[i];
        let tableBody = document.getElementById('articleTBody');
        let row = document.createElement('tr');
    
        let scoreCell = document.createElement('td');
        scoreCell.innerText = article['score'];
        
        let titleCell = document.createElement('td');
        titleCell.innerText = article['title'];
        titleCell.value = article['link'];
        titleCell.setAttribute('class', "new-article-link");
        titleCell.addEventListener('click', function(){
            openInSameWindow(this.value);
        })
        row.appendChild(scoreCell);
        row.appendChild(titleCell);
        tableBody.appendChild(row);
        }
  }

function openInSameWindow(URL){
    window.open(URL, '_blank');
}
