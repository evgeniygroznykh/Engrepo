function setButtonClickActions () {
    document.getElementById('main-sources-button').addEventListener('click', function() {
        document.querySelector('.main-srcs-bg-modal').style.display = 'flex';
    });
    document.getElementById('main-dests-button').addEventListener('click', function() {
        document.querySelector('.main-dests-bg-modal').style.display = 'flex';
    });

    document.querySelector('.main-srcs-close-btn').addEventListener('click', function() {
        document.querySelector(".main-srcs-bg-modal").style.display = 'none';
    });

    document.querySelector('.main-dests-close-btn').addEventListener('click', function() {
        document.querySelector(".main-dests-bg-modal").style.display = 'none';
    });
    document.getElementById('res-sources-button').addEventListener('click', function() {
        document.querySelector('.res-srcs-bg-modal').style.display = 'flex';
    });
    document.getElementById('res-dests-button').addEventListener('click', function() {
        document.querySelector('.res-dests-bg-modal').style.display = 'flex';
    });

    document.querySelector('.res-srcs-close-btn').addEventListener('click', function() {
        document.querySelector(".res-srcs-bg-modal").style.display = 'none';
    });

    document.querySelector('.res-dests-close-btn').addEventListener('click', function() {
        document.querySelector(".res-dests-bg-modal").style.display = 'none';
    });
}

function expandOrCollapseVar(){
    var flag = 0;
    document.getElementById("Коммутация VAR").addEventListener("click", function()
    {
        var descs = document.getElementById("Коммутация VAR").getElementsByClassName("report-desc-block");
        if(flag == 0){
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "block";
            }
            flag = 1;
        }
          else {
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "none";
            }
            flag = 0;
        }
    });
}

function expandOrCollapseMP(){
    var flag = 0;
    document.getElementById("Коммутация Матч Премьер").addEventListener("click", function()
    {
        var descs = document.getElementById("Коммутация Матч Премьер").getElementsByClassName('report-desc-block');
        if(flag == 0){
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "block";
            }
            flag = 1;
        }
          else {
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "none";
            }
            flag = 0;
        }
    });
}

function expandOrCollapseRec(){
    var flag = 0;
    document.getElementById("Запись трансляции").addEventListener("click", function()
    {
        var descs = document.getElementById("Запись трансляции").getElementsByClassName('report-desc-block');
        if(flag == 0){
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "block";
            }
            flag = 1;
        }
          else {
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "none";
            }
            flag = 0;
        }
    });
}

function expandOrCollapseOst(){
    var flag = 0;
    document.getElementById("Коммутация Останкино").addEventListener("click", function()
    {
        var descs = document.getElementById("Коммутация Останкино").getElementsByClassName('report-desc-block');
        if(flag == 0){
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "block";
            }
            flag = 1;
        }
          else {
            for (var i = 0; i < descs.length; i++){
                descs[i].style.display = "none";
            }
            flag = 0;
        }
    });
}

function read(){
    var flag = 0;
    if(flag == 0){
        document.getElementById("more").style.display="inline";
        document.getElementById("more_link").innerHTML="Скрыть";
        flag = 1;
    }
    else{
        document.getElementById("more").style.display="none";
        document.getElementById("more_link").innerHTML="Читать подробнее..";
        flag = 0;
    }
}

