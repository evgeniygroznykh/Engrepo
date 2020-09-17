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

