var socketio = require('socket.io');
var submissions = r_require('/models/submissions');

var appEvents = r_require('/utils/appEvents');

module.exports = function (http) {

	var io = socketio(http);

	io.on('connection', function(socket){

	    log("info",'Socket: User connected');

	    socket.emit('connected');

	    //TODO: check if there was any submissions in the past 5 minutes, and send them to the phone

	    // Server event handlers
	    function submissionAddedHandler(data) {
	    	log("info",'Socket: emit <submission:new>', data);
		    socket.emit('submission:new',data);
	    }
		appEvents.on('submission:new', submissionAddedHandler);

		function newMessageHandler(data) {
			log("info","Socket: received <message:new>", data);
		}
		socket.on('message:new', newMessageHandler);

		socket.on('error', function(err) {
	    	log("error",err);
		});


	    // Clean up after disconnect
	    socket.on('disconnect', function(){
	        log("info",'Socket: User disconnected');

	        //remove server events
	        appEvents.removeListener('submissions:new',submissionAddedHandler);
	        socket.removeListener('message:new',newMessageHandler);
	    });

	});

};