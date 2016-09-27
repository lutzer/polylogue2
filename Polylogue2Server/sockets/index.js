var socketio = require('socket.io');
var submissions = r_require('/models/submissions');

var appEvents = r_require('/utils/appEvents');

module.exports = function (http) {

	var io = socketio(http);

	io.on('connection', function(socket){

	    console.log('Socket: User connected');
	    socket.emit('connected');

	    // Server event handlers

	    function submissionAddedHandler(data) {
	    	console.log('socket emit:<submission:new>');
		    socket.emit('submission:new',data);
	    }
		appEvents.on('submission:new', submissionAddedHandler);

		function newMessageHandler(data) {
			console.log("socket event: <message:new>");
			socket.emit('submission:new',data);
		}
		socket.on('message:new', newMessageHandler);

		socket.on('error', function(err) {
	    	console.log(err);
		});


	    // Clean up after disconnect

	    socket.on('disconnect', function(){
	        console.log('Socket: User disconnected');

	        //remove server events
	        appEvents.removeListener('submissions:new',submissionAddedHandler);
	        socket.removeListener('message:new',newMessageHandler);
	    });

	});

};