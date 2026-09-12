#!/bin/sh
# Push lib/swift to quran-ws/quran-text-swift, which is what SwiftPM resolves.
#
# SwiftPM looks for Package.swift at the root of whatever it clones, so the
# Swift binding cannot be consumed from the subdirectory it lives in. This
# replays lib/swift as its own history — same commits, same messages, rooted at
# lib/swift — and force-pushes it. The mirror carries no commits of its own; a
# change made there would be overwritten the next time this runs.
#
# There is no Swift registry: the tag is the release. After running this, tag
# the mirror at the version being released, or SwiftPM has nothing to resolve.
#
# Run it after anything under lib/swift lands on main.
set -e
git fetch origin main
git subtree split --prefix lib/swift --branch swift-mirror-tmp
git push --force https://github.com/quran-ws/quran-text-swift.git swift-mirror-tmp:main
git branch -D swift-mirror-tmp
echo "mirrored lib/swift to quran-ws/quran-text-swift"
echo "remember the tag: git push https://github.com/quran-ws/quran-text-swift.git <sha>:refs/tags/vX.Y.Z"
