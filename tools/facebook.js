/*facebook.py - this script should be run by phantomJS.
Navigate to the desired facebook page and it will log
in with the provided credentials and dump the interpreted
html to console */

var page = new WebPage();

function doLogin(){
    page.evaluate(function() {
        var form = document.getElementById("login_form");

        form.elements["email"].value = "";
        form.elements["pass"].value = "";

        form.submit();
    });
}

page.onLoadFinished = function(status) {
    doLogin();
    window.setTimeout(function() {
        console.log(page.content);
        phantom.exit();
    }, 20000);

};

page.open('https://www.facebook.com/groups/518171768298214/', function(status) {
});
