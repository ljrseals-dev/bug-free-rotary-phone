"""Demographic-Anatomical Conditioning Adapter (DACA).

Implements the conditioning mechanism for Design 1: a small FiLM adapter that
modulates frozen text-encoder hidden states using demographic vectors and a
vocal-tract-length proxy.

Maps to US12614539B1's "trained AI model predicts additional acoustic parameter
adjustments based on demographic, anatomical, content, and environment factors."

UNTESTED scaffolding.
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


class DACA(nn.Module):
    """FiLM adapter over frozen encoder states."""

    def __init__(self, hidden_size: int, cfg: DACAConfig) -> None:
        super().__init__()
        self.cfg = cfg
        in_dim = cfg.age_dim + cfg.gender_dim + cfg.dialect_dim + cfg.vtl_dim

        layers: list[nn.Module] = []
        d = in_dim
        for _ in range(cfg.n_layers):
            layers += [nn.Linear(d, cfg.hidden_dim), nn.GELU(), nn.Dropout(cfg.dropout)]
            d = cfg.hidden_dim
        self.trunk = nn.Sequential(*layers)
        self.to_film = nn.Linear(cfg.hidden_dim, 2 * hidden_size)

        # Zero-init the final projection so the adapter starts as identity.
        nn.init.zeros_(self.to_film.weight)
        nn.init.zeros_(self.to_film.bias)

    def forward(self, hidden: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
        """
        hidden: (B, T, H) frozen encoder states
        cond:   (B, in_dim) conditioning vector
        returns: (B, T, H) modulated states
        """
        z = self.trunk(cond)                 # (B, hidden)
        film = self.to_film(z)               # (B, 2H)
        gamma, beta = film.chunk(2, dim=-1)  # each (B, H)
        gamma = 1.0 + gamma                  # identity at init
        return hidden * gamma.unsqueeze(1) + beta.unsqueeze(1)


class ConditioningEncoder(nn.Module):
    """Turns raw demographic fields into the DACA conditioning vector.

    Deliberately simple: embeddings for categorical fields, a normalized scalar
    for the vocal-tract-length proxy. Callers are responsible for normalization.
    """

    def __init__(self, cfg: DACAConfig) -> None:
        super().__init__()
        self.age = nn.Embedding(8, cfg.age_dim)
        self.gender = nn.Embedding(4, cfg.gender_dim)
        self.dialect = nn.Embedding(64, cfg.dialect_dim)
        self.vtl = nn.Linear(1, cfg.vtl_dim)

    def forward(
        self,
        age_id: torch.Tensor,
        gender_id: torch.Tensor,
        dialect_id: torch.Tensor,
        vtl: torch.Tensor,
    ) -> torch.Tensor:
        return torch.cat(
            [
                self.age(age_id),
                self.gender(gender_id),
                self.dialect(dialect_id),
                self.vtl(vtl.unsqueeze(-1)).squeeze(-1),
            ],
            dim=-1,
        )


def sanity_check() -> None:
    cfg = DACAConfig()
    B, T, H = 4, 50, 192
    hidden = torch.randn(B, T, H)
    cond = torch.randn(B, cfg.age_dim + cfg.gender_dim + cfg.dialect_dim + cfg.vtl_dim)

    daca = DACA(hidden_size=H, cfg=cfg)
    out = daca(hidden, cond)

    assert out.shape == hidden.shape
    # At init, DACA should be (near) identity.
    assert torch.allclose(out, hidden, atol=1e-5), "adapter is not identity at init"
    n_params = sum(p.numel() for p in daca.parameters())
    print(f"DACA sanity check passed | params={n_params:,} (target ~2M)")

    enc = ConditioningEncoder(cfg)
    c = enc(
        age_id=torch.tensor([0, 1, 2, 3]),
        gender_id=torch.tensor([0, 1, 0, 1]),
        dialect_id=torch.tensor([5, 6, 7, 8]),
        vtl=torch.tensor([0.5, -0.5, 0.1, -0.1]),
    )
    print(f"Conditioning vector shape: {tuple(c.shape)}")


if __name__ == "__main__":
    sanity_check()
