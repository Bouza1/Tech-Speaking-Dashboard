document.addEventListener("DOMContentLoaded", function() {
    getNewsFromServer();
})

function getNewsFromServer() {
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if(xhttp.status == 200 && xhttp.readyState == 4 ) {
            news = JSON.parse(xhttp.response);
            for(let i = 0; i < 3; i++){
              createArticleCard(news[i])
              console.log(news[i])
            }
        }
    }
    xhttp.open("GET", "/api/get_live_articles", true);
    xhttp.send();
}

function createArticleCard(article){
    let row = document.getElementById('content')
    let col = document.createElement("div")
    col.setAttribute('class', 'col-lg-4 col-md-6 col-12')

    let cardholder = document.createElement("div")
    cardholder.setAttribute('class', 'card shadow mb-3 bg-white rounded')
    cardholder.setAttribute('id', 'card')

    let topContainer = document.createElement("div")
    topContainer.setAttribute('class', 'container')
    topContainer.setAttribute('id', 'top-container')
    
    let cardbody = document.createElement("div")
    cardbody.setAttribute('class', 'card-body align-items-center')

    let image = document.createElement("img")
    image.src = article['imagelink']
    image.setAttribute('class', 'card-img-top text-center')
    image.setAttribute('id', 'card-image')
    
    
    let title = document.createElement("H5")
    title.setAttribute('class', 'card-title')
    title.innerText = article['title']

    let content = document.createElement("p")
    content.setAttribute('class', 'card-text')
    content.setAttribute('id', 'card-text')
    content.innerText = article['content']

    let buttonContainer = document.createElement('div')
    buttonContainer.setAttribute('class', 'container')
    
    let openButton = document.createElement("button")
    openButton.setAttribute('class', 'btn btn-primary card-btn')
    openButton.setAttribute('id', article['id'])
    openButton.innerText = "View"
    openButton.addEventListener('click', function () {
        openArticlePage(this.id)
        console.log(this.id)
    })
    
    cardbody.appendChild(image)
    cardbody.appendChild(title)
    cardbody.appendChild(content)
    buttonContainer.appendChild(openButton)
    topContainer.appendChild(cardbody)
    
    cardholder.appendChild(topContainer)
    cardholder.appendChild(buttonContainer)
    
    
    col.appendChild(cardholder)
    row.appendChild(col)
}

function openArticlePage(id){
  window.open("https://techspeaking.s4820791.repl.co/news/article/" + id, "_self")
}

function destroy_article_cards(){
    let row = document.getElementById('content');
    row.innerHTML = "";
}

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
        clearAddArticleInputs();
        destroy_article_cards();
        getNewsFromServer();
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
