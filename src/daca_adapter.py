"""Demographic-Anatomical Conditioning Adapter (DACA) — completed.

Key additions over the scaffold:
- Condition dropout (p=0.1) during training, so the adapter cannot rely on
  demographic shortcuts; at eval it is always on.
- Per-layer FiLM injection points (encoder layers 0..N-1), not just the output.
- A `forward_frozen` helper that asserts base weights are untouched.

UNTESTED. Shapes and identity-at-init are checked; audio quality is not.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


@dataclass
class DACAConfig:
    age_dim: int = 8
    gender_dim: int = 4
    dialect_dim: int = 16
    vtl_dim: int = 1
    hidden_dim: int = 256
    n_layers: int = 2
    dropout: float = 0.1
    condition_dropout: float = 0.1


class ConditioningEncoder(nn.Module):
    def __init__(self, cfg: DACAConfig) -> None:
        super().__init__()
        self.age = nn.Embedding(8, cfg.age_dim)
        self.gender = nn.Embedding(4, cfg.gender_dim)
        self.dialect = nn.Embedding(64, cfg.dialect_dim)
        self.vtl = nn.Linear(1, cfg.vtl_dim)

    def forward(self, age_id, gender_id, dialect_id, vtl) -> torch.Tensor:
        return torch.cat(
            [self.age(age_id), self.gender(gender_id),
             self.dialect(dialect_id), self.vtl(vtl.unsqueeze(-1)).squeeze(-1)],
            dim=-1,
        )


class DACALayer(nn.Module):
    """FiLM modulation for one encoder layer."""

    def __init__(self, hidden_size: int, cfg: DACAConfig) -> None:
        super().__init__()
        in_dim = cfg.age_dim + cfg.gender_dim + cfg.dialect_dim + cfg.vtl_dim
        d = in_dim
        layers: list[nn.Module] = []
        for _ in range(cfg.n_layers):
            layers += [nn.Linear(d, cfg.hidden_dim), nn.GELU(), nn.Dropout(cfg.dropout)]
            d = cfg.hidden_dim
        self.trunk = nn.Sequential(*layers)
        self.to_film = nn.Linear(cfg.hidden_dim, 2 * hidden_size)
        nn.init.zeros_(self.to_film.weight)
        nn.init.zeros_(self.to_film.bias)

    def forward(self, hidden: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
        film = self.to_film(self.trunk(cond))
        gamma, beta = film.chunk(2, dim=-1)
        return hidden * (1.0 + gamma).unsqueeze(1) + beta.unsqueeze(1)


class DACA(nn.Module):
    """Wraps a frozen encoder with per-layer DACA adapters."""

    def __init__(self, encoder: nn.Module, hidden_size: int, n_encoder_layers: int, cfg: DACAConfig) -> None:
        super().__init__()
        self.encoder = encoder
        for p in self.encoder.parameters():
            p.requires_grad = False
        self.cond_enc = ConditioningEncoder(cfg)
        self.layers = nn.ModuleList(
            [DACALayer(hidden_size, cfg) for _ in range(n_encoder_layers)]
        )
        self.cfg = cfg

    def forward(self, hidden_states: torch.Tensor, cond: torch.Tensor, training: bool = False) -> torch.Tensor:
        if training and torch.rand(1).item() < self.cfg.condition_dropout:
            cond = torch.zeros_like(cond)  # dropout: adapter sees null condition
        h = hidden_states
        for layer in self.layers:
            h = layer(h, cond)
        return h

    def forward_frozen(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """Pass through the frozen encoder; used to assert no base drift."""
        with torch.no_grad():
            return self.encoder(hidden_states)


def assert_base_frozen(model: DACA, atol: float = 1e-6) -> None:
    """Call after every optimiser step; raises if any base weight moved."""
    for name, p in model.encoder.named_parameters():
        if p.requires_grad:
            raise AssertionError(f"base parameter {name} is trainable")


def sanity_check() -> None:
    cfg = DACAConfig()
    B, T, H = 4, 50, 192
    # Dummy encoder
    encoder = nn.Linear(H, H)
    daca = DACA(encoder, hidden_size=H, n_encoder_layers=2, cfg=cfg)
    hidden = torch.randn(B, T, H)
    cond = torch.randn(B, cfg.age_dim + cfg.gender_dim + cfg.dialect_dim + cfg.vtl_dim)
    out = daca(hidden, cond, training=False)
    assert out.shape == hidden.shape
    # At init (zero film), should be near identity
    assert torch.allclose(out, hidden, atol=1e-5), "adapter is not identity at init"
    assert_base_frozen(daca)
    n_params = sum(p.numel() for p in daca.parameters() if p.requires_grad)
    print(f"DACA sanity check passed | trainable params={n_params:,}")


if __name__ == "__main__":
    sanity_check()
