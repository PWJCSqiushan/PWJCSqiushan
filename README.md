<div align="right">

**中文** · [English](README_EN.md)

</div>

<p align="center">
  <img src="./assets/banner.svg" width="100%" alt="Qiu Shan — Code, Camera, Kilometers">
</p>

<p align="center">
  <a href="#featured-work"><img alt="代表项目" src="https://img.shields.io/badge/代表项目-查看项目-AF85B9?style=for-the-badge"></a>
  <a href="#tech-stack"><img alt="技术栈" src="https://img.shields.io/badge/技术栈-Tools_&_Stack-668099?style=for-the-badge"></a>
  <a href="#github-data"><img alt="GitHub 数据" src="https://img.shields.io/badge/GitHub_数据-动态更新-CFA2B0?style=for-the-badge"></a>
  <a href="https://github.com/PWJCSqiushan/PWJCSqiushan/issues/new?template=say-hello.yml"><img alt="留言交流" src="https://img.shields.io/badge/留言交流-Say_Hello-8D6A9F?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="https://github.com/PWJCSqiushan"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-PWJCSqiushan-181717?style=flat-square&logo=github"></a>
  <a href="mailto:dongzongyue@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-dongzongyue%40gmail.com-8D6A9F?style=flat-square&logo=gmail&logoColor=white"></a>
  <img alt="Location" src="https://img.shields.io/badge/Location-Jilin%2C_China-5B7088?style=flat-square&logo=googlemaps&logoColor=white">
</p>

## 你好，我是丘山

吉林大学软件工程专业大二在读，长期进行 vibe coding、程序设计竞赛、数学建模、计算机视觉、嵌入式等领域的学习和研究。
同时，我热爱摄影创作和中长跑，并在持续学习使用 达芬奇、light room、PR、PS 等工具进行影像的后期处理工作。

我希望自己不仅仅在完成课程与比赛，而是不断积累完整项目的设计、开发和迭代经验。
目前，我主要关注的领域有 AI 应用、计算机视觉、全栈产品与智能交互，我也在尝试把软件开发能力用于解决摄影、学习和训练中的实际问题。

| <code>CODE / 工程</code> | <code>CAMERA / 影像</code> | <code>KILOMETERS / 长跑</code> |
|:---|:---|:---|
| AI 应用、计算机视觉、全栈产品、嵌入式交互 | 活动与人像摄影、后期工作流、创作者工具 | 路跑、越野跑、训练计划与数据复盘 |

<a name="featured-work"></a>

## 代表项目 · Featured Work

### 01 / [FurColor Studio](https://github.com/PWJCSqiushan/FurColor-Studio) <code>ACTIVE</code>

面向兽聚摄影的本地优先 AI 批量后期工作站。当前 v4.1 已将选片、主体检测与匿名分组、人脸隐私复核、参考样片驱动调色、主体分层曝光、眼睛蒙版、人工质检和可校验交付串成完整流程。

- <code>Python</code> <code>FastAPI</code> <code>OpenCV</code> <code>YuNet</code> <code>YOLO</code> <code>Computer Vision</code>
- 融合主体框、人脸检测与人工记忆，同时保留人工隐私复核
- v4.1 增加可选账户、会话安全与服务器隔离边界
- 交付前检查隐私、蒙版、曝光与颜色、水印与裁切

