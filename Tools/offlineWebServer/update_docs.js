const extract = require("extract-zip")
const https = require("https")
const fs = require("fs")
const { exit } = require("process")
const ProgressBar = require('progress')

const save_path = "./docs"
const doc_download_address = "https://docs.gl/docs.gl.zip"
const download_filename = "docs.gl.zip"

if (fs.existsSync(save_path)) {
  fs.rmSync(save_path, { recursive: true, force: true })
}

fs.mkdirSync(save_path)
if (!fs.existsSync(save_path)) {
  console.error(`create ${save_path} failed`)
  exit()
}

const docs_zip_path = `${save_path}/${download_filename}`;
let total_bytes = 0

const file = fs.createWriteStream(docs_zip_path);
console.log(`Connecting ${doc_download_address} ...`)
https.get(doc_download_address, function (res) {
  console.log(`Downloading ${doc_download_address} to ${docs_zip_path}`)
  const bar = new ProgressBar('-> downloading [:bar] :percent :etas', {
    width: 40,
    complete: '=',
    incomplete: ' ',
    renderThrottle: 1,
    total: parseInt(res.headers['content-length'])
  })
  res.on("data", (chunk) => {
    file.write(chunk);
    bar.tick(chunk.length)
  })

  res.on("end", () => {
    file.close();
    console.log("Download Completed");
    console.log(`Unzip to ${save_path}`)
    // unzip
    try {
      extract(docs_zip_path, { dir: __dirname + "/" + save_path }).then(() => {
        console.log(`Uzip success, remove file ${docs_zip_path}`)
        fs.rmSync(docs_zip_path)
      })
    }
    catch (err) {
      console.error(`Unzip failed: ${err}`)
    }

  });
  file.on("error", () => {
    fs.unlink(dest);
    console.error(`Download ${doc_download_address} failed`)
  })

});