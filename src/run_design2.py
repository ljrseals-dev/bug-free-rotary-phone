"""Design 2 driver: build manifest, run Z0/L10/L20/L30/F30, evaluate SECS.
Refuses to run without a signed consent record for the speaker."""
import argparse, json, subprocess, sys
from pathlib import Path

def require_consent(speaker_dir: Path, tier: int) -> None:
    rec = speaker_dir / "consent.json"
    if not rec.exists():
        sys.exit(f"BLOCKED: no consent.json in {speaker_dir}. Run is not permitted.")
    d = json.loads(rec.read_text())
    for k in ("signed", "date", "release_tier", "speaker_id"):
        if k not in d:
            sys.exit(f"BLOCKED: consent.json missing field {k!r}")
    if not d["signed"]:
        sys.exit("BLOCKED: consent.json signed=false")
    if d["release_tier"] < tier:
        sys.exit(f"BLOCKED: consent tier {d['release_tier']} < required {tier}")
    print(f"consent OK: speaker={d['speaker_id']} tier={d['release_tier']} date={d['date']}")

def build_manifest(speaker_dir: Path, out: Path, n_clips: int = 3) -> None:
    import soundfile as sf
    clips = sorted(speaker_dir.glob("*.wav"))
    if len(clips) < n_clips + 1:
        sys.exit(f"need >= {n_clips + 1} wavs, found {len(clips)}")
    ref = clips[0]
    rd = sf.info(str(ref)); ref_dur = rd.frames / rd.samplerate
    lines = []
    for c in clips[1:1 + n_clips]:
        txt = c.with_suffix(".txt")
        lines.append({"audio": str(c.resolve()),
                      "text": txt.read_text().strip() if txt.exists() else "",
                      "ref_audio": str(ref.resolve()), "ref_duration": ref_dur})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(l) for l in lines))
    print(f"manifest: {out} ({len(lines)} lines, ref={ref.name})")

def train(manifest: Path, out_dir: Path, lora: bool, rank: int = 16, epochs: int = 3) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = {"pretrained_path": "openbmb/VoxCPM1.5", "sample_rate": 44100,
           "use_lora": lora, "lora_rank": rank, "lora_alpha": rank * 2,
           "epochs": epochs, "batch_size": 16, "lr": 2e-4, "max_batch_tokens": 8192,
           "train_manifest": str(manifest)}
    (out_dir / "train_config.json").write_text(json.dumps(cfg, indent=2))
    print(f"[{'LoRA' if lora else 'full FT'}] config -> {out_dir}/train_config.json")
    print(f"   run: python scripts/train_voxcpm_finetune.py --config_path {out_dir}/train_config.json")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--speaker-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("outputs/d2"))
    p.add_argument("--tier", type=int, default=1)
    a = p.parse_args()
    require_consent(a.speaker_dir, a.tier)
    a.out.mkdir(parents=True, exist_ok=True)
    m = a.out / "manifest.jsonl"
    build_manifest(a.speaker_dir, m)
    for dur, n in ((10, 1), (20, 2), (30, 3)):
        sub = a.out / f"L{dur}"
        build_manifest(a.speaker_dir, sub / "manifest.jsonl", n_clips=n)
        train(sub / "manifest.jsonl", sub / "adapter", lora=True)
    train(m, a.out / "F30", lora=False)
    print("\nnext: src/evaluate_secs.py on outputs/d2/*/audio/")
