var settings = {
    mqtt: {
        host: process.env.MQTT_HOST || 'mqtt://mosquitto',
        user: process.env.MQTT_USER || '',
        password: process.env.MQTT_PASS || '',
        clientId: process.env.MQTT_CLIENT_ID || null
    },
    keepalive: {
        topic: process.env.KEEP_ALIVE_TOPIC || 'keep_alive',
        message: process.env.KEEP_ALIVE_MESSAGE || 'keep_alive'
    },
    debug: process.env.DEBUG_MODE || false,
    auth_key: process.env.AUTH_KEY || '',
    http_port: process.env.PORT || 5000
}

var mqtt = require('mqtt');
var express = require('express');
var bodyParser = require('body-parser');
var multer = require('multer');

var app = express();
function getMqttClient(client) {
    var options = {
        username: client.username,
        password: client.password,
    };
    if (settings.mqtt.clientId) {
        options.clientId = settings.mqtt.clientId
    }

    return mqtt.connect(settings.mqtt.host, options);
}
var mqttClient;

app.set('port', settings.http_port);
app.use(bodyParser.json());

function logRequest(req, res, next) {
    var ip = req.headers['x-forwarded-for'] ||
        req.connection.remoteAddress;
    var message = 'Received request [' + req.originalUrl +
        '] from [' + ip + ']';

    if (settings.debug) {
        message += ' with payload [' + JSON.stringify(req.body) + ']';
    } else {
        message += '.';
    }
    console.log(message);

    next();
}

function authorizeUser(req, res, next) {
    if (settings.auth_key && req.body['key'] != settings.auth_key) {
        console.log('Request is not authorized.');
        res.sendStatus(401);
    }
    else {
        next();
    }
}

function checkSingleFileUpload(req, res, next) {
    if (req.query.single) {
        var upload = multer().single(req.query.single);

        upload(req, res, next);
    }
    else {
        next();
    }
}

function checkMessagePathQueryParameter(req, res, next) {
    if (req.query.path) {
        req.body.message = req.body[req.query.path];
    }
    next();
}

function checkTopicQueryParameter(req, res, next) {

    if (req.query.topic) {
        req.body.topic = req.query.topic;
    }

    next();
}

function ensureTopicSpecified(req, res, next) {
    if (!req.body.topic) {
        res.status(500).send('Topic not specified');
    }
    else {
        next();
    }
}

app.get('/keep_alive/', logRequest, function (req, res) {
    client = {
        username: req.query.username,
        password: req.query.password,
    };
    mqttClient = getMqttClient();
    mqttClient.publish(settings.keepalive.topic, settings.keepalive.message);
    res.sendStatus(200);
});

app.post('/post/', logRequest, authorizeUser, checkSingleFileUpload, checkMessagePathQueryParameter, checkTopicQueryParameter, ensureTopicSpecified, function (req, res) {
    client = {
        username: req.body.username,
        password: req.body.password,
    }
    mqttClient = getMqttClient(client);
    console.log(mqttClient);
    mqttClient.on('connect', function () {
        console.log("Here 2");
        mqttClient.publish(req.body['topic'], req.body['message']);
    });
    mqttClient.on('error', function(){
        console.log('Error')
        mqttClient.end()
    });
    
    res.sendStatus(200);
});

app.get('/subscribe/', logRequest, authorizeUser, function (req, res) {
    client = {
        username : req.query.username,
        password : req.query.password,
    };
    var topic = req.query.topic;
    if (!topic) {
        res.status(500).send('topic not specified');
    }
    else {
        // get a new mqttClient
        // so we dont constantly add listeners on the 'global' mqttClient
        var mqttClient = getMqttClient(client);

        mqttClient.on('connect', function () {
            console.log("subscribed to " + "\"" + topic + "\"")
            mqttClient.subscribe(topic);
        });
        mqttClient.on('error', function(){
            console.log('Error')
            mqttClient.end()
        });
        mqttClient.on('message', function (t, m) {
            console.log("MESSAGE Received")
            if (t === topic) {
                res.write(m.toString('utf8'));
                console.log("Wrote message to " + req)
            }
        });

        req.on("close", function () {
            mqttClient.end();
            console.log("CLOSED");
        });

        req.on("end", function () {
            mqttClient.end();
            console.log("ENDED");
        });
    }
});

app.listen(app.get('port'), function () {
    console.log('Node app is running on port', app.get('port'));
});
