function reverseCoin(number){
	q=document.getElementById("imgObverse"+number);
	w=document.getElementById("imgReverse"+number);
	e=q.style.display;
	q.style.display=w.style.display;
	w.style.display=e;
    /*e=q.width;
    q.width=w.width;
    w.width=e;
    e=q.height;
    q.height=w.height;
    w.height=e;*/
	}

function reverseCoins(){
q=document.getElementsByName("imgObverse");
w=document.getElementsByName("imgReverse");
    for (a=0; a<q.length;a++){
        e=q[a].style.display;
        q[a].style.display=w[a].style.display;
        w[a].style.display=e;
    }
}

function filterCoins(){
    q=document.getElementById("text");
    q.innerHTML="";
    params="?country="+document.getElementById("filter_country").value+"&seria="+document.getElementById("filter_seria").value+"&metal="+document.getElementById("filter_metal").value+"&denomination="+document.getElementById("filter_denomination").value+"&coinage="+document.getElementById("filter_coinage").value;
    showAJAXinTip("/katalog/coins"+params,"text")
}

function orderCoins(){
    q=document.getElementById("text");
    q.innerHTML="";
    params="?order1_name="+document.getElementById("order1_name").value+
            "&order1_how="+document.getElementById("order1_how").value+
            "&order2_name="+document.getElementById("order2_name").value+
            "&order2_how="+document.getElementById("order2_how").value;
    showAJAXinTip("/katalog/coins"+params,"text")
}

function convertJE(inyear){
sum=0
mult=1
for (var q=0;q<inyear.length;q++){
    switch (inyear[q]){
        case 'א':
            sum+=1*mult;
            break;
        case 'ב':
            sum+=2*mult;
            break;
        case 'ג':
            sum+=3*mult;
            break;
        case 'ד':
            sum+=4*mult;
            break;
        case 'ה':
            sum+=5*mult;
            break;
        case 'ו':
            sum+=6*mult;
            break;
        case 'ז':
            sum+=7*mult;
            break;
        case 'ח':
            sum+=8*mult;
            break;
        case 'ט':
            sum+=9*mult;
            break;
        case 'י':
            sum+=10*mult;
            break;
        case 'כ':
            sum+=20*mult;
            break;
        case 'ל':
            sum+=30*mult;
            break;
        case 'מ':
            sum+=40*mult;
            break;
        case 'נ':
            sum+=50*mult;
            break;
        case 'ס':
            sum+=60*mult;
            break;
        case 'ע':
            sum+=70*mult;
            break;
        case 'פ':
            sum+=80*mult;
            break;
        case 'צ':
            sum+=90*mult;
            break;
        case 'ק':
            sum+=100*mult;
            break;
        case 'ר':
            sum+=200*mult;
            break;
        case 'ש':
            sum+=300*mult;
            break;
        case 'ת':
            sum+=400*mult;
            break;
        case '׳':
            mult=1000;
            break;
}
}
if (mult==1 || (mult==1000 && inyear[inyear.length-1]=='׳'))
    sum+=5000;
return sum-3760;
}

function convertAH(inyear){
        var myear=inyear*1.0;
        cyear=myear*0.970224044+621.574981435;
        var     fday= cyear-Math.floor(cyear);
        cyear -= fday;
        if (cyear <1) {cyear -=1;}
        return cyear;
}

function convertBE(inyear){
        cyear=inyear*1.0-543;
        return cyear;
}

function convertBENG(inyear){
        cyear=inyear*1.0+593;
        return cyear;
}

function convertMO(inyear){
        cyear=inyear*1.0+1910;
        return cyear;
}

function convertVS(inyear){
        cyear=inyear*1.0-57;
        return cyear;
}

function tryToConvertDate(){
    q=document.getElementById('hidenInputDate').value;
    //Конвертируем q
    if (q=="" || q=="&nbsp;"){
        document.getElementById('outputDate').value=q;
        return;
    }
    switch (document.getElementById("keyboardType").value){
    case "1":
        q=convertAH(q);
        break;
    case "2":       
        q=convertJE(q);
        break;
    case "4":       
        q=convertBE(q);
        break;
    case "5":       
        q=convertBENG(q);
        break;
    case "6":       
        q=convertMO(q);
        break;
    case "7":       
        q=convertVS(q);
        break;
    }
    document.getElementById('outputDate').value=q;
}

function clearLastInputDate(){
q=document.getElementById('inputDate').value;
q=q.substr(0,q.length-1);
document.getElementById('inputDate').value=q;
q=document.getElementById('hidenInputDate').value;
q=q.substr(0,q.length-1);
document.getElementById('hidenInputDate').value=q;
tryToConvertDate();
}

function clearInputDate(){
document.getElementById('inputDate').value="";
document.getElementById('hidenInputDate').value="";
document.getElementById('outputDate').value="";
}

function enterNumberIntoInputDate(a){
document.getElementById('inputDate').value+=a;
document.getElementById('hidenInputDate').value+=a;
tryToConvertDate();
}

function enterNumberIntoInputDate(a,b){
document.getElementById('inputDate').value+=a;
document.getElementById('hidenInputDate').value+=b?b:a;
tryToConvertDate();
}

function selectKeyBoard(){
a=document.getElementById("keyboardType").value;
for (var q=0;q<8;q++){
    hideDiv("displayKeyboard"+q);
}
document.getElementById('inputDate').value="";
document.getElementById('hidenInputDate').value="";
document.getElementById('outputDate').value=""
showDiv("displayKeyboard"+a);
}