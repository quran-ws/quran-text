<?php

declare(strict_types=1);

namespace QuranText;

/** Text helpers shared by the whole library. */
final class Text
{
    public const AYAH_MARK = "\u{06DD}";

    /** The end-of-āyah sign with its number, as the muṣḥaf prints it: ۝٢٥٥ */
    public static function ayahMark(int $number): string
    {
        $digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
        return self::AYAH_MARK . strtr((string) $number, array_combine(range(0, 9), $digits));
    }

    /**
     * Reduce a word to plain letters for matching: no harakah, no waqf
     * marks, one alif, one yāʾ.  For search only — it is not a spelling.
     */
    public static function fold(string $text): string
    {
        $text = preg_replace('/[\x{0670}\x{0671}\x{0623}\x{0625}\x{0622}\x{0870}-\x{0882}]/u', "\u{0627}", $text);
        $text = preg_replace('/[\x{06D2}\x{06D1}\x{0649}]/u', "\u{064A}", $text);
        return preg_replace(
            '/[\x{0640}\x{0610}-\x{061A}\x{064B}-\x{065F}\x{06D6}-\x{06DC}\x{06DF}-\x{06E8}\x{06EA}-\x{06ED}\x{08CA}-\x{08FF}\x{0888}]/u',
            '',
            $text
        );
    }

    /** Index of the unit that contains $position (-1 before the first). */
    public static function indexOf(array $starts, int $position): int
    {
        $lo = 0;
        $hi = count($starts);
        while ($lo < $hi) {
            $mid = ($lo + $hi) >> 1;
            if ($starts[$mid] <= $position) {
                $lo = $mid + 1;
            } else {
                $hi = $mid;
            }
        }
        return $lo - 1;
    }

    /** @return array<string,true> */
    public static function markKinds(bool|array $marks): array
    {
        if ($marks === true) {
            return ['waqf' => true, 'division' => true, 'sajdah' => true,
                    'sajdah_line' => true, 'sah' => true, 'raised_dot' => true];
        }
        if ($marks === false) {
            return [];
        }
        return array_fill_keys($marks, true);
    }
}
