#!/usr/bin/env bash
# Render every scene to an MP4 (720p30) and a GIF (480p15) and copy the results
# into blog/assets/ for the post. Run from the repo root or the manim/ folder.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PY="$ROOT/manimenv/bin/manim"
ASSETS="$ROOT/blog/assets"

# TeX Live provides latex + dvisvgm that Manim's MathTex needs.
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
mkdir -p "$ASSETS"

# scene_file :: SceneClass
SCENES=(
  "s01_hide_with_noise.py:HideWithNoise"
  "s02_lwe_sample_and_decrypt.py:LWESampleAndDecrypt"
  "s03_mod_clock_torus.py:ModClockTorus"
  "s04_poly_ring.py:PolyRing"
  "s05_poly_mult_rotate_reflect.py:PolyMultRotateReflect"
  "s06_keygen.py:KeyGen"
  "s07_encryption_build.py:EncryptionBuild"
  "s08_decryption_rescale_round.py:DecryptionRescaleRound"
  "s09_hom_add_noise.py:HomAddNoise"
  "s10_hom_mult_powers_of_s.py:HomMultPowersOfS"
  "s11_roots_of_unity.py:RootsOfUnity"
  "s12_modular_roots.py:ModularRoots"
  "s13_ntt_pipeline.py:NTTPipeline"
  "s14_crt_sharding.py:CRTSharding"
  "s15_lattice_cvp.py:LatticeCVP"
)

cd "$HERE"
for entry in "${SCENES[@]}"; do
  file="${entry%%:*}"
  scene="${entry##*:}"
  base="${file%.py}"
  echo "==> rendering $scene"
  "$PY" -qm --format=mp4 -o "$base" "scenes/$file" "$scene"
  "$PY" -ql --format=gif -o "$base" "scenes/$file" "$scene"
  cp "media/videos/$base/720p30/$base.mp4" "$ASSETS/$base.mp4"
  cp "media/videos/$base/480p15/$base.gif" "$ASSETS/$base.gif"
done

echo "All scenes rendered into $ASSETS"
