const { exec } = require("child_process");
const express = require("express");
const server = express();

exec("python test.py");
