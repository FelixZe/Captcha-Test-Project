const { exec } = require("child_process");
const express = require("express");
const server = express();
//const keep_alive = require("./keep_alive.js");

exec("python test.py");
