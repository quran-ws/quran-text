#!/bin/sh
# Push lib/php to quran-ws/quran-text-php, which is what Packagist reads.
#
# Packagist looks for composer.json at a repository root and nowhere else, so
# the PHP binding cannot be published from the subdirectory it lives in. This
# replays lib/php as its own history — same commits, same messages, rooted at
# lib/php — and force-pushes it. The mirror carries no commits of its own; a
# change made there would be overwritten the next time this runs.
#
# Run it after anything under lib/php lands on main.
set -e
git fetch origin main
git subtree split --prefix lib/php --branch php-mirror-tmp --rejoin=no 2>/dev/null \
  || git subtree split --prefix lib/php --branch php-mirror-tmp
git push --force https://github.com/quran-ws/quran-text-php.git php-mirror-tmp:main
git branch -D php-mirror-tmp
echo "mirrored lib/php to quran-ws/quran-text-php"
