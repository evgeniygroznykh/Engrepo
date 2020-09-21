function styleReportDescriptions (){
    $("div.report-desc-block:contains('Без замечаний')").css("background", "linear-gradient(to bottom, #339933 0%, #99ff33 100%)");
    $("div.report-desc-block:not(:contains('Без замечаний'))").css("background", "linear-gradient(to bottom, #ff0000 0%, #ff99cc 100%)");
}

function styleWorkTypeDivs (){
    $("div[id^='Коммутация VAR']").each(function() {
            if (this.children.length <= 1){
                this.style.background = 'grey';
            }
            else {
                this.style.background = '#fcca03';
            }
        });
        $("div[id^='Коммутация Матч Премьер']").each(function() {
            if (this.children.length <= 1){
                this.style.background = 'grey';
            }
            else {
                this.style.background = '#fcca03';
            }
        });
            $("div[id^='Запись трансляции']").each(function() {
            if (this.children.length <= 1){
                this.style.background = 'grey';
            }
            else {
                this.style.background = '#fcca03';
            }
        });
            $("div[id^='Коммутация Останкино']").each(function() {
            if (this.children.length <= 1){
                this.style.background = 'grey';
            }
            else {
                this.style.background = '#fcca03';
            }
        });
}