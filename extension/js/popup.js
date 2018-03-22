// DOM elements in popup
var toggleSwitch = document.getElementById('myonoffswitch');

// this port is available as soon as popup is opened
var popupPort = chrome.runtime.connect({name: 'POPUPCHANNEL'});

//lay gia tri toggleSwitchState tu localStorage
//on/off show requests capture
toggleSwitch.checked = localStorage.getItem("toggleSwitchState") === "true";

//DOM logger de show requests capture
var loggerList = document.getElementById('logger');

// Options which are shared with Background Page.
var appOptions = {
  toggleSwitchState: false,
}


// long-lived connection to the background channel 
chrome.runtime.onConnect.addListener(function(port){
  console.assert(port.name === 'BACKGROUNDCHANNEL');
  console.log("Connected to background");

  port.onMessage.addListener(function(msg) {
    if (msg.logcache) {
      showLogs(msg.logcache.items, loggerList);
    }});

});

// takes an array of log messages and appends in the container
// items is of Deque type
function showLogs(items, container) {
  container.innerHTML = ""; // clear it first
  for (var i = 0; i < items.length; i++) {
    var entry = document.createElement('li');
    var node = document.createElement('div');
    node.innerHTML = items[i];
    entry.appendChild(node);
    container.appendChild(entry);
  }
}

toggleSwitch.addEventListener('click', function() {
    appOptions.toggleSwitchState = !appOptions.toggleSwitchState;
    popupPort.postMessage({options: appOptions});

    localStorage.setItem('toggleSwitchState', appOptions.toggleSwitchState);
}, false);
