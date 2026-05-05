# Source and citation notes

## Selected paper

**Let ViT Speak: Generative Language-Image Pre-training**  
Yan Fang, Mengcheng Lan, Zilong Huang, Weixian Lei, Yunqing Zhao, Yujie Zhong, Yingchen Yu, Qi She, Yao Zhao, Yunchao Wei.  
ArXiv preprint: `arXiv:2605.00809`.

Primary URLs:

- arXiv abstract: https://arxiv.org/abs/2605.00809
- arXiv PDF: https://arxiv.org/pdf/2605.00809
- Official project page: https://yanfangcs.github.io/vitspeak/
- Official code: https://github.com/YanFangCS/GenLIP
- Official model collection: https://huggingface.co/collections/YanFang/genlip
- Hugging Face paper page: https://huggingface.co/papers/2605.00809

## Why this paper

Chosen on 2026-05-05 as a recent high-signal multimodal/generative model paper. It is about vision encoders for multimodal LLMs, and its core idea is easy to show visually: train a ViT with an autoregressive language objective, then deploy it as the MLLM vision encoder.

## Claims used in the video

Source-grounded claims used in narration/visuals:

- GenLIP trains a Vision Transformer to predict language tokens directly from image patches using a standard language modeling objective.
- The framework emphasizes a single Transformer, a single next-token prediction loss, and no extra text Transformer/decoder in the pretraining stack.
- Stage-one pretraining uses Recap-DataComp-1B for 8B samples at fixed resolution.
- Stage-two adaptation uses native aspect ratios and keeps visual patches between 16 and 1024.
- Official project page reports GenLIP-g/16 with Qwen2.5-7B reaches 73.6 ALL AVG and is +4.7 over SigLIP2-g/16 in the same setting.
- Official project page reports GenLIP-g/16 Doc/OCR average of 63.5 in the Qwen2.5-7B frozen visual representation setting.
- Caveat: this is an arXiv preprint; downstream results depend on the surrounding MLLM/projector/evaluation setup.

## BibTeX from project page

```bibtex
@article{fang2026letvitspeakgenerative,
 title={Let ViT Speak: Generative Language-Image Pre-training},
 author={Yan Fang and Mengcheng Lan and Zilong Huang and Weixian Lei and Yunqing Zhao and Yujie Zhong and Yingchen Yu and Qi She and Yao Zhao and Yunchao Wei},
 journal={arXiv preprint arXiv:2605.00809},
 year={2026}
}
```
