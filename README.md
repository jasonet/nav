# 网址导航（静态页面通用模板）
是使用 [GenEasy](https://github.com/geneasy/geneasy) 文档生成工具 + [WebStack](https://github.com/WebStackPage/WebStackPage.github.io) 模板创建的静态页面，托管在 GitHub Pages 服务器上面。

当修改 `links.yml` 文件里的内容时，**GitHub Actions** 会自动更新 HTML 文件。不需要服务器，不需要数据库。

## 如何在我的网站里加入这个网址导航页面？

第一步：fork 这个项目[gh-pages 分支]

第二步：进入 Settings > Pages, 启用 GitHub Pages 功能。分支选择 `gh-pages`。

第三步：2 分钟后，访问你的 GitHub Pages 域名，看看是否正常显示。`https://你的用户名.github.io/nav/`

第四步：进入 Actions，启用 Actions 功能，进入 Settings，启用 Issues 功能。

## Tips

### Tip: 如何修改 `links.yml`

把现在 GitHub repository 的 URL 里的 `github.com` 改成 `github.dev`，会进入 web 版的 VS Code。在 web 版的 VS Code 里修改提交。

## License

Copyright (c) 2025 Licensed under the MIT license.
