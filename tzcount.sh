#!/usr/bin/env bash
set -euo pipefail
git log "$1" --pretty=fuller|grep -Po "(?<=CommitDate:.{25})[+-]{1}\d{4}$" |sort|uniq -c|awk '{print $2, $1}'|sort -n #>  tzdb-"${1//../-}".tzcount