# Literature Comparison Matrix

> [!abstract]+ 📌 跨文献全景横向对比矩阵说明 (Matrix Description)
> 本表系统对齐了当前知识库中所有已收录文献的核心学术主张、测试方法/数据集、论证强度及主要局限性，用于跨文献横向分析与论文写作证据支撑。

| Paper | Title | Year | Core Claim | Method / Benchmark | Claim Strength | Primary Limitation |
|---|---|:---:|---|---|:---:|---|
| [[Sources/Papers/he2016deep|he2016deep]] | **Deep Residual Learning for Image Recognition** | 2016 | Residual networks reduce top-5 error on ImageNet to 3.57% with 152 layers | ImageNet classification benchmark, top-5 error rate 3.57% | `strong` | Does not resolve memory footprint scaling linearly with layer count |
| [[Sources/Papers/hu2021lora|hu2021lora]] | **LoRA: Low-Rank Adaptation of Large Language Models** | 2021 | Matches or exceeds full fine-tuning performance on GPT-3 175B with 10,000x fewer trainable parameters | GLUE benchmark, WikiSQL, SAMSum; accuracy and ROUGE scores | `strong` | Rank hyperparameter r must be empirically tuned |
| [[Sources/Papers/vaswani2017attention|vaswani2017attention]] | **Attention Is All You Need** | 2017 | Achieves 28.4 BLEU on WMT 2014 English-to-German, establishing new state-of-the-art | WMT 2014 EN-DE and EN-FR translation benchmarks, BLEU score | `strong` | O(N^2) memory footprint for long sequences |
