var express = require('express');
var _ = require('underscore');
var htmlspecialchars = require('htmlspecialchars');


var config = r_require('/config.js');
var questions = r_require('/models/questions');
var appEvents = r_require('/utils/appEvents.js');
var utils = r_require('/utils/utils');

var router = express.Router();

/*
 * GET /api/questions/
 */ 
router.get('/',function(req,res){

    questions.list({},function(err,docs) {
        if (utils.handleError(err)) return;
        res.send(docs);
    });
});

/*
 * GET /api/questions/:id
 */ 
router.get('/:id',function(req,res){
    questions.get(req.params.id, function(err,doc) {
        if (utils.handleError(err)) return;
        res.send(doc);
    });
});

module.exports = router;