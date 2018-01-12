/*facebook.py - this script should be run by casperJS.
Navigate to the desired facebook page and it will log
in with the provided credentials and dump the interpreted
html to console */
var casper = require('casper').create({verbose: false, logLevel: 'debug'});

casper.start('https://www.facebook.com/groups/518171768298214/', function() {
    this.waitForSelector('form#login_form');
});

casper.then(function() {
    this.fill('form#login_form', {'email': '', 'pass': ''}, true);
});

casper.then(function() {
    this.waitForSelector('div#contentArea');
});

casper.run(function() {
    this.echo(casper.getHTML());
    this.exit();
});
