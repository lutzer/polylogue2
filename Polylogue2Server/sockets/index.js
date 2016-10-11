var socketio = require('socket.io');
var _ = require('underscore');

var submissions = r_require('/models/submissions');
var appEvents = r_require('/utils/appEvents');
var config = r_require('/config.js');

module.exports = function (http) {

	var io = socketio(http);

	io.on('connection', function(socket){

	    log("info",'Socket: User connected, usercount: '+ io.engine.clientsCount);

	    socket.emit('connected');

	    //check if there are any active submissions and return them
        submissions.getActive( (err, docs) => {
            if (err) {
            	log("error","Fetching active submission: ", err)
            	return;
            }
            _.each(docs, function(doc) {
            	socket.emit('submission:new',doc);
            })
        });

	    // Server event handlers
	    function submissionAddedHandler(data) {
	    	log("info",'Socket: emit <submission:new>', data);
		    socket.emit('submission:new',data);
	    };
		appEvents.on('submission:new', submissionAddedHandler);

		function newMessageHandler(data) {
			log("info","Socket: received <message:new>", data);
			submissions.addMessage(data, (err) => {
				if (err) log("error", "Error adding message: ", err);
			});
		};
		socket.on('message:new', newMessageHandler);

		function submissionExpiredHandler(data) {
			log("info","Socket: received <submission:expired>", data);
			submissions.setExpired(data, (err) => {
				if (err) log("error", "Error handling <submission:expired>: ", err);
			});
		}
		socket.on('submission:expired', submissionExpiredHandler);

		function errorHandler(err) {
			log("error","Socket error: ",err);
		};
		socket.on('error', errorHandler);

	    // Clean up after disconnect
	    socket.on('disconnect', function(){
	        log("info",'Socket: User disconnected');

	        //remove server events
	        appEvents.removeListener('submission:new',submissionAddedHandler);
	        socket.removeListener('error',errorHandler);
	        socket.removeListener('message:new',newMessageHandler);
	        socket.removeListener('submission:expired',submissionExpiredHandler)
	    });

	});

};