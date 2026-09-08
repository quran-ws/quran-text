<?php

declare(strict_types=1);

namespace QuranText;

/**
 * The KFGQPC font a muṣḥaf's text is set in — the only one guaranteed to draw
 * every codepoint the words use.  $path is the file when the package has it
 * (bundled for Ḥafṣ, or data/fonts/ beside a loaded file); null otherwise.
 */
final class Font
{
    public function __construct(
        public readonly string $family,
        public readonly string $file,
        public readonly string $sha256,
        public readonly string $publisher,
        public readonly ?string $path = null,
    ) {
    }
}
