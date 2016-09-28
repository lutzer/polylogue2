var express = require('express');
var _ = require('underscore');
var htmlspecialchars = require('htmlspecialchars');


var config = r_require('/config.js');
var submissions = r_require('/models/submissions');
var appEvents = r_require('/utils/appEvents.js');
var utils = r_require('/utils/utils');

var router = express.Router();

/*
 * GET /api/submissions/
 */ 
router.get('/',function(req,res){

    submissions.list({},function(err,docs) {
        utils.handleError(err,res);
        res.send(docs);
    });
});

/*
 * GET /api/submissions/:id
 */ 
router.get('/:id',function(req,res){
    submissions.get(req.params.id, function(err,doc) {
        utils.handleError(err);
        res.send(doc);
    });
});

/*
 * POST /api/submissions/
 */ 
router.post('/', function (req, res) {

    log("info",'Received new Submission');

    log("debug","Submission body:",req.body);

    var data = {
        message : req.body.message
    };

    // trigger socket event and send mesagge to printer
    appEvents.emit('submission:new',data)

    // send answer
    res.send(data);
});

module.exports = router;