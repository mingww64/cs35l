#!/usr/bin/env bash
set -euo pipefail
git log $@ --pretty=%ci|grep -Po "[+-]\d{4}$" |sort|uniq -c|awk '{print $2, $1}'|sort -n #>  ../tzdb-"${1//../-}".tzcount