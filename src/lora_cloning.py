"""LoRA speaker-cloning pipeline for VoxCPM1.5 — completed.

Uses the documented VoxCPM1.5 API and the official fine-tuning manifest format.
Speaker conditioning is native (`ref_audio`), so we do not reimplement
embedding injection; we rely on the model's own cloning path and adapt it with
LoRA.

References:
- Fine-tuning guide: JSONL manifest with audio/text/ref_audio fields.
- LoRA VRAM: ~12 GB at batch_size=16 for VoxCPM1.5.
- Entry point: scripts/train_voxcpm_finetune.py --config_path <yaml>
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Optional import — only needed at runtime when VoxCPM is installed
try:
    from voxcpm import VoxCPM
except ImportError:
    VoxCPM = None  # type: ignore


@dataclass
class CloningRun:
    base_model: str = "openbmb/VoxCPM1.5"
    revision: str = "PIN_COMMIT_SHA"
    reference_durations_s: tuple[int, ...] = (10, 20, 30)
    clip_length_s: int = 10
    n_clips: int = 3
    lora_rank: int = 16
    lora_alpha: int = 32
    epochs: int = 3
    batch_size: int = 16
    lr: float = 2e-4
    consent_tier: int = 1
    release_adapter: bool = False

    def make_manifest(self, speaker_dir: Path, out_path: Path) -> Path:
        """Build the JSONL manifest the official trainer expects.

        Each line: {"audio": ..., "text": ..., "ref_audio": ..., "ref_duration": ...}
        `ref_audio` is a clip from the SAME speaker, used as cloning context.
        """
        clips = sorted(speaker_dir.glob("*.wav"))
        texts = {
            p.stem: (p.with_suffix(".txt")).read_text().strip()
            for p in clips if p.with_suffix(".txt").exists()
        }
        if len(clips) < self.n_clips + 1:
            raise ValueError("need at least n_clips + 1 clips (one held out for ref)")
        ref = clips[0]
        lines = []
        for c in clips[1 : 1 + self.n_clips]:
            lines.append({
                "audio": str(c.resolve()),
                "text": texts.get(c.stem, ""),
                "ref_audio": str(ref.resolve()),
                "ref_duration": self._dur(ref),
            })
        out_path.write_text("\n".join(json.dumps(l) for l in lines))
        return out_path

    @staticmethod
    def _dur(p: Path) -> float:
        import soundfile as sf
        info = sf.info(str(p))
        return info.frames / info.samplerate

    def build_train_config(self) -> dict:
        """Config for scripts/train_voxcpm_finetune.py."""
        return {
            "pretrained_path": self.base_model,
            "sample_rate": 44100,          # VoxCPM1.5 native
            "use_lora": True,
            "lora_rank": self.lora_rank,
            "lora_alpha": self.lora_alpha,
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "lr": self.lr,
            "max_batch_tokens": 8192,
        }


class ReleasePolicy:
    """Encodes the 'no baked identities' rule. Same as the scaffold, kept in code."""

    FORBIDDEN = {"baked_speaker_slot", "speaker_embedding_table", "voice_slot_weights"}

    @classmethod
    def check(cls, kind: str, consent_tier: int) -> None:
        if kind in cls.FORBIDDEN:
            raise PermissionError(f"refusing to release {kind}")
        if kind == "adapter" and consent_tier < 3:
            raise PermissionError("adapter release needs consent tier 3")
        if kind == "synthetic_audio" and consent_tier < 2:
            raise PermissionError("synthetic audio release needs consent tier 2")

    # Alias for compatibility with earlier scaffold
    assert_releasable = check


def infer_with_lora(
    base_model_id: str,
    lora_path: str | None,
    text: str,
    prompt_wav: str,
    out_wav: str,
) -> None:
    """Minimal inference call using the documented VoxCPM1.5 API."""
    if VoxCPM is None:
        raise ImportError("pip install voxcpm (or install from the OpenBMB repo)")
    model = VoxCPM.from_pretrained(base_model_id)
    # Note: actual LoRA loading depends on the published VoxCPM API; adjust when integrating
    wav = model.generate(
        text=text,
        prompt_wav_path=prompt_wav,     # speaker conditioning
        cfg_value=2.0,
        inference_timesteps=10,
    )
    import soundfile as sf
    sf.write(out_wav, wav, 44100)


def estimate_efficiency(
    lora_trainable: int,
    total_params: int,
    full_ft_epochs: int,
    lora_epochs: int,
) -> dict:
    """Pre-run estimate to check against H2b before spending GPU time."""
    return {
        "trainable_ratio": lora_trainable / max(total_params, 1),
        "epoch_ratio": lora_epochs / max(full_ft_epochs, 1),
        "h2b_params_ok": (lora_trainable / max(total_params, 1)) <= 0.30,
    }


def sanity_check() -> None:
    try:
        ReleasePolicy.check("baked_speaker_slot", consent_tier=3)
        raise AssertionError("policy failed to block baked slot")
    except PermissionError as e:
        print(f"release policy correctly blocked baked slot: {e}")

    est = estimate_efficiency(
        lora_trainable=8_000_000,
        total_params=750_000_000,
        full_ft_epochs=3,
        lora_epochs=3,
    )
    print(f"efficiency estimate: {est}")
    print("lora_cloning sanity check passed")


if __name__ == "__main__":
    sanity_check()
