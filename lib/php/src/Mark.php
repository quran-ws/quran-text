<?php

declare(strict_types=1);

namespace QuranText;

/** A sign printed against a word: kind is waqf, hizb or sajdah. */
final class Mark
{
    public function __construct(
        public readonly string $kind,
        public readonly string $side,
        public readonly string $sign,
    ) {
    }
}
