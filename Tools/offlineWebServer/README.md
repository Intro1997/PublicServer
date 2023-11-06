## 说明

由于 docs.gl 提供的离线版本，其 API 描述所在 html 文件名没有提供 html 后缀，导致 chrome 跳转到该文件的时候不显示网页，因此需要在 server 端修改 content-type 来完成。考虑到这可能是一个通用的行为，因此这里提供一个通用 server 工具来完成这个事情

工具以 docs.gl 本地启动为例，使用 nodejs 来完成启动服务

## 文件结构

```
.
├── README.md
├── tool.js             存放 http 相关工具
├── package.json
├── server.js           server class 负责启动/停止服务器
├── start_server.js     使用 server 启动服务，在这里配置离线 docs 资源
└── update_docs.js      负责更新 docs 资源
```

## 使用

start_server.js 中修改 gl_docs 属性

```js
const gl_docs = {
  main_page: "index.html", // 离线文档主页
  docs_folder: "docs/htdocs",
  // 文件夹内只有 html 文件，并且这些 html 文件的均没有后缀
  html_folds: ["el3", "es2", "es3", "gl2", "gl3", "gl4", "sl4"],
};

// start 传入服务端口
docs_server.start(20481);
```

update_docs.js 中配置获取离线文档的压缩包链接：

1. 默认下载并解压到 docs 目录：
2. 若存在 docs 目录，则递归删除 docs 后创建 docs 目录
3. 解压完成后删除压缩包文件

启动服务输入以下命令：

```
npm install
npm run update_docs
npm run start
```
