document.addEventListener("DOMContentLoaded", function(){
    getNewArticles();
    getNewMemes();
    console.log("Working")
})

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

function getNewMemes(){
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if(xhttp.status == 200 && xhttp.readyState == 4 ) {
            content = JSON.parse(xhttp.response);
            fillMemeTable(content)
        }
    }
    xhttp.open("GET", "/api/get_new_memes", true);
    xhttp.send();
}

function fillMemeTable(memes){
    let meme_container = document.getElementById('meme-container');
    for(let i=0; i<memes.length; i++){
        let meme = memes[i];
        let row = document.createElement('div');
        row.setAttribute('class', 'row border-bottom')

        let imgDiv = document.createElement('div');
        imgDiv.setAttribute('class', 'col-6')
        let img = document.createElement('img');
        img.setAttribute('class', 'img-fluid')
        img.src = meme['image']
        imgDiv.appendChild(img)

        let captionDiv  = document.createElement('div');
        captionDiv.setAttribute('class', 'col-4')
        captionDiv.innerText = meme['title'];

        let scoreDiv  = document.createElement('div');
        scoreDiv.setAttribute('class', 'col-2')
        scoreDiv.innerText = meme['score'];

        row.appendChild(scoreDiv);
        row.appendChild(captionDiv);
        row.appendChild(imgDiv)
        meme_container.appendChild(row);
    }
}
