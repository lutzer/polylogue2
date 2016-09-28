var fs = require('fs');
var exec = require('child_process').exec;

var Database = r_require('/models/database');
var config = r_require('/config');
var utils = r_require('/utils/utils');

var Submission = {

	create : function(data,callback) {
		var db = new Database();
		db.submissions.insert(data,callback)

		//print out submission
		if (data.message) {

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
		}
	},

	get : function(id,callback) {

		var db = new Database();
		db.submissions.findOne({ _id : id }, callback);
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