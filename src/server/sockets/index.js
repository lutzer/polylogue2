var socketio = require('socket.io');
var _ = require('underscore');

var questions = r_require('/models/questions');
var appEvents = r_require('/utils/appEvents');
var config = r_require('/config.js');

module.exports = function (http) {

	var io = socketio(http);

	var nsp_box = io.of('/box');
	var nsp_phone = io.of('/phone')

	/* NAMESPACE FOR BOXES */

	nsp_box.on('connection', function(socket){

	    log("info",'Socket: Box connected, usercount: '+ io.engine.clientsCount);

	    /* Server event handlers */
	    
	    function questionAddedHandler(data) {
	    	log("info",'Socket: recieved <question:new>', data);
		    questions.create(data, function(err, docs) {
		        if (err) {
		        	log("error", "Error adding question: ", err);
		        	return;
		        }
		        if (docs.length > 0)
					nsp_phone.emit('question:new',docs[0]); // send to phones
		    });
	    };
		socket.on('question:new', questionAddedHandler);

		function questionExpiredHandler(data) {
			log("info","Socket: received <question:expired>", data);
			nsp_phone.emit('question:expired',data);
			questions.setExpired(data, (err) => {
				if (err) { 
					log("error", "Error handling <question:expired>: ", err);
					return;
				}
			});
		}
		socket.on('question:expired', questionExpiredHandler);

		function errorHandler(err) {
			log("error","Socket error: ",err);
		};
		socket.on('error', errorHandler);

	    // Clean up after disconnect
	    socket.on('disconnect', function(){
	        log("info",'Socket: User disconnected');

	        //remove server events
	        socket.removeListener('question:new',questionAddedHandler);
	        socket.removeListener('question:expired',questionExpiredHandler);
	        socket.removeListener('error',errorHandler);
	    });

	});

	/* NAMESPACE FOR PHONES */

	nsp_phone.on('connection', function(socket){

	    log("info",'Socket: Phone connected, usercount: '+ io.engine.clientsCount);

	    socket.emit('connected');

	    /* check if there are any active questions and return them */
	    
        questions.getActive( (err, docs) => {
            if (err) {
            	log("error","Fetching active questions: ", err)
            	return;
            }
            _.each(docs, function(doc) {
            	socket.emit('question:new',doc);
            })
        });

	    /* Server event handlers */

		function newMessageHandler(data) {
			log("info","Socket: received <message:new>", data);
			questions.addMessage(data, (err, doc) => {
				if (err) {
					log("error", "Error adding message: ", err);
					return;
				}
				data.boxId = doc.boxId
				console.log(data);
				nsp_box.emit('message:new',data);
			});
		};
		socket.on('message:new', newMessageHandler);


		function errorHandler(err) {
			log("error","Socket error: ",err);
		};
		socket.on('error', errorHandler);

	    // Clean up after disconnect
	    socket.on('disconnect', function(){
	        log("info",'Socket: User disconnected');

	        //remove server events
	        socket.removeListener('message:new',newMessageHandler);
	        socket.removeListener('error',errorHandler);
	    });

	});

};