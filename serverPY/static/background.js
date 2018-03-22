function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

//GET new log from server by json
async function getNewLog() {
    var xmlhttp = new XMLHttpRequest();
    while (true) {
    	xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            showLog(this.responseText);
        	}
   		};
    	xmlhttp.open("GET", "ShowLog", true);
    	xmlhttp.send();
    	//showLog(this.responseText);
    	await sleep(2000);
    }
}

//show log in table
function showLog(newLog) {
    var obj = JSON.parse(newLog);
    var para = document.createElement("p");
	var node = document.createTextNode(obj.url + " " + obj.number);
	para.appendChild(node);
	var element = document.getElementById("content");
	element.appendChild(para);
}


window.onload = function main(){
	getNewLog();
}
