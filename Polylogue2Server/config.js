/* CONFIG FILE */

var Config = {
	
	databaseFile : __dirname + "/data", //chmod this path 777

	baseUrl : '/', // with trailing /
	servePublicDir : true,
	hostname : false, // 127.0.0.1 = private, false = public
	port : '8081',

	submissionDiscussTime: 5 * 60 * 1000 //how long is a submission open do discuss

};

module.exports = Config;