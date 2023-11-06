const fs = require("fs")
const server = require("./server.js")

// main_page and html_folds must under the docs_folder
const gl_docs = {
  main_page: "index.html",
  docs_folder: "docs/htdocs",
  html_folds: [
    "el3",
    "es2",
    "es3",
    "gl2",
    "gl3",
    "gl4",
    "sl4"]
}

function StartServer(main_page, docs_folder, html_folds) {
  if (!fs.existsSync(docs_folder)) {
    console.error(`file ${docs_folder} not exist`)
  }

  for (let i = 0; i < html_folds.length; i++) {
    if (!fs.existsSync(docs_folder + "/" + html_folds[i])) {
      console.error(`file ${docs_folder + "/" + html_folds[i]} not exist`)
      return;
    }
  }

  const base_folder = __dirname + "/" + docs_folder
  const docs_server = new server.Server(main_page, docs_folder, html_folds)
  docs_server.start(20481)
}

StartServer(gl_docs.main_page, gl_docs.docs_folder, gl_docs.html_folds);
