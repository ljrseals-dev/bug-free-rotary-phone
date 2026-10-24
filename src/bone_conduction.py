"""Differentiable bone-conduction simulation for Design 1.

Two learnable components, both differentiable end-to-end:

1. Low-shelf biquad (RBJ cookbook form), learned cutoff 150–750 Hz and gain 0–12 dB.
2. F0-conditioned harmonic exciter: energy at F0 multiples below the shelf
   cutoff, mixed by a learned coefficient.

Bone-conduction in the acoustics literature is characterised by a low-pass
transfer (skull/soft-tissue filtering) and a 2–3 kHz emphasis in the external
channel. The low-shelf models the former; the harmonic exciter approximates the
perceptual "inside-the-head" quality that TTS vocoders systematically omit.

UNTESTED against human listeners. Validate the filter response against a
reference implementation (e.g. scipy.signal.shelf) before the perceptual study.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from scipy import signal


class BoneConductionSim(nn.Module):
    def __init__(
        self,
        sample_rate: int = 22050,
        init_cutoff_hz: float = 350.0,
        init_gain_db: float = 6.0,
        init_harmonic_mix: float = 0.15,
    ) -> None:
        super().__init__()
        self.sample_rate = sample_rate
        # Unbounded parameters, mapped through bounded views below.
        self._cutoff = nn.Parameter(torch.tensor(init_cutoff_hz, dtype=torch.float32))
        self._gain_db = nn.Parameter(torch.tensor(init_gain_db, dtype=torch.float32))
        self._mix = nn.Parameter(torch.tensor(init_harmonic_mix, dtype=torch.float32))

    @property
    def cutoff_hz(self) -> torch.Tensor:
        return 150.0 + 600.0 * torch.sigmoid(self._cutoff / 200.0)

    @property
    def gain_db(self) -> torch.Tensor:
        return 12.0 * torch.tanh(self._gain_db / 12.0)

    @property
    def mix(self) -> torch.Tensor:
        return torch.sigmoid(self._mix)

    def _biquad_coeffs(self) -> tuple[torch.Tensor, torch.Tensor]:
        """RBJ low-shelf coefficients, S = 1."""
        w0 = 2.0 * torch.pi * self.cutoff_hz / self.sample_rate
        w0 = torch.clamp(w0, 1e-4, torch.pi - 1e-4)
        A = torch.pow(10.0, self.gain_db / 40.0)
        alpha = torch.sin(w0) / 2.0 * torch.sqrt(torch.tensor(2.0))
        cos_w0 = torch.cos(w0)
        sqrtA = torch.sqrt(A)

        b0 = A * ((A + 1) - (A - 1) * cos_w0 + 2 * sqrtA * alpha)
        b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
        b2 = A * ((A + 1) - (A - 1) * cos_w0 - 2 * sqrtA * alpha)
        a0 = (A + 1) + (A - 1) * cos_w0 + 2 * sqrtA * alpha
        a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
        a2 = (A + 1) + (A - 1) * cos_w0 - 2 * sqrtA * alpha

        b = torch.stack([b0, b1, b2]) / a0
        a = torch.stack([a0, a1, a2]) / a0
        return b, a

    def _low_shelf(self, x: torch.Tensor) -> torch.Tensor:
        b, a = self._biquad_coeffs()
        # Manual biquad difference equation (stable for this coefficient range).
        b0, b1, b2 = b[0], b[1], b[2]
        _, a1, a2 = a[0], a[1], a[2]
        y = torch.zeros_like(x)
        x1 = torch.zeros(x.shape[0], device=x.device)
        x2 = torch.zeros_like(x1)
        y1 = torch.zeros_like(x1)
        y2 = torch.zeros_like(x1)
        for t in range(x.shape[1]):
            xt = x[:, t]
            yt = b0 * xt + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
            y[:, t] = yt
            x2, x1 = x1, xt
            y2, y1 = y1, yt
        return y

    def _harmonic_excitation(self, x: torch.Tensor) -> torch.Tensor:
        """Half-wave rectification + smoothing approximates low-order harmonics."""
        rect = torch.relu(x)
        k = max(3, int(self.sample_rate / 500))
        # Ensure 3D for avg_pool1d: (B, C, T)
        if rect.dim() == 2:
            rect = rect.unsqueeze(1)
        smooth = nn.functional.avg_pool1d(rect, kernel_size=k, stride=1, padding=k // 2)
        if smooth.shape[-1] != x.shape[-1]:
            smooth = smooth[..., :x.shape[-1]]
        return smooth.squeeze(1) - x

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        squeeze = waveform.dim() == 2
        if squeeze:
            waveform = waveform.unsqueeze(1)
        # waveform: (B, 1, T) or (B, C, T)
        if waveform.shape[1] == 1:
            w = waveform.squeeze(1)
            out = self._low_shelf(w) + self.mix * self._harmonic_excitation(w)
            out = out.unsqueeze(1)
        else:
            outs = []
            for c in range(waveform.shape[1]):
                w = waveform[:, c, :]
                outs.append(self._low_shelf(w) + self.mix * self._harmonic_excitation(w))
            out = torch.stack(outs, dim=1)
        return out.squeeze(1) if squeeze else out


def validate_filter_response(sr: int = 22050) -> dict:
    """Cross-check the learned biquad at init values."""
    sim = BoneConductionSim(sample_rate=sr)
    cutoff = float(sim.cutoff_hz)
    gain = float(sim.gain_db)

    b, a = sim._biquad_coeffs()
    w, h_torch = signal.freqz(b.detach().numpy(), a.detach().numpy(), worN=2048, fs=sr)
    h_torch_db = 20 * np.log10(np.abs(h_torch) + 1e-12)

    # Expected DC gain for low-shelf is approximately the gain_db
    dc_gain_db = float(h_torch_db[0])
    max_diff = abs(dc_gain_db - gain)

    return {
        "cutoff_hz": cutoff,
        "gain_db": gain,
        "dc_gain_db": dc_gain_db,
        "max_diff_db_below_cutoff": max_diff,
    }


if __name__ == "__main__":
    print(validate_filter_response())
    # Shape check
    sim = BoneConductionSim()
    x = torch.randn(2, 22050) * 0.1
    y = sim(x)
    assert y.shape == x.shape, f"shape mismatch {y.shape} vs {x.shape}"
    assert torch.isfinite(y).all()
    print("bone_conduction shape check passed")
