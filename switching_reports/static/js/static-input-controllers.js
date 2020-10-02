function selectMainSource(Button) {
    var input = document.getElementById('switchingSource');
    input.value = Button.textContent;
    document.querySelector(".main-srcs-bg-modal").style.display = 'none';
    document.querySelector(".main-var-srcs-bg-modal").style.display = 'none';
}


function selectMainDest(Button) {
    var input = document.getElementById('switchingDestination');
    input.value = Button.textContent;
    document.querySelector(".main-dests-bg-modal").style.display = 'none';
    document.querySelector(".main-var-dests-bg-modal").style.display = 'none';
}


function selectResSource(Button) {
    var input = document.getElementById('reserveSwitchingSource');
    input.value = Button.textContent;
    document.querySelector(".res-srcs-bg-modal").style.display = 'none';
    document.querySelector(".res-var-srcs-bg-modal").style.display = 'none';
}


function selectResDest(Button) {
    var input = document.getElementById('reserveSwitchingDestination');
    input.value = Button.textContent;
    document.querySelector(".res-dests-bg-modal").style.display = 'none';
    document.querySelector(".res-var-dests-bg-modal").style.display = 'none';
}

function chooseWorkType(Button) {
    var select = document.getElementById('switchingReportWorkType');
    select.value = Button.textContent;
}

function chooseCustomer(Button) {
    var select = document.getElementById('switchingCustomer');
    select.value = Button.textContent;
}

function addText(Button) {
    var input = document.getElementById('reportTags');
    input.value = input.value + Button.textContent + ' ';
}

