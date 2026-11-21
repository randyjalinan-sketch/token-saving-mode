# Aturan hemat token

## Pilih model
- Haiku: cari file, baca, ringkas, format, ganti nama.
- Sonnet: kode rutin, analisis standar, tulisan formal.
- Opus: arsitektur, bug yang sulit, keputusan berisiko.
- Pakai versi terbaru dari tiap keluarga (Haiku 5.5, Sonnet 5.5, Opus 5.5).

## Pilih effort
- low: satu langkah, cari, format, ganti nama.
- medium: default untuk kode dan tulisan biasa.
- high: bug yang berulang, rancangan, perubahan lintas banyak file.
- max: hanya jika diminta secara eksplisit.

## Sub-agent
- Jika menjalankan lebih dari satu sub-agent, semuanya memakai model Haiku.
- Sonnet atau Opus hanya untuk agen utama.

## Cache lock
- Hasil riset, keputusan, dan lokasi file yang penting disimpan dengan
  `python3 /home/user/.claude/hooks/cache_lock.py put <nama> <sumber> <hasil>`.
- Sebelum mencari ulang, cek dengan `cache_lock.py get <nama> <sumber>`. Jika ada hasilnya, pakai itu.
- Hasil lama tidak terpakai otomatis jika isi sumbernya berubah, karena kuncinya memakai hash isi.

## PDF
- Membaca PDF dikonversi otomatis ke Markdown oleh hook `pdf_guard.py`, lalu disimpan di cache.
- Baca file .md yang ditunjuk oleh pesan hook. Jangan membaca ulang PDF-nya.
