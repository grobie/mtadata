var servi = require('servi');
var app = new servi(true);


port(7777);

start();

serveFiles("public");