var Mongo_Modul = require("./MODULLER/mongo_modul");
var Ups_Modul = require("./MODULLER/ups_modul");
var Fonksiyonlar_Modul = require("./MODULLER/fonksiyonlar_modul");
var Remote_Server_Modul = require("./MODULLER/remote_server_modul");

var ConfigParser = require('configparser');
var path = require('path');
var moment = require('moment');
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var io_client = require('socket.io-client');

var config = new ConfigParser();
config.read('../config.ini');

const LOCAL_SOKET_PORT = 3001;
const REMOTE_SERVER_IP = config.get('AYARLAR', "REMOTE_SERVER_IP");
const REMOTE_SERVER_SOKET_PORT = config.get('AYARLAR', "REMOTE_SERVER_SOKET_PORT");
const OFSIS_SERVER_URL = `http://${REMOTE_SERVER_IP}:${REMOTE_SERVER_SOKET_PORT}/`;


var remote_server_soket_client = io_client.connect(OFSIS_SERVER_URL, { reconnect: true });
app.use(express.static(path.join(__dirname, '/WEB/')));
app.get('/', function (req, res) { res.sendFile(__dirname + '/WEB/index.html') });
http.listen(LOCAL_SOKET_PORT, function () { console.log('http://localhost:' + LOCAL_SOKET_PORT) });


Fonksiyonlar_Modul.SISTEM_RESET_FONK(LOCAL_SOKET_PORT);
Remote_Server_Modul.REMOTE_SERVER_FONK(remote_server_soket_client, io);

setInterval(Ups_Modul.UPS_VERI_FUNC, 1000, io);


var role_string = "";


io.on('connection', function (socket) {

    socket.on('tum_veri_dict', function (tum_veri) {
        io.emit('tum_veri_dict', tum_veri);
        remote_server_soket_client.emit('tum_veri_dict', tum_veri);


        if (tum_veri["SISTEM_DURUM"] != "NORMAL") {
            Mongo_Modul.MONGO_KAYIT_SORGULA(io, remote_server_soket_client)
                .then()
                .catch(console.error)
        };
    });

    socket.on('role_dict', function (role_dict) {
        io.emit('role_dict', role_dict);
        role_string = role_dict;
        // console.log(data);
    });

    socket.on('komut_kanal', function (komut_kanal) {
        io.emit('komut_kanal', komut_kanal);
        if (komut_kanal == "SISTEM_RESET") {
            Fonksiyonlar_Modul.SISTEM_RESET_FONK(LOCAL_SOKET_PORT);
        }
        console.log(komut_kanal);
    });

    if (remote_server_soket_client.connected) {
        io.emit('server_durum', true);
    }
    else {
        io.emit('server_durum', false);
    };

    socket.on('VERITABANI_SIFIRLA', function () {
        Mongo_Modul.VERITABANI_SIFIRLA_FONK()
            .then(console.log)
            .catch(console.error)
    });

    io.emit('role_dict', role_string);

    Mongo_Modul.MONGO_KAYIT_SORGULA(io, remote_server_soket_client)
        .then()
        .catch(console.error)
});

