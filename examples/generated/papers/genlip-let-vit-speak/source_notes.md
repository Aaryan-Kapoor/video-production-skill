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

## Video remake notes

Remade on 2026-05-04 as a 5:55 technical lecture rather than a short promotional showcase. The new cut follows this arc:

1. Objective mismatch in CLIP/SigLIP-style contrastive vision pretraining for MLLMs.
2. GenLIP's key design: a single transformer trained with direct next-token language supervision.
3. Mechanism: image patches -> visual-prefix sequence -> Prefix-LM attention -> text-only NTP loss.
4. Gated attention and attention-sink caveat.
5. Two-stage training pipeline and model scales.
6. Frozen LLaVA-NeXT evaluation protocol.
7. Main results with exact SigLIP2 baselines and deltas.
8. Same-budget ablations, data scaling, and discriminative-feature checks.
9. Limitations and practical takeaway.

## Claims used in narration/visuals

Source-grounded claims used in the video:

- GenLIP trains a Vision Transformer to predict language tokens directly from image patches using a standard autoregressive language modeling objective, without contrastive batch construction or an additional text decoder.
- The input sequence is visual tokens followed by text tokens: `S = [v0, ..., vM, t0, ..., tL]`.
- Prefix-LM attention lets image tokens attend bidirectionally while text tokens attend causally to image and previous text.
- The language modeling loss is applied exclusively to text tokens; at deployment the tokenizer and LM head are discarded and the visual features are projected into the MLLM.
- Full mixed-modality attention can create an attention sink where the first visual token absorbs most attention; gated attention is introduced to improve convergence and preserve spatially distributed features.
- Stage 1 pretraining uses Recap-DataComp-1B at 224x224 for 8.0B samples; Stage 2 adapts on 37M long-caption samples from BLIP3o-Long-Caption and Infinity-MM with native aspect ratios and 16-1024 visual tokens.
- Reported model scales are GenLIP-L/16 (~0.3B), GenLIP-So/16 (~0.4B), and GenLIP-g/16 (~1.1B).
- In Table 4's Qwen2.5-7B frozen setting, SigLIP2-g/16 reports 68.9 ALL AVG and GenLIP-g/16 reports 73.6 ALL AVG, a +4.7 point delta.
- In Table 3's Qwen2.5-1.5B frozen setting, SigLIP2-g/16 reports 61.5 ALL AVG and GenLIP-g/16 reports 65.2 ALL AVG, a +3.7 point delta.
- The paper reports Doc&OCR average gains over SigLIP2 of +4.3, +3.3, and +5.9 points at L/16, So/16, and g/16 scales.
- Under the controlled 2.0B-sample ablation in Table 7, GenLIP-So/16 reports 44.2 OCR average and 55.2 General VQA average, ahead of the controlled SigLIP and OpenVision2 runs.
- Table 8 reports GenLIP w/o gated attention at 76.2 ImageNet-1K top-1; gated GenLIP-g/16 reports 85.2 ImageNet-1K top-1 and 44.5 ADE20K mIoU.
- The limitations section states that validation is in an academic-scale LLaVA-NeXT setup, larger-scale behavior remains unverified, and high-quality captions create data acquisition cost.
- Appendix A describes remaining OCR/detail failure modes: long numbers, tiny text, and precise spatial layouts.

## Source figures/tables used or recreated

- Actual source crop: Figure 1 GenLIP architecture comparison / “Ours” panel.
- Actual source crop: Figure 3 attention sink thumbnail, paired with a recreated readable bar plot.
- Actual source crop: Figure 6 data scaling plots.
- Actual source crop: Table 4 excerpt thumbnail, paired with extracted exact values.
- Recreated chart: SigLIP2-g/16 vs GenLIP-g/16 ALL AVG for Qwen2.5-1.5B and 7B frozen settings.
- Recreated chart: controlled 2.0B-sample Table 7 OCR and General VQA averages.
- Recreated mechanism diagram: image patches -> ViT/prefix-LM sequence -> LM-head next-token loss -> deployment as frozen vision encoder.

## BibTeX

```bibtex
@article{fang2026letvitspeakgenerative,
 title={Let ViT Speak: Generative Language-Image Pre-training},
 author={Yan Fang and Mengcheng Lan and Zilong Huang and Weixian Lei and Yunqing Zhao and Yujie Zhong and Yingchen Yu and Qi She and Yao Zhao and Yunchao Wei},
 journal={arXiv preprint arXiv:2605.00809},
 year={2026}
}
```
