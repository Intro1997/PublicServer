# file uploader

## 说明

跨端上传文件用。

```
.
├── HttpWrapper.js（包装 request 和 response，所有的错误处理，进度显示在这里完成）
├── README.md
├── UploadFileServer.js（所有的服务器功能实现放在这里）
├── index.css
├── index.html
├── index.js
├── package.json
├── received_files (上传的所有文件存储在这里，不支持归类文件)
│   └── text_uploaded.txt（上传的文本存放在这里，重新上传会覆盖之前的信息）
└── tool.js
```

1. 暂时可用，不显示文件上传进度
2. 没有使用样式文件

## 使用方法

参考 index.js 中的示例：

```js
const { UploadFileServer } = require("./UploadFileServer");

const server_host = "your.server.host.address";
const server_port = 8080;
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
```

之后运行 `npm start` 