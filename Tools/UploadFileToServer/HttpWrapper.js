class ResponseWrapper {
  constructor(response) {}
}

class RequestWrapper {
  constructor(request) {
    this.req = request;
    this.receivedBytes = 0;
    this.totalBytes = 0;
  }

  writeToFile(prepared_file) {
    if (!prepared_file) {
      console.error(
        `Write to file ${prepared_file} failed! File is not a valid object\n`
      );
    }

    this.req.on("data", (chunk) => {
      this.receivedBytes += chunk.length;
      this.totalBytes += chunk.length;
      console.log(
        `RequestWrapper: Received ${this.receivedBytes} bytes of ${this.totalBytes} bytes.`
      );
    });

    this.req.on("end", () => {
      console.log("RequestWrapper: Upload complete.");
      this.#resetState();
      // res.writeHead(200, { "Content-Type": "text/plain" });
      // res.end("Upload successful!");
    });

    this.req.on("error", (err) => {
      console.error("RequestWrapper: Error occurred during upload:", err);
      this.#resetState();
      // res.writeHead(500, { "Content-Type": "text/plain" });
      // res.end("Error uploading file.");
    });

    this.req.pipe(prepared_file);
  }
  #resetState() {
    this.receivedBytes = 0;
    this.totalBytes = 0;
  }
}

exports.RequestWrapper = RequestWrapper;
