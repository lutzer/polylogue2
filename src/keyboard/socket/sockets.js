/*
* @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
* @Date:   2016-10-19 23:26:25
* @Last Modified by:   lutzer
* @Last Modified time: 2016-10-20 00:04:01
*/

'use strict';

var socketio = require('socket.io');
var _ = require('underscore');

module.exports = function (http) {

	var io = socketio(http);

	io.on('connection', function(socket){

	    log("info",'Socket: User connected, usercount: '+ io.engine.clientsCount);

	    function onKeyPress(key) {
	    	// send to all other clients
	    	socket.broadcast.emit('keypress',key);
	    }
	    socket.on('keypress', onKeyPress)

		function errorHandler(err) {
			log("error","Socket error: ",err);
		};
		socket.on('error', errorHandler);

	    // Clean up after disconnect
	    socket.on('disconnect', function(){
	        log("info",'Socket: User disconnected');

	        //remove server events
	        socket.removeListener('error',errorHandler);
	        socket.removeListener('keypress',onKeyPress);
	    });

	});

};