sources=(
  "https://downloads.tatoeba.org/exports/sentences_detailed.tar.bz2"
  "https://downloads.tatoeba.org/exports/sentences_base.tar.bz2"
  "https://downloads.tatoeba.org/exports/links.tar.bz2"
  "https://downloads.tatoeba.org/exports/tags.tar.bz2"
  "https://downloads.tatoeba.org/exports/sentences_with_audio.tar.bz2"
  "https://downloads.tatoeba.org/exports/user_languages.tar.bz2"
)

mkdir -p data-tatoeba
cd data-tatoeba || exit 1

for source in "${sources[@]}"; do
  echo "Downloading ${source}..."
  curl -o archive.tar.bz "$source"
  echo "Unpacking..."
  tar --extract --bzip2 --file archive.tar.bz
  rm archive.tar.bz
done
