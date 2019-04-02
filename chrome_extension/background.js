console.log('background script')
// chrome.tabs.query({},function(tabs) 
// 	{for (var i = 0;i<tabs.length;i++) 
// 		{if (tabs[i].active) 
// 			{
// 				chrome.tabs.sendMessage(tabs[i].id,'hi');
// 				console.log(tabs[i].id)
// 			}
// 		}
// 	console.log(tabs)})
// chrome.browserAction.onClicked.addListener(buttonClicked);
// chrome.browserAction.onClicked.addListener(buttonClicked);
// function buttonClicked(tab) {
// 	setInterval(chrome.tabs.sendMessage(tab.id,'hi'),5000);
// }
chrome.alarms.onAlarm.addListener(function( alarm ) {
  console.log("Got an alarm!", alarm);
});