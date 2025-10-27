#!/usr/bin/env bash
set -e
git diff "${1}" "${2}" > "${1}"-"${2}".diff