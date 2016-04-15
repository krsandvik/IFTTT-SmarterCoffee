
var express = require('express');
var spawn = require("child_process").spawn;
var request = require('request');
var app = express();
app.use(require('morgan')('dev'));

/*
Explanation of parameters:
-f F        Which function to call, 1 = startbrew whit options -c -g -m -s,
              2 = startbrew whit settings already on brewer, 3 = start
              hotplate whit option -m, 4 = set cups whit option -c, 5 = set
              strength whit option -2, 6 = defin grinder or filter whit option
              -g
  -c C        Define how many cups that will be brewed choose between 1 - 12
  -g G        Define is grinder or filter should be used. 1 for grinder, 0 for
              filter
  -m M        Define how many minutes hot plate should be on. define in minutes
              minimum 5
  -s S        Define whick strenght it should be. choose between 1 - 3
*/
// Get status from coffee machine 
app.get('/status', (req, res) => {
  getStatus(res, data => res.json(data));
});
// NOTE: For me 2 smarter coffee cups is 1 normal cup
// Brew 2 cups -f, 1 = startbrew whit options, -c, 2 = defines 2 cups, -g, 1 = defines grinder, -m, 15 = hotplate on 15 minutes, -s strenght strong  
// "make1cupsofcoffee" is the the end of your url http://YourPublicIP:3000/make1cupsofcoffee 
app.post('/make1cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "2", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

// Makes 2 cups of coffee. Grinder, 15 min hotplate, strong 
app.post('/make2cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "4", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

// Makes 3 cups of coffee. Grinder, 15 min hotplate, strong 
app.post('/make3cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "6", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

// Makes 4 cups of coffee. Grinder, 15 min hotplate, strong 
app.post('/make4cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "8", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

//The rest of the status function 
function getStatus(res, successCallback) {
  const status = spawn('python',["pollingStatusMessage.py"]);
  status.stdout.setEncoding("utf8");
  status.stdout.on('data', statusData => {
    console.log('Received status from coffee maker');
    request("https://maker.ifttt.com/trigger/status/with/key/2rVVw18PCVkmhyzDGX1YX", { form: { value1: statusData } }, function(error, response, body) {
      if (error) {
        console.log('Unable to send request to IFTTT', error);
        res.status(500).end();
      }
      console.log('Successfully triggered push to IFTTT!');
      if (successCallback) successCallback(statusData);
    });
 });
}

//This is the port you need to forward to your server 
app.listen(3000, () => {
  console.log('listening on port 3000');
});
