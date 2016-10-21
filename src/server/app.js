/* 
* @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
* @Date:   2016-01-25 11:08:47
* @Last Modified by:   lutzer
* @Last Modified time: 2016-10-21 09:40:26
*/

/* use absolute paths for require */
global.r_require = function(name) {
    return require(__dirname + name);
}

/* setup logging */
var winston = require('winston')
winston.level = 'debug'
winston.remove(winston.transports.Console);
winston.add(winston.transports.Console, {'timestamp':true});

global.log = function(level,string,object) {

	if (typeof(object) !== 'undefined')
		winston.log(level,string,object)
	else
		winston.log(level,string)
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
    log("info","Polylogue2 Web-Server listening on "+config.hostname+":"+config.port);
});