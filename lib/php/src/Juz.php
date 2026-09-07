<?php

declare(strict_types=1);

namespace QuranText;

final class Juz extends Span
{
    public function __construct(Mushaf $mushaf, public readonly int $number)
    {
        $starts = $mushaf->doc['juz_starts'] ?? null;
        if (!$starts) {
            throw new \LogicException($mushaf->absent('juz'));
        }
        if ($number < 1 || $number > count($starts)) {
            throw new \OutOfRangeException("juz $number: there are " . count($starts));
        }
        parent::__construct($mushaf, $starts[$number - 1], $starts[$number] ?? count($mushaf->words));
    }
}
