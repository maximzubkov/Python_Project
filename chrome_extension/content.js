var SEND_INTERVAL = 3000; // interval 
var CAPTURE_INTERVAL = 30;  // interval of capturing a mouse event
var MAX_SAVED = (1000/CAPTURE_INTERVAL) * (SEND_INTERVAL/1000);
var CHUNK_TYPE_MOUSE = 0
var CHUNK_TYPE_KEYBOARD = 1
var CHUNK_TYPE_SCROLL = 2

function add_chunk_mouse(e) {
	moment= new Date();
	site_url = document.location.href
	return({
		type: CHUNK_TYPE_MOUSE,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		mousePlace: {
			positionX: e.clientX,
			positionY: e.clientY
		}
	})
}
function add_chunk_scroll() {
	moment= new Date();
	site_url = document.location.href
	return({
		type: CHUNK_TYPE_SCROLL,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		scrollPositionY: window.scrollY
	})
}
function add_key_chunk(event) {
	moment= new Date();
	site_url = document.location.href
	return({
		type:CHUNK_TYPE_KEYBOARD,
		current_page:site_url,
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		keypress: event.key,
		shiftPress:event.shiftKey,
		ctrlPress:event.ctrlKey,
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
			console.log(this.saved)
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
setInterval(function() {console.log(keyBoardCache.saved);keyBoardCache.saved=[]},3000)




document.addEventListener("scroll",function onScroll(event) {
	scrollCache.add(add_chunk_scroll())
});
setInterval(function() {console.log(scrollCache.saved);scrollCache.saved=[]},3000)

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






