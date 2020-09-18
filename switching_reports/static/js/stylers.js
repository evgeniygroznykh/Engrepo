function styleReportDescriptions (){
    $("div.report-desc-block:contains('Без замечаний')").css("background", "linear-gradient(to bottom, #339933 0%, #99ff33 100%)");
    $("div.report-desc-block:not(:contains('Без замечаний'))").css("background", "linear-gradient(to bottom, #ff0000 0%, #ff99cc 100%)");
}

function styleWorkTypeDivs (){
    if(document.getElementById("Коммутация VAR").children.length <= 1){
        document.getElementById("Коммутация VAR").style.background = 'grey';
    }

    if(document.getElementById("Коммутация Матч Премьер").children.length <= 1){
        document.getElementById("Коммутация Матч Премьер").style.background = 'grey';
    }

    if(document.getElementById("Запись трансляции").children.length <= 1){
        document.getElementById("Запись трансляции").style.background = 'grey';
    }

    if(document.getElementById("Коммутация Останкино").children.length <= 1){
        document.getElementById("Коммутация Останкино").style.background = 'grey';
    }
}