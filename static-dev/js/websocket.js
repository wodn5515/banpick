draftSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data['message'].split('|');
    const msgType = message[0];
    const msgData = message[1]
    if(msgType=='timer'){
        draft.timer = Number(msgData);
    }
    if(msgType=='draftrefresh'){
        draft.draftRefresh();
    }
    if(msgType=='championsrefresh'){
        draft.championsRefresh();
    }
    if(msgType=='championselect'){
        const order = msgData.split(',')[0]
        const no = msgData.split(',')[1]
        document.querySelector('.od_' + order + ' .sp').style.backgroundImage = 'url(/assets/img/champion82.png)';
        document.querySelector('.od_' + order + ' .sp').style.backgroundPosition = '0px -' + String(Number(no) * 82) + 'px';
    }
};