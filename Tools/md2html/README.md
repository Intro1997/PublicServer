## 说明

使用 [markdown-to-html-cli](https://github.com/jaywcjlove/markdown-to-html-cli) 

## 依赖

~~依赖 [showdown CLI Tool](https://github.com/showdownjs/showdown)，通过 npm 安装：~~
依赖 [markdown-to-html-cli](https://github.com/jaywcjlove/markdown-to-html-cli)

## 使用

~~md2html 是一个 node 脚本，需要提前准备 nodejs 环境。~~

~~`./md2html --help` 查看脚本支持的操作，对于 showdown config 的项目，需要修改 md2html 脚本中，convert 的 config_list 参数，以字符串的方式新增，showdown 的配置项目可以参考[这里](https://github.com/showdownjs/showdown/wiki/Showdown-Options)，或者使用 `showdown makehtml --config-help` 查看。~~

```shell
markdown-to-html markdown-to-html --source <markdown file> --output <html file>
```