#!/bin/bash
#
# Generate release notes from the first entry in the changelog.
#
# Usage:
#   generate-release-notes.sh [-v] [--pep] [CHANGELOG_FILE]
#
# Options:
#   -v     Print the parsed release version instead of the release notes.
#   --pep  Use PEP 440 instead of SemVer.
#
# Requirements:
#   - parse-changelog: https://github.com/taiki-e/parse-changelog
#   - jq: https://github.com/jqlang/jq
#
set -euo pipefail

abort() {
  echo "error: $*" 1>&2
  exit 1
}

changelog_file=CHANGELOG.md
print_version=false
args=()
parse_changelog_args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
  -v)
    print_version=:
    shift
    ;;
  --pep)
    parse_changelog_args+=(--version-format '^([0-9]+\.[0-9]+\.[0-9]+((a|b|rc)[0-9]+)?(\.post[0-9]+)?(\.dev[0-9]+)?|Unreleased)$')
    shift
    ;;
  *)
    args+=("$1")
    shift
    ;;
  esac
done

if [[ ${#args[@]} -gt 0 ]]; then
  # Only the first positional argument is used for now.
  changelog_file=${args[0]}
fi

parse() {
  command -v parse-changelog &>/dev/null || abort 'parse-changelog was not found'
  set -- "${parse_changelog_args[@]}" "$@"
  if parse-changelog "$@" &>/dev/null; then
    parse-changelog "$@"
  elif parse-changelog "$@" Unreleased &>/dev/null; then
    parse-changelog "$@" Unreleased
  else
    abort "failed to parse the changelog using parse-changelog $*"
  fi
}

rstrip_newlines() {
  # See: https://unix.stackexchange.com/a/666549
  awk '
    NF {
      print s $0
      s = ""
      next
    }
    {
      s = s ORS
    }
  '
}

command -v jq &>/dev/null || abort 'jq was not found'
version=$(parse --json "$changelog_file" | jq -r 'to_entries[0].value.version')

if $print_version; then
  echo "$version"
else
  parse "$changelog_file" "$version" |
    sed '/^<a name="[^"]*"><\/a>$/d' |
    sed '/^\[[^]]*]: https:\/\/github\.com\/.*$/d' |
    sed '/^<!--.*-->$/d' |
    rstrip_newlines
fi
