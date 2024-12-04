function addlog(log){
    log = log || '';
    teminal_log = localStorage.getItem('terminal_log') || '';
    teminal_log += log + '\n';
    localStorage.setItem('terminal_log', teminal_log);
    displaylog();
}

function clearLogs(){
    localStorage.setItem('terminal_log','');
    displaylog();
}

function displaylog(){
    const logBar = document.getElementById('scrapystate');
    logBar.value = localStorage.getItem('terminal_log');
    scrapystate.scrollTo(0,10000);
}