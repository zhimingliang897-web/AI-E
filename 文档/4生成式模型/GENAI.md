# 生成式AI进化史（图像与视频全纪录）

## 1. 启蒙与理论奠基期（1960s - 2000s）
> **核心特征**：基于统计学的早期尝试，深度学习尚未普及。

### 1.1 关键理论/论文
*   **隐马尔可夫模型 (HMM)**
    *   时间：1960s
    *   内容：最早期的统计生成模型之一，主要用于语音序列处理。
*   **高斯混合模型 (GMM)**
    *   时间：1960s
    *   内容：用于数据分布拟合，体现了早期的概率生成思想。

### 1.2 关键模型/产品
*   **ELIZA**
    *   时间：1966年
    *   作者：Joseph Weizenbaum (MIT)
    *   地位：世界上第一个聊天机器人，虽然基于规则，但埋下了人机交互的种子。

---

## 2. 深度生成时代的黎明（2014 - 2016）
> **核心特征**：深度学习介入，GAN成为主角，视觉创作大门开启。

### 2.1 关键理论/论文
*   **VAE (变分自编码器)**
    *   论文：*Auto-Encoding Variational Bayes*
    *   时间：2013年12月预印本，2014年ICLR会议
    *   作者：Diederik P. Kingma, Max Welling
    *   贡献：提出了“隐空间”和“重参数化”技巧，实现了数据的高效重建与生成。
*   **GAN (生成对抗网络)**
    *   论文：*Generative Adversarial Nets*
    *   时间：2014年6月
    *   作者：Ian Goodfellow et al.
    *   贡献：提出“生成器-判别器”对抗博弈机制，开启了高保真图像生成的时代。

### 2.2 关键模型/产品
*   **DCGAN**
    *   时间：2015年
    *   贡献：首次将CNN与GAN结合，让GAN训练更稳定，生成了早期较高质量的人脸。

---

## 3. 架构革命与多模态预埋（2017 - 2019）
> **核心特征**：Transformer架构统一了序列建模范式，为后续视觉大模型奠基。

### 3.1 关键理论/论文
*   **Transformer架构**
    *   论文：*Attention Is All You Need*
    *   时间：2017年6月 (NeurIPS 2017)
    *   作者：Google Brain (Vaswani et al.)
    *   贡献：彻底改变了序列建模，成为后来GPT、ViT及多模态模型的统一基石。
*   **ViT (Vision Transformer)**
    *   论文：*An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*
    *   时间：2020年10月预印本 (ICLR 2021)
    *   作者：Google Research
    *   贡献：将Transformer架构跨界引入视觉领域（将图片切块处理），为后来的“DiT”等架构埋下伏笔。

---

## 4. 扩散模型的崛起与图像爆发（2020 - 2022）
> **核心特征**：扩散模型击败GAN，开源生态爆发，AI绘画全民化。

### 4.1 关键理论/论文

#### 4.1.1 基础扩散理论
*   **DDPM (去噪扩散概率模型)**
    *   论文：*Denoising Diffusion Probabilistic Models*
    *   时间：2019年11月预印本，2020年NeurIPS
    *   作者：Jonathan Ho et al. (Google Research)
    *   贡献：奠定了现代扩散模型的数学框架，“加噪-去噪”范式。
*   **Diffusion Models Beat GANs**
    *   论文：*Diffusion Models Beat GANs on Image Synthesis*
    *   时间：2021年5月
    *   作者：OpenAI (Prafulla Dhariwal, Alex Nichol)
    *   贡献：首次在学术上证明扩散模型生成质量超越GAN，确立扩散模型统治地位。

#### 4.1.2 高效与可控生成
*   **Classifier-Free Guidance**
    *   论文：*Classifier-Free Diffusion Guidance*
    *   时间：2022年
    *   作者：Google Research
    *   贡献：在不依赖外部分类器的情况下实现强条件控制，是现代文生图模型（如SD、MJ）采用的主流方案。
*   **Latent Diffusion Models (LDM)**
    *   论文：*High-Resolution Image Synthesis with Latent Diffusion Models*
    *   时间：2021年12月预印本，CVPR 2022
    *   作者：Rombach et al. (CompVis / RunwayML)
    *   贡献：将扩散过程置于潜空间，大幅降低计算成本，是Stable Diffusion的理论基础。

### 4.2 关键模型/产品（图像）

#### 4.2.1 国外
*   **DALL-E 1**
    *   时间：2021年1月
    *   作者：OpenAI
    *   架构：基于Transformer的自回归离散token建模（非纯扩散）。
    *   地位：首个现象级的文本生成图像模型。
*   **CLIP**
    *   时间：2021年1月
    *   作者：OpenAI
    *   地位：虽非生成模型，但提供了图文对齐能力，是所有现代生成模型的“眼睛”。
*   **DALL-E 2**
    *   时间：2022年4月
    *   作者：OpenAI
    *   架构：扩散模型 + Prior。
    *   地位：生成质量惊艳，推动AI艺术破圈。
*   **Imagen**
    *   时间：2022年5月
    *   作者：Google Research
    *   架构：大语言模型（T5） + 级联扩散模型。
    *   地位：强调“大语言模型+扩散”路线，生成质量极高。
