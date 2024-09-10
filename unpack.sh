#!/bin/bash

VERBOSE=0
RECURSIVE=0
ARCHIVES_DECOMPRESSED=0
FILES_SKIPPED=0
EXIT_STATUS=0

usage() {
  echo "Usage: $0 [-r] [-v] file [file...]"
  echo "-r - will traverse contents of folders recursively, performing unpack on each."
  echo "-v - echo each file decompressed & warn for each file that was NOT decompressed"
}

while getopts "vr" OPTION; do
  case $OPTION in
    v) VERBOSE=1 ;;
    r) RECURSIVE=1 ;;
    *) usage; exit 1 ;;
  esac
done

shift $((OPTIND-1))

if [ $# -lt 1 ]; then
  usage
  exit 1
fi

overwrite_check() {
  local output_file=$1
  if [ -f "$output_file" ]; then
    if [ $VERBOSE -eq 1 ]; then
      echo "File $output_file exists, overwriting."
    fi
    rm -f "$output_file"
  fi
}

decompress_file() {
  local file=$1
  local file_type=$(file -b "$file")
  local file_name

  case "$file_type" in
    *gzip*)
      file_name=$(basename "$file" .gz)
      overwrite_check "$file_name"
      gunzip -c "$file" > "$file_name"
      ;;
    *bzip2*)
      file_name=$(basename "$file" .bz2)
      overwrite_check "$file_name"
      bunzip2 -c "$file" > "$file_name"
      ;;
    *Zip*)
      unzip -o "$file" > /dev/null
      ;;
    *compress*)
      file_name=$(basename "$file" .Z)
      overwrite_check "$file_name"
      uncompress -c "$file" > "$file_name"
      ;;
    *)
      FILES_SKIPPED=$((FILES_SKIPPED + 1))
      if [ $VERBOSE -eq 1 ]; then
        echo "Ignoring $file (not an archive)"
      fi
      EXIT_STATUS=1
      return 1
      ;;
  esac

  ARCHIVES_DECOMPRESSED=$((ARCHIVES_DECOMPRESSED + 1))
  
  if [ $VERBOSE -eq 1 ]; then
    echo "Unpacked $file"
  fi

  if [ $RECURSIVE -eq 1 ] && [ -f "$file_name" ]; then
    decompress_file "$file_name"
  fi

  return 0
}

unpack_directory() {
  local dir=$1
  for entry in "$dir"/*; do
    if [ -d "$entry" ]; then
      if [ $RECURSIVE -eq 1 ]; then
        unpack_directory "$entry"
      fi
    else
      decompress_file "$entry"
    fi
  done
}

for file in "$@"; do
  if [ -d "$file" ]; then
    if [ $RECURSIVE -eq 1 ]; then
      unpack_directory "$file"
    else
      FILES_SKIPPED=$((FILES_SKIPPED + 1))
      if [ $VERBOSE -eq 1 ]; then
        echo "$file is a directory, skipping."
      fi
    fi
  else
    decompress_file "$file"
  fi
done


echo "Decompressed $ARCHIVES_DECOMPRESSED archive(s)"
if [ $FILES_SKIPPED -gt 0 ]; then
  echo "Skipped $FILES_SKIPPED file(s)"
fi

exit $EXIT_STATUS
