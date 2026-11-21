# Mod penghemat token untuk Claude Code

Isi:
- `CLAUDE.md`: aturan pilihan model, effort, sub-agent (Haiku), cache lock, dan PDF.
- `.claude/settings.json`: hook PDF, pemotongan output, dan status line.
- `.claude/hooks/`: skrip Python untuk hook tersebut.

Dependensi: `python3` dan `pdftotext` (paket `poppler-utils`).

Pemasangan di cloud: pastikan repositori ini dipilih saat membuat sesi, dan tambahkan
`apt-get install -y poppler-utils` ke setup script environment.
