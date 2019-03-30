var SEND_INTERVAL = 3000; // interval 
var CAPTURE_INTERVAL = 30;  // interval of capturing a mouse event
var MAX_SAVED = (1000/CAPTURE_INTERVAL) * (SEND_INTERVAL/1000);

function add_chunk(e) {
	moment= new Date();
	return({
		minutes:moment.getMinutes(),
		seconds:moment.getSeconds(),
		miliseconds:moment.getMilliseconds(),
		mousePlace: {
			positionX: e.clientX,
			positionY: e.clientY
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
			console.log(this.saved)
			this.cacheFull == true
			this.saved = []
			}
		this.saved.push(income)
	}
}

onmousemove = function(){mouseCache.add(add_chunk(event))}
console.log(mouseCache.cacheFull)
setTimeout(console.log(mouseCache.cacheFull),3000)
// if (cacheFull)
// var finalVal = '';

// for (var i = 0; i < content.length; i++) {
//     var value = content[i];

//     for (var j = 0; j < value.length; j++) {
//         var innerValue =  value[j]===null?'':value[j].toString();
//         var result = innerValue.replace(/"/g, '""');
//         if (result.search(/("|,|\n)/g) >= 0)
//             result = '"' + result + '"';
//         if (j > 0)
//             finalVal += ',';
//         finalVal += result;
//     }

//     finalVal += '\n';
// }

// console.log(finalVal);

// var download = document.getElementById('download');
// download.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(finalVal));
// download.setAttribute('download', 'test.csv');