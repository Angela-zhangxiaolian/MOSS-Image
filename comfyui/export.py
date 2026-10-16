import argparse
import json
import shutil
from pathlib import Path

from safetensors.torch import load_file, save_file


def load_shards(directory, index_name):
    index = json.loads((directory / index_name).read_text())
    state = {}
    for filename in sorted(set(index["weight_map"].values())):
        path = (directory / filename).resolve()
        if not path.is_relative_to(directory.resolve()):
            raise ValueError("Shard path escapes the component directory")
        state.update(load_file(path))
    if state.keys() != index["weight_map"].keys():
        raise ValueError("Shard keys do not match the index")
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Exported MOSSImagePipeline directory, not a distributed training checkpoint")
    parser.add_argument("models", type=Path, help="Destination ComfyUI models directory")
    parser.add_argument("--name", default="moss-image", help="Output filename prefix for this checkpoint")
    args = parser.parse_args()
    if not args.name or Path(args.name).name != args.name or args.name in (".", ".."):
        parser.error("--name must be a filename prefix, not a path")
    config = json.loads((args.source / "transformer/config.json").read_text())
    if config.get("_class_name") not in ("MOSImageTransformer", "MOSSImageTransformer"):
        raise ValueError(f"Unsupported MOSSImage class: {config.get('_class_name')!r}")
    for key, expected in {"text_dim": 4096, "freq_dim": 256,
                          "latent_channels": 128, "rope_base": 10000.0}.items():
        if config.get(key) != expected:
            raise ValueError(f"Unsupported MOSSImage configuration: {key}={config.get(key)!r}")
    outputs = [args.models / f"diffusion_models/{args.name}-dit.safetensors",
               args.models / f"text_encoders/{args.name}-qwen35.safetensors",
               args.models / f"vae/{args.name}-vae.safetensors"]
    for path in outputs:
        if path.exists():
            raise FileExistsError(path)
    for path in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
    for component, index_name, target in [
        ("transformer", "diffusion_pytorch_model.safetensors.index.json", outputs[0]),
        ("text_encoder", "model.safetensors.index.json", outputs[1]),
    ]:
        state = load_shards(args.source / component, index_name)
        # Keep the exported values and dtype; this is packaging, not quantization.
        temporary = target.with_suffix(".partial")
        save_file(state, temporary, metadata={"format": "pt", "model": "moss-image"})
        temporary.rename(target)
        del state
    temporary = outputs[2].with_suffix(".partial")
    shutil.copyfile(args.source / "vae/diffusion_pytorch_model.safetensors", temporary)
    temporary.rename(outputs[2])


if __name__ == "__main__":
    main()
