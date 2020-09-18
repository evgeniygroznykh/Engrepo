function styleReportDescriptions (){
    $("div.report-desc-block:contains('Без замечаний')").css("background", "linear-gradient(to bottom, #339933 0%, #99ff33 100%)");
    $("div.report-desc-block:not(:contains('Без замечаний'))").css("background", "linear-gradient(to bottom, #ff0000 0%, #ff99cc 100%)");
}