[查看项目说明与完整工作流 →](https://github.com/PWJCSqiushan/FurColor-Studio#readme)

---

### 02 / [Mirage Mane 1.0](https://github.com/PWJCSqiushan/Mirage-Mane) <code>TEACHING PROTOTYPE</code>

面向理发教学的本地优先 3D 头发操作网页。项目以浏览器实时性能为边界，验证从头模与发束建模到抓发、梳理、剪切、推剪、造型和教学截图的一整套交互。

- <code>React</code> <code>Three.js</code> <code>Vite</code> <code>WebGL</code> <code>Local-first</code>
- 使用“导向簇 + 高密度显示发丝”兼顾固定发根、等长约束与实时操作
- 支持空间剪刀、电动推子、梳子、吹风机与多种造型工具
- 教学项目保存在浏览器本地，并用模型与交互烟雾测试覆盖关键行为

[查看功能、操作说明与建模边界 →](https://github.com/PWJCSqiushan/Mirage-Mane#readme)

---

### 03 / [Higgs](https://github.com/PWJCSqiushan/Higgs) <code>ACTIVE</code>

面向个人长期使用的自托管 QQ 智能体。项目围绕“稳定人格、可信记忆、主人权限和受控自动化”构建可持续运行、可审计、可停止和可回滚的智能交互系统。

- <code>Python</code> <code>SQLite</code> <code>OneBot</code> <code>WebSocket</code> <code>AI Agent</code>
- 通过 NapCat / OneBot 支持私聊、白名单群、自然触发群与引用消息
- 使用候选、隔离、激活状态机管理长期记忆，并结合向量召回与主人审核
- 在 QQ 内提供白名单、触发词、回复频率、运行开关、记忆状态和即时备份治理
- 坚持权限与记忆分离、人格核心不自我漂移以及高风险工具默认拒绝

[查看架构、安全模型与阶段文档 →](https://github.com/PWJCSqiushan/Higgs#readme)

## 其他项目 · More Projects

| 项目 | 主要内容 | 技术与定位 |
|---|---|---|
| **[Mirage Mane V2](https://github.com/PWJCSqiushan/Mirage-Mane-V2)**<br>3D 美发教学工作台 | 以真实头模、教学点线、头发分区和发片图层构建多用户、项目隔离的美发教学空间 | <code>TypeScript</code> <code>Three.js</code> <code>Cloudflare D1</code><br>多用户教学产品 |
| **[JKS](https://github.com/PWJCSqiushan/JKS)**<br>智能语音交互助手 | 串联桌面端录音、STT、智能体、TTS 与 ESP32-S3 圆形 AMOLED 表情反馈 | <code>Python</code> <code>C++</code> <code>ESP32-S3</code><br>软硬件交互原型 |
| **[Starflare Codex Pet](https://github.com/PWJCSqiushan/starflare-codex-pet)**<br>自定义 Codex 宠物 | 制作并修复符合 Codex v2 规范的 8×11 动画精灵图，包含完整校验与透明边缘清理 | <code>Sprite Animation</code> <code>Codex Pet v2</code><br>角色资产 |
| **[StockHub](https://github.com/PWJCSqiushan/stockhub)**<br>影像素材平台 | 完成创作者上传、EXIF 展示、用户、订单、下载和管理后台等业务链路，探索个人影像作品展示与交易方式 | <code>Next.js</code> <code>TypeScript</code> <code>Prisma</code><br>全栈产品原型 |
| **[chaoxing-fanya](https://github.com/PWJCSqiushan/chaoxing-fanya)**<br>超星学习通自动化工具 | 在开源项目基础上继续开发，补充 Web 可视化、OCR、题库接入、通知和便携打包能力 | <code>Python</code> <code>Flask</code> <code>React</code><br>开源二次开发 |

<details>
<summary><strong>展开项目档案 / Project archive</strong></summary>

| 项目 | 一句话说明 |
|---|---|
| [chaoxing-quiz-pdf](https://github.com/PWJCSqiushan/chaoxing-quiz-pdf) | 抓取、整理题目并生成可打印 PDF 的学习资料工具 |
| [hospital-management-system](https://github.com/PWJCSqiushan/hospital-management-system) | 使用 C/C++ 实现完整门诊业务流程的课程设计项目 |
| [media-marketplace](https://github.com/PWJCSqiushan/media-marketplace) | StockHub 之前用于验证产品流程的纯前端原型 |
| [cloudflare-edgetunnel-v2rayn-guide](https://github.com/PWJCSqiushan/cloudflare-edgetunnel-v2rayn-guide) | 根据实际部署与排障过程整理的网络配置指南 |

</details>

<a name="current-route"></a>

## 当前方向 · Current Focus

- 项目工程：继续推进 FurColor Studio 的真实场景验证、安全边界与交付可靠性
- 3D 交互：推进 Mirage Mane V2 的多用户项目空间、教学图层与触控体验，并持续完善实时 3D 教学工具
- 智能交互：推进 Higgs 的长期记忆治理，并继续探索语音智能体、嵌入式显示和 Codex 自定义交互资产
- 专业基础：系统学习 C++ 程序设计竞赛、算法、计算机系统与数学建模
- 影像与训练：持续完善摄影后期工作流，并用阶段复盘指导长跑训练，为不同年龄段体适能教育提供专业化指导建议

<a name="tech-stack"></a>

## 技术栈与工具 · Tech Stack

以下内容综合了已经在项目中使用的技术，以及现阶段重点学习和补强的方向。

<p align="center">
  <strong>Languages</strong><br><br>
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,cpp,ts,js,matlab&theme=dark&perline=5" alt="Python, C++, TypeScript, JavaScript and MATLAB">
  </a>
</p>

<p align="center">
  <strong>AI · Web · Data</strong><br><br>
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=opencv,fastapi,flask,react,nextjs,threejs,vite,tailwind,sqlite,prisma&theme=dark&perline=10" alt="OpenCV, FastAPI, Flask, React, Next.js, Three.js, Vite, Tailwind CSS, SQLite and Prisma">
  </a>
</p>

<p align="center">
  <strong>Engineering · Creative</strong><br><br>
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=git,github,docker,linux,powershell,vscode,ps,pr&theme=dark&perline=8" alt="Git, GitHub, Docker, Linux, PowerShell, VS Code, Photoshop and Premiere">
  </a>
</p>

<a name="github-data"></a>

## GitHub 数据 · Development Activity

<p align="center">
  <img width="96%" src="https://ghchart.rshah.org/AF85B9/PWJCSqiushan" alt="PWJCSqiushan 过去一年的 GitHub 贡献记录">
</p>

<p align="center">
  <a href="https://github.com/PWJCSqiushan?tab=repositories">
    <img height="170" src="./assets/github-overview.svg" alt="PWJCSqiushan GitHub 公开项目与贡献统计">
  </a>
  <a href="https://github.com/PWJCSqiushan?tab=repositories&type=source">
    <img height="170" src="./assets/top-languages.svg" alt="PWJCSqiushan 公开仓库常用语言占比">
  </a>
</p>

<sub>贡献热力图展示过去一年的 GitHub 公开活动；统计卡片更新于 2026-08-03，语言占比按非 Fork 公开仓库的代码体积统计。</sub>

## 个人方向 · Beyond Development

- 📷 持续进行拍摄活动、人像与视频拍摄、后期剪辑与调色处理，并将真实的需求转化为软件功能
- 🏃 参加路跑、越野跑与高校中长跑赛事，重视训练计划和赛后复盘
- 📚 推进程序设计竞赛、数学竞赛、数学建模等的长期学习

## 联系与交流 · Connect

如果你对 **AI 与影像、3D 交互、创作者工具、智能硬件或开源协作** 感兴趣，欢迎：

- [公开留言或提出合作想法](https://github.com/PWJCSqiushan/PWJCSqiushan/issues/new?template=say-hello.yml)
- [浏览全部仓库](https://github.com/PWJCSqiushan?tab=repositories)
- [发送邮件](mailto:dongzongyue@gmail.com)
