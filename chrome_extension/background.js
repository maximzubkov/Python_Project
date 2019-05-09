var isExtensionOn = false;
var microsecondsPerTenYears = 1000 * 60 * 60 * 24 * 7 * 31 * 12 *10;
var tenYearsAgo = (new Date).getTime() - microsecondsPerTenYears;
chrome.history.search({
						text: '', 
						startTime: tenYearsAgo , 
						endTime :  (new Date).getTime(), 
						maxResults : 10000}, function(data) {
	var res = {
		pages : [],
		add: function(income) {
			this.pages.push(income) 
		},
		send: function() {
			fetch("http://127.0.0.1:5000/api/get_history", {
			  method: "POST", 
			  headers: {
			    'Access-Control-Allow-Origin': 'http://127.0.0.1:5000/'
			  },
			  body: JSON.stringify(this.pages)
			}).then(res => {
				return res
			})
		}
	}
	function addHistoryInstance(page) {
		return({
			url: page.url,
			moment: page.lastVisitTime
		})
	}
    data.forEach(function(page) {
        res.add(addHistoryInstance(page))
    });
   	res.send()
});
