import {GRANT_STEPS} from './grant.js';
export const WORKFLOWS = {
  "grant": {
    "title": "项目申报",
    "steps": [
      {
        "id": "intake",
        "title": "材料清点",
        "skill": "research-intake",
        "intent": "对照指南、模板和已有研究资料，列出还缺哪些信息。"
      },
      {
        "id": "template",
        "title": "核对申报要求",
        "skill": "grant-template",
        "intent": "逐项检查指南要求，确认现有材料可以支撑哪些章节和指标。"
      },
      {
        "id": "content",
        "title": "研究内容",
        "skill": "grant-research-content",
        "intent": "根据已有材料整理研究目标、研究内容和需要回答的问题。"
      },
      {
        "id": "route",
        "title": "技术路线",
        "skill": "grant-technical-route",
        "intent": "说明各项目标如何研究、采用什么方法，以及怎样检查结果。"
      },
      {
        "id": "audit",
        "title": "检查申报草稿",
        "skill": "grant-review",
        "intent": "检查草稿是否回应指南，指出需要补充依据或修改的地方。"
      }
    ]
  },
  "paper": {
    "title": "论文写作",
    "steps": [
      {
        "id": "intake",
        "title": "材料审查",
        "skill": "research-intake",
        "intent": "分清已有事实、研究假说和数据，找出还缺哪些资料。"
      },
      {
        "id": "outline",
        "title": "整理论文结构",
        "skill": "paper-drafting",
        "intent": "按引言、方法、结果和讨论组织内容，检查论点是否连贯。"
      },
      {
        "id": "evidence",
        "title": "核对结论与证据",
        "skill": "claim-audit",
        "intent": "逐项找出支持结论的数据和出处，标明仍需核实的内容。"
      },
      {
        "id": "polish",
        "title": "修改表述",
        "skill": "academic-humanizer",
        "intent": "修改空话和难懂的句子，保留术语、数字、引用和适用条件。"
      },
      {
        "id": "review",
        "title": "检查论文草稿",
        "skill": "paper-review",
        "intent": "从方法、统计、论证和写作几个方面，列出需要修改的问题。"
      }
    ]
  },
  "patent": {
    "title": "专利交底",
    "steps": [
      {
        "id": "intake",
        "title": "技术事实",
        "skill": "research-intake",
        "intent": "整理技术要解决的问题和已有方案，分清哪些事实已经确认。"
      },
      {
        "id": "questions",
        "title": "发明人追问",
        "skill": "patent-disclosure",
        "intent": "列出影响理解或实施方案的疑问，交给发明人补充。"
      },
      {
        "id": "draft",
        "title": "整理交底内容",
        "skill": "patent-disclosure",
        "intent": "把技术问题、方案、部件关系和实施方式整理成文。"
      },
      {
        "id": "diagram",
        "title": "整理附图关系",
        "skill": "diagram",
        "intent": "根据已确认的方案，整理附图中应有的部件、连接和流程。"
      },
      {
        "id": "audit",
        "title": "检查交底草稿",
        "skill": "claim-audit",
        "intent": "检查方案是否讲清楚，指出缺少的参数、实施细节和证据。"
      }
    ]
  },
  "figures": {
    "title": "科研图表",
    "steps": [
      {
        "id": "type",
        "title": "图表类型",
        "skill": "data-figure",
        "intent": "根据任务选择数据图、流程图或概念示意图。"
      },
      {
        "id": "facts",
        "title": "整理科学关系",
        "skill": "claim-audit",
        "intent": "明确研究对象及其关系，标出尚未证实或不能自行添加的内容。"
      },
      {
        "id": "prompt",
        "title": "写清绘图要求",
        "skill": "nano-banana-figure",
        "intent": "写出图中应有的对象、关系、文字和排版要求，供后续绘图使用。"
      },
      {
        "id": "audit",
        "title": "检查图表",
        "skill": "claim-audit",
        "intent": "逐项核对数据、标注和科学关系，并检查投稿格式要求。"
      }
    ]
  },
  "closeout": {
    "title": "项目结题",
    "steps": [
      {
        "id": "intake",
        "title": "成果清单",
        "skill": "research-intake",
        "intent": "整理任务书要求和已有成果，记录各份资料的出处。"
      },
      {
        "id": "map",
        "title": "核对指标与成果",
        "skill": "research-closeout",
        "intent": "把每项指标与对应成果、证明资料放在一起核对。"
      },
      {
        "id": "draft",
        "title": "结题草稿",
        "skill": "research-closeout",
        "intent": "根据已有材料撰写结题摘要，保留尚未完成或缺少证据的事项。"
      },
      {
        "id": "audit",
        "title": "检查结题材料",
        "skill": "claim-audit",
        "intent": "检查完成情况是否有依据，列出提交前需要补齐的材料。"
      }
    ]
  }
};

WORKFLOWS.grant.steps=GRANT_STEPS;
