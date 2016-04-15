
var express = require('express');
var spawn = require("child_process").spawn;
var request = require('request');
var app = express();
app.use(require('morgan')('dev'));

// 1-12
app.post('/cups/:cups', (req, res) => {
  spawn('python',["sendcommand.py", "-f", "4", "-c", req.params.cups]);
  res.json({'cups': req.params.cups});
});

// 1-3
app.post('/strength/:strength', (req, res) => {
  spawn('python',["sendcommand.py", "-f", "5", "-s", req.params.strength]);
  res.json({'strength': req.params.strength});
});

// minutes, >5
app.post('/hotplate/:hotplate', (req, res) => {
  spawn('python',["sendcommand.py", "-f", "5", "-s", req.params.hotplate]);
  res.json({'hotplate': req.params.hotplate});
});

// 0 = grinder; 1 = filter
app.post('/grinder/:grinder', (req, res) => {
  spawn('python',["sendcommand.py", "-f", "6", "-g", req.params.grinder]);
  res.json({'grinder': req.params.grinder});
});

app.post('/brew', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "2"]);
  result.stdout.on('data', (data) => {
    res.type('application/json');
    res.send(data);
  });
});

app.get('/status', (req, res) => {
  getStatus(res, data => res.json(data));
});


app.post('/make1cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "2", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

app.post('/make2cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "4", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

app.post('/make3cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "6", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

app.post('/make4cupsofcoffee', (req, res) => {
  const result =  spawn('python',["sendcommand.py", "-f", "1", "-c", "8", "-g", "1", "-m", "15", "-s", "3"]);
  result.stdout.on('data', (data) => {
    console.log('Started default brewing');
    getStatus(res, () => res.status(200).end());
  });
});

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

app.listen(3000, () => {
  console.log('listening on port 3000');
});
