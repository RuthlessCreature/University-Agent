# Section 5 文献检索、阅读与综述

24页中文讲授课件，当前修订s5-r3。内容包括检索概念与逻辑、实际检索页、检索记录、关键词／语义／引文路径、工具用途、去重与版本、筛选与全文缺失、原文阅读、两篇研究比较、综述表达、引文核验、空白反证和文献工作流。没有课堂练习。

## 交付

- output/高校科研AI课程_Section5_文献检索阅读与综述_s5-r3.pptx：可编辑课件。
- renders/s5-r3/：真实PPTX渲染PDF与24页预览。
- literature-packet/：两篇比较案例证据表、来源索引、真实试查记录与教学综述示例。
- 讲师稿.md、国外课件参考.md、材料状态与核验范围.md：逐页讲解、来源与范围。
- lesson.json、build.mjs、render.py、capture.mjs：内容、构建、渲染与公开网页截图代码。
- checks.json、validation.json、审查记录.md：检查记录，不替代教学验收。

## 来源与示例

参考UCL 2025证据综合工作坊原始PDF第14、17、43、56页。现行功能另查官方文档，Elicit按2026-09-30入口变更说明编写。PubMed试查页与Elicit帮助页为真实浏览器截图，细节版采用浏览器clip直接截取，原始整页截图保留。未使用生成模型重画页面。

两篇研究全文经Europe PMC XML实际读取，身份信息与XML中的DOI匹配；原文文件保存在忽略的参考缓存。课件仅比较其研究对象、对照和测量，不宣称完成系统综述。更正／撤稿状态检查仍列PENDING。

## 构建与检查

使用工作区bundled Node、Python和Artifact Tool。RUNTIME_NODE_MODULES与node_modules连接指向bundled包路径。首次构建按presentation技能执行操作标记一次，再运行build.mjs。新修订通过SECTION_REVISION设置，render.py和check_delivery.py接收同一修订号。LibreOffice转PDF，bundled Poppler渲染。capture.mjs访问公开网页，无需登录，不调用付费研究服务。

逐页检查最终预览后再交付。尚未在Microsoft PowerPoint或Google Slides中验证显示。本节的文件检查不证明文献Agent已经完成多数据库检索或科学核验。
