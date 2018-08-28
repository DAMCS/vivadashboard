"use strict";
var page = require('webpage').create(),
    system = require('system');

if (system.args.length < 2) {
    console.log('ERROR');
    phantom.exit();
}

var address = system.args[1];

page.open(address, function(status) {
    if (status === 'success') {
		setTimeout(function(){
			var pageURL = page.evaluate(function() {
				return window.location.href;
			});
			console.log(pageURL);
			phantom.exit();
		}, 3000);
    } else {
        console.log('ERROR');
        phantom.exit();
    }
});