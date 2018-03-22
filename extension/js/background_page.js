//TODO:
//chrome.management.get("fhbjgbiflinjbdggehcddcbncdddomop", function(a) {console.log(a)})
//chrome.management.launchApp("fhbjgbiflinjbdggehcddcbncdddomop", function(a) {console.log(a)}) to open the app

var blacklistedIds = ["none"],

	// enum for postman message types
	postmanMessageTypes = {
	  xhrError: "xhrError",
	  xhrResponse: "xhrResponse",
	  captureStatus: "captureStatus",
	  capturedRequest: "capturedRequest"
	},

	// indicates status of popup connected
	popupConnected = false,

	// placeholder for the background page port object for transferring log msgs
	BackgroundPort,

	// object store to cache captured requests
	requestCache = {},

	// storing last N (maxItems) log messages
	maxItems = 10,
	logCache = new Deque(maxItems),

	background = this,

	// Options which are shared with Extension Popup.
	appOptions = {
		isCaptureStateEnabled: false,
		filterRequestUrl: '.*'
	},

	// requestId is a chrome-specific value that we get in the onBeforeSendHeaders handler
	// postman-interceptor-token is a header (X-Postman-Interceptor-Id) that we add in the interceptor code
	requestTokenMap = {}, // map from postman-interceptor-token to postmanMessage and requestId.
	requestIdMap = {}, // map from requestId to postmanMessage and postman-interceptor-token.
	CUSTOM_INTERCEPTOR_HEADER = "X-Postman-Interceptor-Id",

	restrictedChromeHeaders = [
	    "ACCEPT-CHARSET",
	    "ACCEPT-ENCODING",
	    "ACCESS-CONTROL-REQUEST-HEADERS",
	    "ACCESS-CONTROL-REQUEST-METHOD",
	    "CONTENT-LENGTHNECTION",
	    "CONTENT-LENGTH",
	    "COOKIE",
	    "CONTENT-TRANSFER-ENCODING",
	    "DATE",
	    "EXPECT",
	    "HOST",
	    "KEEP-ALIVE",
	    "ORIGIN",
	    "REFERER",
	    "TE",
	    "TRAILER",
	    "TRANSFER-ENCODING",
	    "UPGRADE",
	    "USER-AGENT",
	    "VIA"
	],

	postmanCheckTimeout = null,
	isPostmanOpen = true;

// returns an edited header object with retained postman headers
function onBeforeSendHeaders(details) {
	//console.log("2: ", details.method, details.url);
}


// for filtered requests sets a key in requestCache
function onBeforeRequest(details) {
    requestCache[details.requestId] = details;
    //console.log(details.method, details.url);
}

// for filtered requests it sets the headers on the request in requestcache
function onSendHeaders(details) {
    if (requestCache.hasOwnProperty(details.requestId)) {
    	console.log(details.method, details.url);
      //sendCapturedRequestToPostman(details.requestId);
    } else {
      console.log("Hidden request:", details.method, details.url);
    }
  //}
}

// sends the captured request to postman with id as reqId (using the requestCache)
// then clears the cache
function sendCapturedRequestToPostman(reqId){
  var loggerMsg = "<span>" + requestCache[reqId].method + "&nbsp;&nbsp;" + "</span><span class=\"captured-request-url\">" + (requestCache[reqId].url).substring(0, 150) + "</span>";

  chrome.runtime.sendMessage(
      {
        "postmanMessage": {
          "reqId": reqId,
          "request": requestCache[reqId],
          "type": postmanMessageTypes.capturedRequest
        }
      },
      function response(resp) {
          sendCapturedRequestToFrontend(loggerMsg);
          delete requestCache[reqId];
          //clearTimeout(requestNotReceived);
      }
  );
}

// sends the captured request to popup.html
function sendCapturedRequestToFrontend(loggerObject) {
  logCache.push(loggerObject);
  if (popupConnected) {
    BackgroundPort.postMessage({logcache: logCache});
  }
}

/*
// long-lived connection to the popupchannel (as popup is opened)
// notifies when popup can start listening
chrome.runtime.onConnect.addListener(function(port){
  console.assert(port.name === 'POPUPCHANNEL');
  BackgroundPort = chrome.runtime.connect({name: 'BACKGROUNDCHANNEL'});
  popupConnected = true;

  port.onMessage.addListener(function(msg) {
    if (msg.options) {
      appOptions.isCaptureStateEnabled = msg.options.toggleSwitchState;
    }
    if(msg.reset) {
        logCache.clear();
    }
  });

  BackgroundPort.postMessage({options: appOptions});
  BackgroundPort.postMessage({logcache: logCache});
  console.log("Sending isPostman Open: " , isPostmanOpen);
  BackgroundPort.postMessage({isPostmanOpen: isPostmanOpen});

  // when the popup has been turned off - no longer send messages
  port.onDisconnect.addListener(function(){
    popupConnected = false;
  });

});*/

// adds an event listener to the onBeforeSendHeaders
chrome.webRequest.onBeforeSendHeaders.addListener(onBeforeSendHeaders,
	{ urls: ["<all_urls>"] },
	[ "blocking", "requestHeaders" ]
);


// event listener called for each request to intercept - used to intercept request data
chrome.webRequest.onBeforeRequest.addListener(onBeforeRequest, 
    { urls: ["<all_urls>"] }, 
    [ "requestBody" ]
);

//event listener called just before sending - used for getting headers
chrome.webRequest.onSendHeaders.addListener(onSendHeaders, 
    { urls: ["<all_urls>"] }, 
    [ "requestHeaders" ]
);
