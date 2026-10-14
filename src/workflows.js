export const WORKFLOWS = {
  "grant": {
    "title": "项目申报 · Grant Agent",
    "steps": [
      {
        "id": "intake",
        "title": "材料清点",
        "skill": "research-intake",
        "intent": "识别指南模板和研究基础，列出缺口"
      },
      {
        "id": "template",
        "title": "要求映射",
        "skill": "grant-template",
        "intent": "把模板章节及考核条件映射到输入材料"
      },
      {
        "id": "content",
        "title": "研究内容",
        "skill": "grant-research-content",
        "intent": "形成研究目标和关键科学问题，不补造团队成果"
      },
      {
        "id": "route",
        "title": "技术路线",
        "skill": "grant-technical-route",
        "intent": "建立目标、方法和指标对应关系"
      },
      {
        "id": "audit",
        "title": "综合审查",
        "skill": "grant-review",
        "intent": "报告约束、引用、科学性及结构风险"
      }
    ]
  },
  "paper": {
    "title": "论文写作 · Paper Agent",
    "steps": [
      {
        "id": "intake",
        "title": "材料审查",
        "skill": "research-intake",
        "intent": "分类事实、假说、数据和缺失信息"
      },
      {
        "id": "outline",
        "title": "IMRAD大纲",
        "skill": "paper-drafting",
        "intent": "用提供的研究资料组织论文论证结构"
      },
      {
        "id": "evidence",
        "title": "主张核验",
        "skill": "claim-audit",
        "intent": "定位每项结论依赖的来源和数据"
      },
      {
        "id": "polish",
        "title": "专业表达",
        "skill": "academic-humanizer",
        "intent": "去掉套话而不改变术语、数字与限定条件"
      },
      {
        "id": "review",
        "title": "模拟审查",
        "skill": "paper-review",
        "intent": "提出方法、结果、统计和写作的审阅清单"
      }
    ]
  },
  "patent": {
    "title": "技术交底 · Patent Agent",
    "steps": [
      {
        "id": "intake",
        "title": "技术事实",
        "skill": "research-intake",
        "intent": "收集技术领域和待核实的发明事实"
      },
      {
        "id": "questions",
        "title": "发明人追问",
        "skill": "patent-disclosure",
        "intent": "识别必须由发明人回答的问题"
      },
      {
        "id": "draft",
        "title": "交底书框架",
        "skill": "patent-disclosure",
        "intent": "组织技术问题、技术方案与实施例"
      },
      {
        "id": "diagram",
        "title": "附图结构",
        "skill": "diagram",
        "intent": "根据已确认技术事实描述附图节点与箭头"
      },
      {
        "id": "audit",
        "title": "专业审核",
        "skill": "claim-audit",
        "intent": "检查实施细节和证据，明确非法律审查"
      }
    ]
  },
  "figures": {
    "title": "科研图表 · Figure Agent",
    "steps": [
      {
        "id": "type",
        "title": "图表类型",
        "skill": "data-figure",
        "intent": "区分数据图、可编辑流程图和生成式示意图"
      },
      {
        "id": "facts",
        "title": "科学关系",
        "skill": "claim-audit",
        "intent": "冻结研究对象、因果关系及禁止新增内容"
      },
      {
        "id": "prompt",
        "title": "可执行绘图规格",
        "skill": "nano-banana-figure",
        "intent": "生成科学图像的提示词和人工复核表，不假装已出图"
      },
      {
        "id": "audit",
        "title": "投稿核对",
        "skill": "claim-audit",
        "intent": "检查数据、文字标记和科学事实"
      }
    ]
  },
  "closeout": {
    "title": "项目结题 · Closeout Agent",
    "steps": [
      {
        "id": "intake",
        "title": "成果清单",
        "skill": "research-intake",
        "intent": "提取任务书要求与现有成果资料"
      },
      {
        "id": "map",
        "title": "指标映射",
        "skill": "research-closeout",
        "intent": "形成指标、成果、证据逐项对照"
      },
      {
        "id": "draft",
        "title": "结题草稿",
        "skill": "research-closeout",
        "intent": "依据可核对材料撰写结题摘要"
      },
      {
        "id": "audit",
        "title": "最终审查",
        "skill": "claim-audit",
        "intent": "标记缺少证据的完成承诺"
      }
    ]
  }
};
