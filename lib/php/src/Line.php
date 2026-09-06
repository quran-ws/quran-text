<?php

declare(strict_types=1);

namespace QuranText;

/** One printed line.  Reconstructed, not read: see layers.derived.line. */
final class Line extends Span
{
    /**
     * @param int $number within the page, 1-based
     * @param int $index within the muṣḥaf, 0-based
     */
    public function __construct(
        Mushaf $mushaf,
        private readonly Page $ofPage,
        public readonly int $number,
        public readonly int $index,
    ) {
        $starts = $mushaf->doc['line_starts'];
        parent::__construct($mushaf, $starts[$index], $starts[$index + 1] ?? count($mushaf->words));
    }

    /** @internal */
    public static function fromIndex(Mushaf $mushaf, int $index): self
    {
        $starts = $mushaf->doc['line_starts'];
        $page = $mushaf->pageAt($starts[$index]);
        $first = Text::indexOf($starts, $page->start);
        return new self($mushaf, $page, $index - $first + 1, $index);
    }

    public function page(): Page
    {
        return $this->ofPage;
    }
}
