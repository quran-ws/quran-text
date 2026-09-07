<?php

declare(strict_types=1);

namespace QuranText;

final class Page extends Span
{
    public function __construct(Mushaf $mushaf, public readonly int $number)
    {
        $starts = $mushaf->doc['page_starts'];
        if ($number < 1 || $number > count($starts)) {
            throw new \OutOfRangeException("page $number: {$mushaf->nameEn} has " . count($starts) . ' pages');
        }
        parent::__construct($mushaf, $starts[$number - 1], $starts[$number] ?? count($mushaf->words));
    }

    /** @return Line[] */
    public function lines(): array
    {
        return $this->mushaf->linesBetween($this->start, $this->end);
    }

    public function line(int $number): Line
    {
        $lines = $this->lines();
        if ($number < 1 || $number > count($lines)) {
            throw new \OutOfRangeException("line $number: page {$this->number} has " . count($lines) . ' lines');
        }
        return $lines[$number - 1];
    }

    public function next(): ?self
    {
        $n = $this->number + 1;
        return $n <= $this->mushaf->pageCount() ? new self($this->mushaf, $n) : null;
    }

    public function previous(): ?self
    {
        $n = $this->number - 1;
        return $n >= 1 ? new self($this->mushaf, $n) : null;
    }
}
