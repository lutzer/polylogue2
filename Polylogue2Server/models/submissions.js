var fs = require('fs');
var exec = require('child_process').exec;

var Database = r_require('/models/database');
var config = r_require('/config');
var utils = r_require('/utils/utils');

var Submission = {

	create : function(data,callback) {
		var db = new Database();

		//add timestamp
		data.createdAt = new Date();

		//add message array
		data.messages = [];

		db.submissions.insert(data,callback)

		//print out submission
		/*if (data.message) {

			//escape double quotes TODO: escape all special strings
			var msg = data.message.toString().replace(/"/g, '\\"');
			log("debug","Submission msg",msg);

			// var process = exec('/bin/python2 /home/pi/scripts/printer/polylogue.py -m "'+msg+'"',
			// 	{ cwd : '/home/pi/scripts/printer'},
			// 	function(error, stdout, stderr) {
			// 		console.log(stdout);	
			// 		if (error !== null) {
			//       		console.log(`exec error: ${error}`);
			//     	}
			// 	}
			// );
		}*/
	},

	addMessage : function(message, callback) {
		var db = new Database();
		db.submissions.findOne({ _id : message.submissionId }, (err,doc) => {
			if (err) {
				callback(err);
				return;
			}

			message.createdAt = new Date();
			doc.messages.push(message);


			db.submissions.update({ _id : message.submissionId}, doc, callback);
		});
	},

	get : function(id,callback) {

		var db = new Database();
		db.submissions.findOne({ _id : id }, callback);
	},

	getLast: function(callback) {
		var db = new Database();
		var cursor = db.submissions.find({}).limit(1).sort( { createdAt : -1 } )
		cursor.toArray(function(err,docs) {
			if (err) {
				callback(err);
				return;
			}
			if (docs.length > 0 )
				callback(err,docs[0],0);
			else
				callback(err,undefined,0);

		});
	},

	list : function(options,callback) {

		var db = new Database();
		db.submissions.find({}, function(err, cursor) {
			
			if (err) {
				callback(err);
				return;
			}

			//apply options
			if (options.sort)
				cursor = cursor.sort(options.sort);
			if (options.skip)
				cursor = cursor.skip(options.skip);
			if (options.limit)
				cursor = cursor.limit(options.limit);

			//send data and count
			cursor.toArray(function(err,docs) {
				callback(err,docs,0);
			});
		});
	},

	count : function(callback) {
		var db = new Database();
		db.submissions.find({}).count(callback);
	},

	remove : function(id,callback) {
		var db = new Database();
		db.submissions.remove({_id: id},callback);
	},


}

module.exports = Submission;