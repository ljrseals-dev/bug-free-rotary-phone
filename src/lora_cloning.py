"""LoRA speaker-cloning scaffolding for Design 2.

Ports the *method* of mlx-audio-train Pipeline 2 (speaker embedding injected as a
positional token in the codec prefix; LoRA rank 16; 3 epochs) to a generic
PyTorch/transformers-style base model. The actual VoxCPM1.5 integration must be
written against its published API; this file defines the pieces.

UNTESTED scaffolding.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch
import torch.nn as nn


@dataclass
class LoRAConfig:
    rank: int = 16
    alpha: int = 32
    dropout: float = 0.05
    target_modules: list[str] = field(
        default_factory=lambda: ["attn.q", "attn.k", "attn.v", "attn.o", "mlp.fc1", "mlp.fc2"]
    )


def count_trainable(model: nn.Module) -> tuple[int, int]:
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    return trainable, total


class SpeakerPrefixInjector(nn.Module):
    """Injects a speaker embedding as a positional token in the codec prefix.

    This is the method element adopted from mlx-audio-train Pipeline 2. The
    injector does not modify base weights; it prepends a learned projection of
    the speaker embedding to the prefix sequence.
    """

    def __init__(self, speaker_embed_dim: int, model_hidden_dim: int) -> None:
        super().__init__()
        self.proj = nn.Linear(speaker_embed_dim, model_hidden_dim)
        self.scale = nn.Parameter(torch.tensor(1.0))

    def forward(self, prefix: torch.Tensor, speaker_emb: torch.Tensor) -> torch.Tensor:
        """
        prefix:      (B, T_prefix, H)
        speaker_emb: (B, D)
        returns:     (B, T_prefix + 1, H)
        """
        token = self.proj(speaker_emb).unsqueeze(1) * self.scale
        return torch.cat([token, prefix], dim=1)


@dataclass
class TrainingPlan:
    epochs: int = 3
    batch_size: int = 16
    lr: float = 2e-4
    grad_clip: float = 1.0
    reference_durations_s: tuple[int, ...] = (10, 20, 30)


def build_training_plan() -> TrainingPlan:
    return TrainingPlan()


def estimate_efficiency(lora_trainable: int, total_params: int, full_ft_epochs: int, lora_epochs: int) -> dict:
    """Pre-run estimate to check against H2b before spending GPU time."""
    return {
        "trainable_ratio": lora_trainable / max(total_params, 1),
        "epoch_ratio": lora_epochs / max(full_ft_epochs, 1),
        "h2b_params_ok": (lora_trainable / max(total_params, 1)) <= 0.30,
    }


# --- Release policy enforcement -------------------------------------------

class ReleasePolicy:
    """Encodes the 'never release baked identities' rule as code."""

    FORBIDDEN_ARTIFACTS = {"baked_speaker_slot", "speaker_embedding_table", "voice_slot_weights"}

    @classmethod
    def assert_releasable(cls, artifact_kind: str, consent_tier: int) -> None:
        if artifact_kind in cls.FORBIDDEN_ARTIFACTS:
            raise PermissionError(
                f"Refusing to release '{artifact_kind}'. Baked speaker identities are "
                "never released, regardless of consent tier."
            )
        if artifact_kind == "adapter" and consent_tier < 3:
            raise PermissionError("Adapter release requires consent tier 3.")
        if artifact_kind == "synthetic_audio" and consent_tier < 2:
            raise PermissionError("Synthetic demo audio release requires consent tier 2.")


def sanity_check() -> None:
    inj = SpeakerPrefixInjector(speaker_embed_dim=192, model_hidden_dim=1024)
    prefix = torch.randn(2, 8, 1024)
    emb = torch.randn(2, 192)
    out = inj(prefix, emb)
    assert out.shape == (2, 9, 1024), out.shape
    print("speaker prefix injector sanity check passed")

    try:
        ReleasePolicy.assert_releasable("baked_speaker_slot", consent_tier=3)
        raise AssertionError("policy failed to block baked slot")
    except PermissionError as e:
        print(f"release policy correctly blocked baked slot: {e}")

    est = estimate_efficiency(lora_trainable=8_000_000, total_params=750_000_000,
                              full_ft_epochs=3, lora_epochs=3)
    print(f"efficiency estimate: {est}")


if __name__ == "__main__":
    sanity_check()
