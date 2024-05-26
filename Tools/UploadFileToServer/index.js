const { GetRemoteIpv4 } = require("./tool");
const { UploadFileServer } = require("./UploadFileServer");

// TODO: set in json
const server_host = GetRemoteIpv4();
const server_port = 20495;
const save_path = "./received_files";
const main_page = "./index.html";

const server = new UploadFileServer(
  main_page,
  save_path,
  server_host,
  server_port
);

server.start((opened_server) => {
  const server_address = opened_server.address().address;
  const server_port = opened_server.address().port;
  console.log(`Create server at http://${server_address}:${server_port}`);
});
