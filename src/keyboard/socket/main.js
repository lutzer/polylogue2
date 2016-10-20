/*
* @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
* @Date:   2016-10-19 23:24:23
* @Last Modified by:   lutzer
* @Last Modified time: 2016-10-19 23:31:09
*/

'use strict';


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

/* require dependencies */
var express = require('express');
var app = express();
var http = require('http').Server(app);
var config = r_require('/config.js')

/* Load Sockets */
var sockets = r_require('/sockets.js')(http);

/* Run the server */
http.listen(config.port,config.hostname,function(){
    log("info","Node Server listening on "+config.hostname+":"+config.port);
});