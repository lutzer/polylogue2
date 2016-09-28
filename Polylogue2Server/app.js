/* 
* @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
* @Date:   2016-01-25 11:08:47
* @Last Modified by:   lutzer
* @Last Modified time: 2016-09-28 10:58:20
*/

/* use absolute paths for require */
global.r_require = function(name) {
    return require(__dirname + name);
}

/* alias for logging */
global.log = function(level,string,object) {
	require('winston').log(level,string,object)
}

/*Define dependencies.*/

var express = require('express');
var app = express();
var http = require('http').Server(app);

var config = r_require('/config.js');

/* Load Sockets */

var sockets = r_require('/sockets')(http);

/* Load Router */
var router = r_require('/router')(app);

/* Error Handling */
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
});

/* Run the server */

http.listen(config.port,config.hostname,function(){
    log("info","Node Server listening on "+config.hostname+":"+config.port);
});