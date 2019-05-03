var SEND_INTERVAL = 3000; // interval 
var CAPTURE_INTERVAL = 20;  // interval of capturing a mouse event
var MAX_SAVED = 10;
var CHUNK_TYPE_MOUSE = 0
var CHUNK_TYPE_KEYBOARD = 1
var CHUNK_TYPE_PAGE_VISIT = 2

// TODO  в json также должен быть пользователь
function add_chunk_mouse(e) {
	moment = new Date();
	site_url = document.location.href
	return({
		type: CHUNK_TYPE_MOUSE,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		positionX: e.clientX,	
		positionY: e.clientY
	})
}
function add_key_chunk(event) {
	moment = new Date();
	site_url = document.location.href
	return({
		type:CHUNK_TYPE_KEYBOARD,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds()
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
				return null
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
												return null
											});
										keyBoardCache.clear()},3000)

// chrome.runtime.onMessage.addListener(receiver);

// function receiver(request, sender, sendResponse) {
// console.log(request)
// }

function pageVisit(time_ml) {
	browserWindowHeight = window.outerHeight;
	browserWindowWidth = window.outerWidth;
	return({
		type: CHUNK_TYPE_PAGE_VISIT,
		current_page:pageVisitCache.saved,
		time_on_page:time_ml
	})
}

function onRefresh(time_ml) {
	fetch("http://127.0.0.1:5000/api/get_content", {
										method: "POST", 
										body: JSON.stringify(pageVisit(time_ml))
											}).then(res => {
												return null;
											})
}

var pageVisitCache = {
	saved:[],
	time:[],
	clear: function() {
		this.saved = ""
	},
	add: function(income) {
		this.saved = income
		this.time = performance.now()
	},
	send_value: function() {
		result = ((performance.now() - this.time) / 1000).toPrecision(4)
		onRefresh(result)
	},
}

window.onload = pageVisitCache.add(document.location.href);
window.addEventListener('beforeunload', function(event) {
   pageVisitCache.send_value()
});

