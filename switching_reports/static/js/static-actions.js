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

    $("div[id^='Коммутация VAR']").each(function() { $(this).on("click", function(e)
        {
            if($(e.target).is('a')) {}
            else {
                var descs = this.getElementsByClassName("report-desc-block");
                if(flag == 0 && this.children.length > 1){
                    for (var i = 0; i < descs.length; i++){
                        descs[i].style.display = "block";
                    }
                    flag = 1;
                    this.style.background = "white";
                }
                  else {
                    for (var i = 0; i < descs.length; i++){
                        descs[i].style.display = "none";
                    }
                    flag = 0;
                  if(this.children.length <= 1){
                    this.style.background = 'grey';
                  }
                  else{
                    this.style.background = "#fcca03";
                  }
                }
            }
        })
    });
}

function expandOrCollapseMP(){
    var flag = 0;

    $("div[id^='Коммутация Матч Премьер']").each(function() { $(this).on("click", function(e)
        {
                if($(e.target).is('a')) {}
                else {
                    var descs = this.getElementsByClassName("report-desc-block");
                    if(flag == 0 && this.children.length > 1){
                        for (var i = 0; i < descs.length; i++){
                            descs[i].style.display = "block";
                        }
                        flag = 1;
                        this.style.background = "white";
                    }
                      else {
                        for (var i = 0; i < descs.length; i++){
                            descs[i].style.display = "none";
                        }
                        flag = 0;
                      if(this.children.length <= 1){
                        this.style.background = 'grey';
                      }
                      else{
                        this.style.background = "#fcca03";
                      }
                    }
            }
        })
    });
}

function expandOrCollapseRec(){
    var flag = 0;

    $("div[id^='Запись трансляции']").each(function() { $(this).on("click", function(e)
        {
            if($(e.target).is('a')) {}
            else {
                var descs = this.getElementsByClassName("report-desc-block");
                if(flag == 0 && this.children.length > 1){
                    for (var i = 0; i < descs.length; i++){
                        descs[i].style.display = "block";
                    }
                    flag = 1;
                    this.style.background = "white";
                }
                  else {
                    for (var i = 0; i < descs.length; i++){
                        descs[i].style.display = "none";
                    }
                    flag = 0;
                  if(this.children.length <= 1){
                    this.style.background = 'grey';
                  }
                  else{
                    this.style.background = "#fcca03";
                  }
                }
            }
        })
    });
}

function expandOrCollapseOst(){
    var flag = 0;

    $("div[id^='Коммутация Останкино']").each(function() { $(this).on("click", function(e)
        {
            if($(e.target).is('a')) {}
            else {
                var descs = this.getElementsByClassName("report-desc-block");
                if(flag == 0 && this.children.length > 1){
                    for (var i = 0; i < descs.length; i++){
                        descs[i].style.display = "block";
                    }
                    flag = 1;
                    this.style.background = "white";
                }
                  else {
                    for (var i = 0; i < descs.length; i++){
                        descs[i].style.display = "none";
                    }
                    flag = 0;
                  if(this.children.length <= 1){
                    this.style.background = 'grey';
                  }
                  else{
                    this.style.background = "#fcca03";
                  }
                }
            }
        })
    });
}

var flag = 0;
function read(){
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

