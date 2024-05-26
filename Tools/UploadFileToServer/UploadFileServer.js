const http = require("http");
const fs = require("fs");
const { RequestWrapper } = require("./HttpWrapper");

const TEXT_FILE_SAVING_PATH = "./text_uploaded.txt";

const REQ_TYPE_UNKNOWN = 0;
const REQ_TYPE_GET_FILE = 1;
const REQ_TYPE_UPLOAD_FILE = 2;
const REQ_TYPE_COMMAND = 3;

const CMD_TYPE_UNKNOWN = 0;
const CMD_TYPE_UPLOAD_TEXT = 0;

class UploadFileServer {
  constructor(main_page, save_path, server_host, server_port) {
    this.main_page = main_page;
    this.save_path = save_path;
    this.#prepareFolder(this.save_path);

    this.server_host = server_host;
    this.server_port = server_port;
    this.server = http.createServer(this.#requestCallback.bind(this));
  }

  start(cb) {
    const server_ref = this.server;
    this.server.listen(this.server_port, this.server_host, () => {
      if (cb) {
        cb(server_ref);
      }
    });
  }

  #requestCallback(req, res) {
    this.#processRequest(req, res);
  }

  #processRequest(req, res) {
    switch (this.#getRequestType(req)) {
      case REQ_TYPE_GET_FILE: {
        this.#loadFileToResponse(res, req.url);
        break;
      }
      case REQ_TYPE_UPLOAD_FILE: {
        this.#saveFileToLocal(req, req.url);
        break;
      }
      case REQ_TYPE_COMMAND: {
        const command = this.#getCommand(req);
        this.#executeCommand(command);
        break;
      }
      default: {
        console.error(
          `Unknown request: { method = ${req.method}, url = ${req.url} s}`
        );
        break;
      }
    }
  }

  #getRequestType(req) {
    console.log("requst url is: ", req.url);
    if (this.#isCommandRequest(req)) {
      return REQ_TYPE_COMMAND;
    } else if (req.method === "GET") {
      return REQ_TYPE_GET_FILE;
    } else if (req.method === "POST") {
      return REQ_TYPE_UPLOAD_FILE;
    } else {
      return REQ_TYPE_UNKNOWN;
    }
  }

  #isCommandRequest(req) {
    if (req.method === "POST" && req.url.substr(0, 4) === "/cmd") {
      return true;
    }
    return false;
  }

  #loadFileToResponse(res, filename) {
    const server_file_path = this.#parseToServerPath(filename);
    const loaded_file = this.#loadFile(res, server_file_path);
    loaded_file.pipe(res);
  }

  #saveFileToLocal(req, filename) {
    const prepare_file = this.#saveFile(filename);
    const req_wrapper = new RequestWrapper(req);

    if (prepare_file) {
      req_wrapper.writeToFile(prepare_file);
    } else {
      console.error(`Save file ${filename} failed\n`);
    }
  }

  #executeCommand(command) {
    console.log(`Execute command: ${command.cmd_type}`);
    switch (command.cmd_type) {
      case CMD_TYPE_UPLOAD_TEXT: {
        this.#uploadText(command);
        break;
      }
      default: {
        console.log(`Unknown command ${command.cmd_type}`);
        break;
      }
    }
  }

  #uploadText(command) {
    const req = command.cmd_req;
    if (req) {
      const prepare_file = this.#saveFile(TEXT_FILE_SAVING_PATH);
      const req_wrapper = new RequestWrapper(req);
      if (prepare_file) {
        req_wrapper.writeToFile(prepare_file);
      } else {
        console.error(`Save file ${TEXT_FILE_SAVING_PATH} failed\n`);
      }
    } else {
      console.error("Cannot find valid request object in command!");
    }
  }

  #loadFile(res, filename) {
    console.log(`Load file: ${filename}`);
    return fs
      .createReadStream(filename, { flags: "r" })
      .on("error", function () {
        console.log(`load ${filename} failed`);
        res.writeHead(404);
        res.end("<h1>404 Read Error</h1>");
      });
  }

  #saveFile(filename) {
    console.log(`Save file: ${filename}`);
    if (this.#prepareFolder(this.save_path)) {
      if (filename[0] !== "/") {
        filename = "/" + filename;
      }
      return fs
        .createWriteStream(this.save_path + filename)
        .on("error", function (error) {
          console.error(`save file ${filename} failed`);
          console.error(`${error.message}`);
        });
    }
    return null;
  }

  #getCommand(req) {
    if (req.url.substr(0, 4) !== "/cmd") {
      return {
        cmd_type: CMD_TYPE_UNKNOWN,
        cmd_req: null,
      };
    }

    const cmd_string = req.url.substr(5);
    return {
      cmd_type: this.#getCommandType(cmd_string),
      cmd_req: req,
    };
  }

  #getCommandType(cmd_string) {
    switch (cmd_string) {
      case "upload_text": {
        return CMD_TYPE_UPLOAD_TEXT;
      }
      default: {
        return CMD_TYPE_UNKNOWN;
      }
    }
  }

  #parseToServerPath(filename) {
    if (filename === "/") {
      return this.main_page;
    } else if (filename[0] === "/") {
      return "." + filename;
    } else {
      return filename;
    }
  }

  #prepareFolder(folder_path) {
    if (fs.existsSync(folder_path)) {
      return true;
    } else {
      if (fs.mkdirSync(folder_path)) {
        console.log(`Create folder ${folder_path}`);
        return true;
      }
    }
    return false;
  }
}

exports.UploadFileServer = UploadFileServer;
