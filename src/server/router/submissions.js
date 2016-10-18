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
        if (utils.handleError(err)) return;
        res.send(docs);
    });
});

/*
 * GET /api/submissions/:id
 */ 
router.get('/:id',function(req,res){
    submissions.get(req.params.id, function(err,doc) {
        if (utils.handleError(err)) return;
        res.send(doc);
    });
});

/*
 * POST /api/submissions/
 */ 
router.post('/', function (req, res) {

    log("info",'Received new Submission');

    log("debug","Submission body:",req.body);

    var data = req.body;

    submissions.create(data, function(err, docs) {
        if (utils.handleError(err)) return;

        log("info",'Submission added to database');

        // trigger socket event
        appEvents.emit('submission:new',docs[0])

        // send answer
        res.send(docs[0]);

    });
});

module.exports = router;