# MOSS-Image for ComfyUI

[English](README.md) | 简体中文

moss-image 支持直接读取本地 Hugging Face / Diffusers 模型目录，提供标准
MODEL、CLIP、VAE 输出，配合 ComfyUI 原生采样、SLG 及显存管理使用。

## 安装

将 `comfyui/moss-image/` 复制到 `ComfyUI/custom_nodes/moss-image/`，重启 ComfyUI。
插件使用 ComfyUI 提供的依赖，可独立安装。

也可以在仓库根目录建立链接：

```bash
python comfyui/install.py --comfy-root /path/to/ComfyUI
```

也可以使用下方的[本地运行脚本](#本地运行)安装独立的 ComfyUI。

已有用户工作流不会被覆盖。环境、权重、生成图片和用户配置不纳入版本控制。

## 工作流

1. 下载 [moss-image.json](moss-image/example_workflows/moss-image.json)，拖入 ComfyUI。
2. 下载 [MOSS-Image-Base](https://huggingface.co/OpenMOSS-Team/MOSS-Image-Base)，在 **MOSS-Image HF Loader** 的 `model_path` 中填写本地模型目录。目录应包含 `transformer/`、`text_encoder/`、`tokenizer/` 和 `vae/`。
3. 修改正向和负向提示词，点击 **Run** 生成图片。

工作流已配置好 **50 步、CFG 3、Shift 5、负向跳过第 22 层**，
使用 Euler / sgm_uniform 采样，分辨率为 1024×1024。
提示词和采样建议见[用户指南](../USERGUIDE_ZH.md)。

## 本地运行

```bash
bash comfyui/local/setup.sh
bash comfyui/local/run.sh
```

安装脚本在目录不存在时将 ComfyUI 克隆到 Git 忽略的 `local/ComfyUI/`，
创建独立环境并安装依赖，然后安装节点和 MOSS-Image 工作流，不覆盖已有同名文件。
`MOSS_PYTHON` 指定解释器，`UV_INDEX_URL` 指定依赖源。

`COMFYUI_ROOT` 指定已有 ComfyUI，`COMFY_HOST`、`COMFY_PORT` 控制监听地址，
`CUDA_VISIBLE_DEVICES` 选择设备。默认启用 FP32 VAE、Latent2RGB 预览并关闭图片元数据写入。
运行目录的 `local/env.sh` 可配置启动选项。

## 高级设置

[API JSON](moss-image/example_workflows/moss-image-api.json) 是同一工作流的接口格式，
供程序提交使用。

加载器读取本地单文件或分片 safetensors，不会通过 Hub 仓库 ID 自动下载模型。
`weight_dtype` 控制 DiT 精度，`text_device` 控制文本编码设备，VAE 使用 FP32。
文本编码最长为 4096 tokens。

清空 Simple SLG 的 `single_layers` 可关闭负向跳层。如需改用标准 SLG，
将 Simple SLG 替换为 `SkipLayerGuidanceDiT`，选择 `single_layers`，
并设置 scale 3、start 0.01、end 1、rescaling 0，`double_layers` 留空。
用户指南尚未指定标准 SLG 的层号。

ModelSamplingSD3 保持在 SLG 前，让采样和 SLG 阈值使用同一套 Shift。
ComfyUI 的 SLG 区间采用 sigma 百分比语义。其原生 scheduler 不包含独立 pipeline
的训练网格吸附；即使 seed 和参数相同，也不保证生成相同的图片。

单独的组件加载节点仍可用于自定义工作流。模型键匹配的 LoRA 可使用内置 LoRA
加载器。TorchCompileModel 会过滤 transformer options 的编译 guard，
配合 SLG 或动态 block 补丁时请使用未编译执行。