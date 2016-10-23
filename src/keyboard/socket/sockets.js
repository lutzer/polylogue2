/*
* @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
* @Date:   2016-10-19 23:26:25
* @Last Modified by:   lutzer
* @Last Modified time: 2016-10-23 12:52:42
*/

'use strict';

var socketio = require('socket.io');
var _ = require('underscore');

module.exports = function (http) {

	var io = socketio(http);

	var nsp_box = io.of('/box');
	var nsp_keyboard = io.of('/keyboard')

	var boxList = []
	var currentBox = false

	function getCurrentBox() {

		// return currently selected box
		if (_.has(currentBox,'available')) {
			if (currentBox.available)
				return currentBox;
		}

		// choose new box
		var list = _.filter(_.values(boxList), function(ele) {
			return ele.available
		});
		if (list.length < 1)
			return false;
		return list[_.random(list.length)];
	}

	/* Keyboard namespace */

	nsp_keyboard.on('connection', function(socket){

	    log("info",'Socket: Keyboard connected, usercount: '+ io.engine.clientsCount);

	    function onKeyPress(key) {
	    	// send to one of the boxes
	    	currentBox = getCurrentBox();
	    	if (currentBox) {
	    		//log("info","send keypress to : ",currentBox.socket.id);
	    		currentBox.socket.emit('keypress',key);
	    	}
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

	/* Box namespace */

	nsp_box.on('connection', function(socket){

	    log("info",'Socket: Box connected, usercount: '+ io.engine.clientsCount);

	    // add socket to boxlist
	    boxList[socket.id] = { 
	    	available : true,
	    	socket: socket,
	    }

	    function onAvailable(available) {
	    	console.log(available)
	    	log("info","Box "+ socket.id+ "s et available: "+available);
	    	boxList[socket.id].available = available;
	    }
	    socket.on('available', onAvailable)

		function errorHandler(err) {
			log("error","Socket error: ",err);
		};
		socket.on('error', errorHandler);

	    // Clean up after disconnect
	    socket.on('disconnect', function(){
	        log("info",'Socket: User disconnected');

	        // remove socket from boxlist
	        delete boxList[socket.id];
	        if (_.has(currentBox,'socket'))
	        	if (currentBox.socket.id == socket.id)
	        		currentBox = false;

	        //remove server events
	        socket.removeListener('error',errorHandler);
	        socket.removeListener('available',onAvailable);
	    });

	});
};