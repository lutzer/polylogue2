var fs = require('fs');
var _ = require('underscore');

var Database = r_require('/models/database');
var config = r_require('/config');
var utils = r_require('/utils/utils');

var Question = {

	create : function(data,callback) {
		var db = new Database();

		if (!_.has(data,'boxId'))
			data.boxId = -1;

		if (!_.has(data,'question'))
			data.question = "undefined";

		if (!_.has(data,'duration'))
			data.duration = 60 * 3000; //standard time three minutes

		//add timestamp
		data.createdAt = new Date();
		//add message array
		data.messages = [];


		//set expire time
		data.expired = false;
		data.expiresAt = new Date(Date.now() + data.duration).toJSON();

		db.questions.insert(data,callback)
	},

	addMessage : function(message, callback) {
		var db = new Database();
		db.questions.findOne({ _id : message.questionId }, (err,doc) => {
			if (err) {
				callback(err);
				return;
			}

			//check if message expired
			if (doc.expired) {
				callback(new Error("Question already expired"));
				return;
			}

			message.createdAt = new Date();
			doc.messages.push(message);
			db.questions.update({ _id : message.questionId}, doc, (err) => {
				if (err) {
					callback(err);
					return;
				}
				callback(null,doc);
			});
		});
	},

	setExpired : function(query, callback) {
		var db = new Database();

		db.questions.update(query, {$set: {expired: true}}, {multi: true}, callback)
	},

	get : function(id,callback) {

		var db = new Database();
		db.questions.findOne({ _id : id }, callback);
	},

	getLast: function(callback) {
		var db = new Database();
		var cursor = db.questions.find({}).limit(1).sort( { createdAt : -1 } )
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

	// returns only message that are not expired yet
	getActive: function(callback) {
		var db = new Database();
		var cursor = db.questions.find({ expired : false });
		cursor.toArray(function(err,docs) {
			if (err) {
				callback(err);
				return;
			}
			callback(err, docs);

		});
	},

	list : function(options,callback) {

		var db = new Database();
		db.questions.find({}, function(err, cursor) {
			
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
		db.questions.find({}).count(callback);
	},

	remove : function(id,callback) {
		var db = new Database();
		db.questions.remove({_id: id},callback);
	},


}

module.exports = Question;