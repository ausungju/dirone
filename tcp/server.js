const express = require('express');
const net = require('net');
const http = require('http');
// const https = require('https');
const {Server} = require("socket.io");
const {spawn} = require('child_process');

// let options = require("./.config/pem_config").options;

const app = express();
const server = http.createServer(app);
// const server = https.createServer(options, app);
const io = new Server(server);
const ipaddr = "192.168.0.3";

let img = null;
let tcp = net.createServer(function (socket) {
    socket.setEncoding('utf8')

    socket.on('data', function (data) {
        data = String(data);
        if(data.lastIndexOf("끝") !== -1) {
            data = data.split("끝");

            io.emit('img', img+data[0]);
            img = data[1]
        }
        else {
            if(img !== null) img += data;
        }
    });
    socket.on('close', function () {
        console.log(`${socket.address()}client disconnected`);
    });
});
tcp.on('error', (err) => {
    console.log(err.code);
});
tcp.listen(8000, ipaddr, () => {
    console.log('server listen', tcp.address());
});

io.on("connection", (socket) => {
    console.log(`클라이언트 접속 ${socket.id}`);
    io.emit('client_data', `USER: ${socket.id} Enter\n`)

    socket.on('data', (data) => {
        console.log('클라이언트로부터 받은 데이터', data);
        io.emit(data)
        tcp.emit(data)
    });
    socket.on('client_data', (data) => {
        console.log('클라이언트간 전송 데이터', data);
        io.emit(data)
    })
    socket.on('disconnect', () => {
        console.log('클라이언트 접속 해제', socket.id);
        clearInterval(socket.interval);
    });
    socket.on('error', (error) => {
        console.error(error);
    });
});


app.set("view engine", "pug");
app.set("views", __dirname + "/views");
app.use("/public", express.static(__dirname + "/public"));
app.get("/", (_, res) => res.render("index"));
app.get("/*", (_, res) => res.redirect("/"));

const PORT = process.env.PORT || 80;
server.listen(PORT,() => {
    console.log(`listening on *:${PORT}`);
});
