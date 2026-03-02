# 文案标注格式指南

本文档说明如何在 txt 文案中添加标注，让 LLM 导演**保留你的创作意图**。

---

## 快速上手

| 标注类型 | 语法 | 示例 |
|---------|------|------|
| 图片/视频 | `[文件名.扩展名]` | `[cyber_cat.png]` |
| 特效描述 | `{特效：描述}` | `{特效：光效闪烁}` |
| 画面段落 | `【画面】...` | 见下方 |
| 配音段落 | `【配音】...` | 见下方 |

---

## 1. 图片/视频标注

### 语法
```
[文件名.扩展名]
```

### 支持的扩展名
- 图片：`.png` `.jpg` `.jpeg` `.gif` `.webp`
- 视频：`.mp4` `.mov` `.avi`

### 示例
```
凭空画出一只赛博朋克猫 [cyber_cat.png]
播放一段演示视频 [demo.mp4]
展示对比图 [before.jpg] 和 [after.jpg]
```

### LLM 输出
```json
{
  "visual": {
    "type": "image",
    "source": "assets/manual/cyber_cat.png"
  }
}
```

### 文件放置
标注的文件需要放在 `项目目录/assets/manual/` 下：
```
my_project/
├── assets/
│   └── manual/
│       ├── cyber_cat.png    ← 你的图片
│       └── demo.mp4         ← 你的视频
└── script.txt
```

---

## 2. 特效标注

### 语法
```
{特效：描述}
{特效:描述}   # 冒号支持中英文
```

### 示例
```
屏幕上闪烁公式 {特效：头上闪烁公式 P(Y|X)}
魔法画笔发光 {特效：光效闪烁}
数据流动 {特效：粒子从左到右流动}
```

### LLM 输出
```json
{
  "visual": {
    "effect": "光效闪烁"
  }
}
```

### 说明
- 特效字段目前会被保留到 JSON 中
- 后续版本将支持自动生成特效动画

---

## 3. 画面/配音分离

### 语法
```
【画面】
这里是画面描述，不会被读出来
【/画面】

【配音】
这里是配音文本，会被 TTS 朗读
```

### 示例
```
=== 第一幕 ===

【画面】
屏幕左边出现一台"垃圾分类机" [cat_dog.jpg]
右边出现一支"魔法画笔" {特效：光效闪烁}
【/画面】

【配音】
大家好，今天我们来聊聊生成式AI。
什么是生成式模型？
```

### 效果
- 【画面】部分：LLM 会根据描述设计视觉元素，但不会生成语音
- 【配音】部分：会被拆分成多个场景，由 TTS 朗读

---

## 4. 完整示例

### 输入文件 `generative_ai.txt`

```
=== 第一幕：什么是生成式模型？ ===

【画面】
屏幕左边出现一台"垃圾分类机"（机械臂快速识别并分拣猫和狗）{特效：头上闪烁公式 P(Y∣X)} [cat_dog.jpg]
右边出现一支"魔法画笔" {特效：光效闪烁}，凭空画出一只赛博朋克猫 [cyber_cat.png]
【/画面】

【配音】
大家都在聊大模型、AI画画，这背后的核心主角，其实叫"生成式模型"。

有人会问，这和以前的AI有什么区别？

说人话：以前的传统AI是个"分类员"（判别式模型），你给它一万张图，它负责找出哪张是猫。

而生成式模型是个"创作家"，它能凭空"捏造"出世界上原本不存在的全新内容。

=== 第二幕：大语言模型 LLM ===

【画面】
展示 ChatGPT / Gemini / 通义千问 的 logo [llm_logos.png]
【/画面】

【配音】
不管是你每天用的 ChatGPT、Gemini，还是国内的通义千问、豆包——

它们本质都是 LLM，大语言模型。
```

### 运行命令

```bash
python -m parser.annotated_converter generative_ai.txt -o script.json --avatar
```

### 期望输出

```json
[
  {
    "id": "01_title_1",
    "text": "",
    "visual": {
      "type": "title_card",
      "prompt": "第一幕：什么是生成式模型？\nChapter 1: What is Generative Model?"
    },
    "avatar": {"mode": "hidden"}
  },
  {
    "id": "02_classifier",
    "text": "",
    "visual": {
      "type": "image",
      "source": "assets/manual/cat_dog.jpg",
      "effect": "头上闪烁公式 P(Y∣X)",
      "prompt": "garbage classification machine"
    },
    "avatar": {"mode": "hidden"}
  },
  {
    "id": "03_creator",
    "text": "",
    "visual": {
      "type": "image",
      "source": "assets/manual/cyber_cat.png",
      "effect": "光效闪烁",
      "prompt": "magic paintbrush drawing cyberpunk cat"
    },
    "avatar": {"mode": "hidden"}
  },
  {
    "id": "04_intro",
    "text": "大家都在聊大模型、AI画画，这背后的核心主角，其实叫生成式模型。",
    "visual": {
      "type": "solid_bg",
      "prompt": "生成式模型",
      "color": "#0d1b2a"
    },
    "avatar": {"mode": "pip_br"}
  },
  {
    "id": "05_question",
    "text": "有人会问，这和以前的AI有什么区别？",
    "visual": {
      "type": "solid_bg",
      "prompt": "区别？"
    },
    "avatar": {"mode": "pip_br"}
  }
]
```

---

## 5. 注意事项

### 文件命名
- 文件名只能包含：字母、数字、下划线、连字符、点
- 避免空格和中文文件名（可能导致路径问题）
- 推荐命名：`cyber_cat.png`、`demo-01.mp4`

### 标注位置
- 图片标注 `[xxx.png]` 可以放在句子任意位置
- 特效标注 `{特效：xxx}` 建议紧跟在相关描述后面
- 一行可以包含多个标注

### 标注冲突
如果同一行既有图片标注又有 AI 生图提示：
```
展示一个 {特效：粒子效果} 的 [my_image.png] 场景
```
→ 图片标注优先，使用 `my_image.png`，特效会被保留

### 画面段落
- 【画面】段落的内容**不会被朗读**
- 如果想让画面描述被读出来，放到【配音】段落
- 可以省略 `【/画面】` 结束标签，遇到 `【配音】` 会自动结束

---

## 6. 快速模板

复制此模板开始创作：

```
=== 视频标题 ===

【画面】
场景描述 [your_image.png] {特效：你想要的效果}
【/画面】

【配音】
这里是配音文本，会被拆分成多个场景。

每一段会成为一个独立的场景。

可以自然分段，LLM 会智能拆分。
```
