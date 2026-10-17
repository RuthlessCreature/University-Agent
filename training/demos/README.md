# 本地文件演示

先在两仓库同级目录准备 Python 及 python-docx。此项目运行使用 Codex bundled Python（具体路径记录于 ../../STATUS.md）。

```
python training/demos/create_inputs.py
python tools/run-local-workflow.py --input training/demos/grant/grant.json --guide training/demos/grant/guide.json --template training/demos/grant/template.docx --output training/demos/grant/replay
```

grant、paper、patent各自目录包括结构化输入、模板、实际DOCX及运行日志。全部是受约束的确定性文件流水线，不是已联通LLM的自主科研Agent。Grant输入指南明确教学模拟，不是任何年度官方基金规则。论文使用公开来源和真实本地描述统计。专利是教学模拟，真实现有技术检索没有执行。

检查 Word 规定标题、文字及来源，然后检查 output/issues.json。当前正式提交应被阻止：团队基础、查新或实施参数缺失，且没有研究者人工签核。禁止用AI冒充人类批准。

```
python tools/run-local-workflow.py --input training/demos/grant/grant.json --guide training/demos/grant/guide.json --template training/demos/grant/template.docx --output training/demos/grant/final-attempt --final
```

预期退出2，run.json记录final_export_blocked。正常草稿退出0表示文件流程执行成功，不能解释为科学验收通过。测试中的审批数据仅为fixture，不是用户签核。

Figure演示：运行 training/deck-zh/src/collect_sources.py，读取真实CC0数据并复算；build.mjs构建包含原生数值的散点图。没有调用Nano Banana。云端联调需要另外注入 Secrets，不能复用本地日志冒充。
