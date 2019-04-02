var SEND_INTERVAL = 3000; // interval 
var CAPTURE_INTERVAL = 30;  // interval of capturing a mouse event
var MAX_SAVED = (1000/CAPTURE_INTERVAL) * (SEND_INTERVAL/1000);
var CHUNK_TYPE_MOUSE = 0
var CHUNK_TYPE_KEYBOARD = 1
var CHUNK_TYPE_SCROLL = 2
var GENERAL_INFO = 3
var CHUNK_TYPE_DOUBLECLICK = 4
var CHUNK_TYPE_SELECTED_TEXT = 5

function add_chunk_mouse(e) {
	moment = new Date();
	site_url = document.location.href
	return({
		type: CHUNK_TYPE_MOUSE,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		data: {
			positionX: e.clientX,	
			positionY: e.clientY
		}
	})
}
function add_chunk_scroll() {
	moment = new Date();
	site_url = document.location.href
	return({
		type: CHUNK_TYPE_SCROLL,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		data:{
			scrollPositionY: window.scrollY
		}
	})
}
function add_key_chunk(event) {
	moment = new Date();
	site_url = document.location.href
	if (event.shiftKey) {
		var shiftPress = 1
	}
	else {
		var shiftPress = 0
	}
	if (event.ctrlKey) {
		var ctrlPress = 1
	}
	else {
		var ctrlPress = 0
	}
	return({
		type:CHUNK_TYPE_KEYBOARD,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		data: {
			keypress: event.key,
			shiftPress:shiftPress,
			ctrlPress:ctrlPress,
		}
	})
}

function systemInfoPage() {
	moment_in = new Date();
	browserWindowHeight = window.outerHeight;
	browserWindowWidth = window.outerWidth;
	site_url = document.location.href
	return({
		type: GENERAL_INFO,
		current_page:site_url,
		minutes:moment_in.getMinutes(),
		seconds:moment_in.getSeconds(),
		miliseconds:moment_in.getMilliseconds(),
		data: {
			currentHeight:browserWindowHeight,
			currentWidth:browserWindowWidth,
		}
	})
}

function add_chunk_doubleclick(e) {
	moment = new Date();
	site_url = document.location.href
	dblclick = e.type
	return({
		type: CHUNK_TYPE_DOUBLECLICK,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		data: {
			event_name:dblclick,
		}
	})
}

function add_chunk_selected_text(isSelected) {
	moment = new Date();
	site_url = document.location.href
	return({
		type: CHUNK_TYPE_SELECTED_TEXT,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		data: {
			selectedText: isSelected
		}
	})
}




var mouseCache = {
	saved:[],
	cacheFull:false,
	clear: function() {
		this.saved = []
	},
	add:function(income) {
		if (this.saved.length == MAX_SAVED){
			fetch("http://127.0.0.1:5000/api/get_content", {
			  method: "POST", 
			  headers: {
			    'Access-Control-Allow-Origin': 'http://127.0.0.1:5000/'
			  },
			  body: JSON.stringify(this.saved)
			}).then(res => {
			  console.log("Request complete! response:", res.body);
			});
			this.cacheFull == true //TODO cacheFULL flag
			this.saved = []
			}
		this.saved.push(income)
	}
}

onmousemove = function(){mouseCache.add(add_chunk_mouse(event))}





document.addEventListener("keydown", function onPress(event) {
	if (event.key) {
		keyBoardCache.add(add_key_chunk(event))
	}
});

var keyBoardCache = {
	saved:[],
	cacheFull:false,//TODO cacheFULL flag
	clear: function() {
		this.saved = []
	},
	add:function(income) {
		this.saved.push(income)
	}
}
setInterval(function() {fetch("http://127.0.0.1:5000/api/get_content", {
										method: "POST", 
										body: JSON.stringify(keyBoardCache.saved)
											}).then(res => {
												console.log("Request complete! response:", res.body);
											});
										keyBoardCache.clear()},3000)




document.addEventListener("scroll",function onScroll(event) {
	scrollCache.add(add_chunk_scroll())
});

setInterval(function() {fetch("http://127.0.0.1:5000/api/get_content", {
										method: "POST", 
										body: JSON.stringify(scrollCache.saved)
											}).then(res => {
												console.log("Request complete! response:", res.body);
											});
											scrollCache.clear()},3000)

var scrollCache = {
	saved:[],
	cacheFull:false,//TODO cacheFULL flag
	clear: function() {
		this.saved = []
	},
	add:function(income) {
		this.saved.push(income)
	}
}


setInterval(function() {fetch("http://127.0.0.1:5000/api/get_content", {
										method: "POST", 
										body: JSON.stringify(systemInfoPage())
											}).then(res => {
												console.log("Request complete! response:", res.body);
											});},5000)

// TODO
// chrome.runtime.onMessage.addListener(receiver);

// function receiver(request, sender, sendResponse) {
// console.log(request)
// }

document.addEventListener("dblclick",function onDBClick(event) {
	doubleClickCache.add(add_chunk_doubleclick(event))
});

var doubleClickCache = {
	saved:[],
	cacheFull:false,//TODO cacheFULL flag
	clear: function() {
		this.saved = []
	},
	add:function(income) {
		this.saved.push(income)
	}
}
setInterval(function() {fetch("http://127.0.0.1:5000/api/get_content", {
										method: "POST", 
										body: JSON.stringify(doubleClickCache.saved)
											}).then(res => {
												console.log("Request complete! response:", res.body);
											});doubleClickCache.clear()},5000)

var selectedTextCache = {
	saved:false,
	cacheFull:false,//TODO cacheFULL flag
	clear: function() {
		this.saved = []
	},
	add: function(income) {
		if (this.saved === false){
			this.saved = income
		}
	}
}


function checkSelected() {
	var selectedFlag = 0
	if (window.getSelection().toString() === "") 
		{return selectedFlag} 
	else 
		{	
			selectedFlag = 1
			return selectedFlag
		}
}

setInterval(function() {
	if (checkSelected() === 1)
		{fetch("http://127.0.0.1:5000/api/get_content", {
										method: "POST", 
										body: JSON.stringify(add_chunk_selected_text(checkSelected()))
											}).then(res => {
												console.log("Request complete! response:", res.body);
											})}},200)


