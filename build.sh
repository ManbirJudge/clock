python -m nuitka src/main.py \
    --standalone \
    --enable-plugin=tk-inter \
    --include-package=plyer \
    --include-package=just_playback \
    --include-package=cffi \
    --include-package=_cffi_backend \
    --output-dir=build \
    --lto=yes \
    --jobs=8