*   **Stable Diffusion (SD)**
    *   时间：2022年8月
    *   作者：Stability AI / CompVis
    *   架构：基于Latent Diffusion Models。
    *   地位：开源神器，让AI绘画可以在消费级显卡运行，引爆社区。
*   **Midjourney**
    *   时间：2022年7月公测
    *   作者：Midjourney Research
    *   地位：艺术感最强，商业化和大众认知度最高的产品。

#### 4.2.2 国内
*   **CogView**
    *   时间：2021年 NeurIPS
    *   作者：清华大学 KEG 实验室
    *   架构：基于Transformer + VQ-VAE的自回归文生图模型。
    *   地位：国内首个大规模中文文生图模型，与国际DALL-E 1路线并行。
*   **CogView2 / CogView3**
    *   时间：CogView2 (2022), CogView3 (2024)
    *   作者：清华大学 KEG
    *   架构：CogView3采用了级联扩散模型。
    *   地位：持续迭代，为后续CogVideo打下基础。
*   **AltDiffusion**
    *   时间：2023年 arXiv
    *   作者：北京智源研究院
    *   架构：多语言扩散模型。
    *   地位：面向多语言场景，强调中文和多语言文生图。
*   **Hunyuan-DiT (混元-DiT)**
    *   时间：2024年5月
    *   作者：腾讯 Hunyuan 团队
    *   架构：Diffusion Transformer (DiT)，多分辨率训练。
    *   地位：国产DiT代表作，强调中英双语理解。

---

## 5. 视频生成的爆发与架构融合（2023 - 2025）
> **核心特征**：Transformer与Diffusion结合，视频时长与连贯性突破。

### 5.1 关键理论/论文

#### 5.1.1 视频扩散基础
*   **Video LDM**
    *   论文：*Align Your Latents: High-Resolution Video Synthesis with Latent Diffusion Models*
    *   时间：CVPR 2023
    *   作者：NVIDIA / LMU Munich
    *   贡献：将LDM扩展到视频，提出时空潜扩散。
*   **AnimateDiff**
    *   论文：*AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models*
    *   时间：ICLR 2024
    *   作者：上海人工智能实验室
    *   贡献：提出可插拔的运动模块，将任意文生图扩散模型“动画化”，显著降低门槛。

#### 5.1.2 架构创新：DiT & 流匹配
*   **DiT (Diffusion Transformer)**
    *   论文：*Scalable Diffusion Models with Transformers*
    *   时间：ICCV 2023 (2022年12月预印本)
    *   作者：William Peebles, Saining Xie
    *   贡献：用Transformer替代U-Net，具备极强的扩展性，是Sora的核心架构。
*   **Lumiere (时空扩散)**
    *   论文：*Lumiere: A Space-Time Diffusion Model for Video Generation*
    *   时间：2024年1月
    *   作者：Google Research
    *   贡献：提出Space-Time U-Net，一次性生成整个视频段，解决短视频动作不连贯问题。
*   **Rectified Flow (流匹配)**
    *   论文：*Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*
    *   时间：2022年提出，2023-2024年广泛应用
    *   作者：Qinsheng Zhang, Yongxin Chen
    *   贡献：提供比DDPM更高效的采样路径，Flux.1、SD3等模型采用的新范式。

### 5.2 关键模型/产品（视频）

#### 5.2.1 国外
*   **Gen-2**
    *   时间：2023年3月
    *   作者：Runway
    *   地位：早期视频生成商业化标杆。
*   **Sora**
    *   时间：2024年2月
    *   作者：OpenAI
    *   架构：DiT架构 + 大规模数据。
    *   地位：引爆全网，生成60秒长视频，理解物理规律。
*   **Lumiere**
    *   时间：2024年1月
    *   作者：Google Research
    *   地位：技术标杆，在时序一致性与视频质量上树立新标准。
*   **Flux.1**
    *   时间：2024年8月
    *   作者：Black Forest Labs
    *   架构：Rectified Flow + Transformer。
    *   地位：证明了新算法在图像生成上的优越性，质量超越SDXL。

#### 5.2.2 国内
*   **CogVideo**
    *   时间：2022年5月预印本，ICLR 2023
    *   作者：清华大学 KEG
    *   架构：基于CogView的自回归Transformer文生视频。
    *   地位：首个开源大规模Transformer文生视频模型之一。
*   **VideoCrafter**
    *   时间：2023年起
    *   作者：上海人工智能实验室
    *   架构：基于LDM的视频生成。
    *   地位：开源高质量视频生成工具箱。
*   **Kling (可灵)**
    *   时间：2024年6月
    *   作者：快手
    *   架构：类DiT的视频生成大模型。
    *   地位：国产视频模型标杆，高质量长视频生成，效果对标Sora。
*   **Vchitect**
    *   时间：2023-2025年
    *   作者：上海人工智能实验室
    *   架构：并行Transformer视频扩散。
    *   地位：面向高效可扩展的视频生成。

---

## 6. 全模态未来展望（2026+）
> **核心特征**：从拼接外挂到走向原生，单一模型同时处理文本、图像、音频、视频。

### 6.1 技术趋势
*   **原生多模态**
    *   解释：不再拼接独立的模型，而是统一架构、统一训练，实现真正的多模态协同生成。
    *   代表：GPT-4o的演进方向、Google Gemini的多模态迭代。
