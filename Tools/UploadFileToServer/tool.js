const http = require("http");

const networkInterfaces = require("os").networkInterfaces;
const fs = require("fs");

function GetRemoteIpv4() {
  const nets = networkInterfaces();
  const results = [];
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
      // 'IPv4' is in Node <= 17, from 18 it's a number 4 or 6
      const familyV4Value = typeof net.family === "string" ? "IPv4" : 4;
      if (net.family === familyV4Value && !net.internal) {
        results.push(net.address);
      }
    }
  }
  if (results.length > 0) {
    return results[0];
  }
  return "";
}

exports.GetRemoteIpv4 = GetRemoteIpv4;
