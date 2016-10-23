/*
* @Author: Lutz Reiter, Design Research Lab, Universität der Künste Berlin
* @Date:   2016-10-23 11:23:21
* @Last Modified by:   lutzer
* @Last Modified time: 2016-10-23 12:15:05
*/

'use strict';

var _ = require('underscore');

var list = []

list['id1'] = { available : false }
list['id2'] = { available : false }
list['id3'] = { available : false }

//console.log(list['id1'])

var nl = _.filter(_.values(list), function(ele) {
	return ele.available
});

console.log(nl)