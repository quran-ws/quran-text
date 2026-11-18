<?php

declare(strict_types=1);

namespace QuranText;

/**
 * One unit of a division layer the printed muṣḥaf marks: a ḥizb or a part of one.
 *
 * The layer is read from the margin of the print, not from the release
 * (layers.derived.divisions).  A muṣḥaf divides the ḥizb into four
 * rubu_al_hizbs or into eight thumns, never both, and one whose print was
 * not read carries none of the three.
 */
abstract class Division extends Span
{
    /** The layer name: "hizb", "rubu_al_hizb" or "thumn". */
    protected const LAYER = '';

    public function __construct(Mushaf $mushaf, public readonly int $number)
    {
        $layer = static::LAYER;
        $starts = $mushaf->doc[$layer . '_starts'] ?? null;
        if (!$starts) {
            throw new \LogicException($mushaf->absent($layer));
        }
        if ($number < 1 || $number > count($starts)) {
            throw new \OutOfRangeException("$layer $number: there are " . count($starts));
        }
        parent::__construct($mushaf, $starts[$number - 1], $starts[$number] ?? count($mushaf->words));
    }
}
