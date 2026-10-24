"""Differentiable bone-conduction simulation.

Approximates the low-frequency emphasis and harmonic excitation described in
US12614539B1 as a "frequency shift to compensate for bone-conducted
low-frequency adjustment."

Design notes
------------
- A first-order low-shelf filter provides the low-frequency gain.
- Harmonic excitation adds energy at F0 multiples below the cutoff, which is the
  perceptual signature of bone conduction in the literature.
- Three parameters are learned: shelf cutoff, shelf gain, harmonic mix.

UNTESTED scaffolding. Validate against a reference acoustics implementation
before using in any perceptual study.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torchaudio


class BoneConductionSim(nn.Module):
    def __init__(
        self,
        sample_rate: int = 22050,
        init_cutoff_hz: float = 350.0,
        init_gain_db: float = 6.0,
        init_harmonic_mix: float = 0.15,
        n_harmonics: int = 4,
    ) -> None:
        super().__init__()
        self.sample_rate = sample_rate
        self.n_harmonics = n_harmonics

        # Learned parameters (bounded via sigmoid/tanh reparameterization).
        self._cutoff = nn.Parameter(torch.tensor(init_cutoff_hz))
        self._gain_db = nn.Parameter(torch.tensor(init_gain_db))
        self._mix = nn.Parameter(torch.tensor(init_harmonic_mix))

    # ---- bounded parameter views -------------------------------------
    @property
    def cutoff_hz(self) -> torch.Tensor:
        return 150.0 + 600.0 * torch.sigmoid(self._cutoff / 200.0)

    @property
    def gain_db(self) -> torch.Tensor:
        return 12.0 * torch.tanh(self._gain_db / 12.0)

    @property
    def mix(self) -> torch.Tensor:
        return torch.sigmoid(self._mix)

    # ---- forward ------------------------------------------------------
    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        """waveform: (B, T) or (B, 1, T). Returns same shape."""
        squeeze = waveform.dim() == 2
        if squeeze:
            waveform = waveform.unsqueeze(1)

        shelf = self._low_shelf(waveform)
        harm = self._harmonic_excitation(waveform)
        out = shelf + self.mix * harm

        return out.squeeze(1) if squeeze else out

    def _low_shelf(self, x: torch.Tensor) -> torch.Tensor:
        """First-order low-shelf via differentiable biquad coefficients."""
        cutoff = self.cutoff_hz
        gain = self.gain_db

        # Normalized frequency; clamp for numerical stability.
        w0 = 2.0 * torch.pi * cutoff / self.sample_rate
        w0 = torch.clamp(w0, 1e-4, torch.pi - 1e-4)
        A = torch.pow(10.0, gain / 40.0)

        # Shelf slope S = 1 (standard).
        alpha = torch.sin(w0) / 2.0 * torch.sqrt(torch.tensor(2.0))
        cos_w0 = torch.cos(w0)

        b0 = A * ((A + 1) - (A - 1) * cos_w0 + 2 * torch.sqrt(A) * alpha)
        b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
        b2 = A * ((A + 1) - (A - 1) * cos_w0 - 2 * torch.sqrt(A) * alpha)
        a0 = (A + 1) + (A - 1) * cos_w0 + 2 * torch.sqrt(A) * alpha
        a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
        a2 = (A + 1) + (A - 1) * cos_w0 - 2 * torch.sqrt(A) * alpha

        b = torch.stack([b0, b1, b2]) / a0
        a = torch.stack([a0, a1, a2]) / a0

        # torchaudio expects (n_coeffs,) tensors; this is differentiable
        # in recent versions. Verify on your torchaudio build.
        return torchaudio.functional.lfilter(x, a, b, clamp=False)

    def _harmonic_excitation(self, x: torch.Tensor) -> torch.Tensor:
        """Add energy at F0 multiples below the cutoff.

        Cheap approximation: rectify-and-smooth produces low-order harmonics
        without an explicit F0 tracker. This is a deliberate simplification and
        should be replaced by an F0-conditioned version if the ablation shows it
        matters.
        """
        rectified = torch.relu(x)
        kernel_size = max(3, int(self.sample_rate / 500))
        smooth = nn.functional.avg_pool1d(
            rectified, kernel_size=kernel_size, stride=1, padding=kernel_size // 2
        )
        return smooth - x


def sanity_check() -> None:
    """Run a shape/parameter check. Not a validation of audio quality."""
    sr = 22050
    sim = BoneConductionSim(sample_rate=sr)
    x = torch.randn(2, sr) * 0.1
    y = sim(x)
    assert y.shape == x.shape, f"shape mismatch: {y.shape} vs {x.shape}"
    assert torch.isfinite(y).all(), "non-finite output"
    print("bone_conduction sanity check passed")
    print(f"  cutoff_hz={sim.cutoff_hz.item():.1f} gain_db={sim.gain_db.item():.2f} mix={sim.mix.item():.3f}")


if __name__ == "__main__":
    sanity_check()
