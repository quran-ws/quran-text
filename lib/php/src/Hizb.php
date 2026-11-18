<?php

declare(strict_types=1);

namespace QuranText;

/**
 * One of the 60 ḥizbs.  Hizb 2k-1 starts where the print starts juz k, which
 * is not always where juz_starts does (docs/known-issues.md §11).
 */
final class Hizb extends Division
{
    protected const LAYER = 'hizb';
}
