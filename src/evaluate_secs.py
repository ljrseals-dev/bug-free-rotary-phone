"""Speaker-encoder cosine similarity (SECS) and related metrics.

Implements the Design 2 objective evaluation:
- SECS via ECAPA-TDNN (primary) and Resemblyzer (replication)
- MCD and F0 RMSE as secondary faithfulness measures
- The preregistered SECS<->SMOS correlation check (H2c)

UNTESTED scaffolding. Requires `speechbrain`, `resemblyzer`, `librosa` at runtime.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class SECSResult:
    mean: float
    sd: float
    n: int
    per_utterance: list[float]

    def to_dict(self) -> dict:
        return {"mean": self.mean, "sd": self.sd, "n": self.n,
                "per_utterance": self.per_utterance}


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b))


def secs_from_embeddings(ref_embs: list[np.ndarray], syn_embs: list[np.ndarray]) -> SECSResult:
    """Pairwise SECS. Assumes ref_embs[i] and syn_embs[i] are the same utterance."""
    assert len(ref_embs) == len(syn_embs), "utterance count mismatch"
    scores = [_cosine(r, s) for r, s in zip(ref_embs, syn_embs)]
    return SECSResult(
        mean=float(np.mean(scores)),
        sd=float(np.std(scores, ddof=1)) if len(scores) > 1 else 0.0,
        n=len(scores),
        per_utterance=scores,
    )


# --- encoder wrappers (thin; replace with your pinned versions) -----------

class ECAPAEncoder:
    """Primary SECS encoder. Loads a pinned SpeechBrain ECAPA-TDNN."""

    def __init__(self, source: str = "speechbrain/spkrec-ecapa-voxceleb") -> None:
        self.source = source
        self._model = None  # lazy

    def _load(self):
        if self._model is None:
            try:
                from speechbrain.inference.speaker import EncoderClassifier
            except ImportError as e:  # pragma: no cover
                raise ImportError("pip install speechbrain") from e
            self._model = EncoderClassifier.from_hparams(source=self.source)
        return self._model

    def embed(self, wav: np.ndarray, sr: int = 16000) -> np.ndarray:
        import torch
        model = self._load()
        if sr != 16000:
            raise ValueError("resample to 16 kHz before embedding")
        wav_t = torch.tensor(wav, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            emb = model.encode_batch(wav_t).squeeze().cpu().numpy()
        return emb


class ResemblyzerEncoder:
    """Replication SECS encoder."""

    def __init__(self) -> None:
        self._enc = None

    def _load(self):
        if self._enc is None:
            try:
                from resemblyzer import VoiceEncoder
            except ImportError as e:  # pragma: no cover
                raise ImportError("pip install resemblyzer") from e
            self._enc = VoiceEncoder()
        return self._enc

    def embed(self, wav: np.ndarray, sr: int = 16000) -> np.ndarray:
        if sr != 16000:
            raise ValueError("resample to 16 kHz before embedding")
        return self._enc.embed_utterance(wav)


# --- H2c correlation check -------------------------------------------------

def secs_smos_correlation(secs: list[float], smos: list[float]) -> dict:
    """Preregistered decision rule: r < 0.6 => SECS insufficient alone."""
    from scipy.stats import pearsonr, spearmanr
    assert len(secs) == len(smos) >= 3
    r_p, p_p = pearsonr(secs, smos)
    r_s, p_s = spearmanr(secs, smos)
    return {
        "pearson_r": float(r_p), "pearson_p": float(p_p),
        "spearman_r": float(r_s), "spearman_p": float(p_s),
        "h2c_supported": bool(r_p >= 0.6),
        "interpretation": (
            "SECS is a sufficient proxy for SMOS"
            if r_p >= 0.6
            else "SECS is INSUFFICIENT alone — report as a limitation"
        ),
    }


# --- report writer ---------------------------------------------------------

def write_report(path: str | Path, payload: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    # Synthetic smoke test with random embeddings (does NOT validate the encoders).
    rng = np.random.default_rng(0)
    ref = [rng.normal(size=192) for _ in range(12)]
    syn = [r + rng.normal(scale=0.1, size=192) for r in ref]
    res = secs_from_embeddings(ref, syn)
    print(f"SECS smoke test: mean={res.mean:.3f} sd={res.sd:.3f} n={res.n}")

    secs_scores = [res.mean + rng.normal(scale=0.02) for _ in range(10)]
    smos_scores = [3.0 + 2.0 * (s - min(secs_scores)) / (max(secs_scores) - min(secs_scores) + 1e-9)
                   for s in secs_scores]
    print(secs_smos_correlation(secs_scores, smos_scores))
