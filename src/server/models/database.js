var Tingodb = require('tingodb')();
var fs = require('fs');

var config = r_require('/config');

var Database = function() {
	//saves the data
	var db = new Tingodb.Db(config.databaseFile, {});
	this.questions = db.collection("questions.db");
}

Database.prototype.questions = function() {
	return this.questions;
};

module.exports = Database;