<?php

declare(strict_types=1);

namespace QuranText;

/** out/word-index.json: the numbering shared by all seven muṣḥafs. */
final class WordIndex implements \Countable, \IteratorAggregate
{
    /** @var string[] */
    public readonly array $mushafs;
    public readonly int $total;
    private readonly array $words;
    private ?array $byHafs = null;
    private ?array $bySimple = null;

    public function __construct(array $doc)
    {
        if (($doc['format'] ?? null) !== 'quran-word-index') {
            throw new \InvalidArgumentException('not a quran-word-index file');
        }
        $this->mushafs = $doc['mushafs'];
        $this->total = $doc['total'];
        $this->words = $doc['words'];
    }

    public static function load(string $path): self
    {
        return self::fromJson(file_get_contents($path));
    }

    public static function fromJson(string|array $data): self
    {
        return new self(is_string($data) ? json_decode($data, true, 512, JSON_THROW_ON_ERROR) : $data);
    }

    public function word(int $number): IndexedWord
    {
        if ($number < 1 || $number > $this->total) {
            throw new \OutOfRangeException("number $number: the numbering is 1 … {$this->total}");
        }
        return new IndexedWord($this->words[$number - 1]);
    }

    /** By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word. */
    public function find(int $sura, int $ayah, int $index): ?IndexedWord
    {
        if ($this->byHafs === null) {
            $this->byHafs = [];
            foreach ($this->words as $r) {
                if ($h = $r['hafs']) {
                    $this->byHafs["{$h['sura']}:{$h['ayah']}:{$h['pos']}"] ??= $r;
                }
            }
        }
        $r = $this->byHafs["$sura:$ayah:$index"] ?? null;
        return $r ? new IndexedWord($r) : null;
    }

    /** Every number whose folded spelling equals $text, folded. @return IndexedWord[] */
    public function search(string $text): array
    {
        if ($this->bySimple === null) {
            $this->bySimple = [];
            foreach ($this->words as $r) {
                $this->bySimple[Text::fold($r['uthmani'])][] = $r;
            }
        }
        return array_map(fn ($r) => new IndexedWord($r), $this->bySimple[Text::fold($text)] ?? []);
    }

    /** Every number the riwāyāt spell in more than one way. @return IndexedWord[] */
    public function differing(): array
    {
        $out = [];
        foreach ($this->words as $r) {
            if (isset($r['groups'])) {
                $out[] = new IndexedWord($r);
            }
        }
        return $out;
    }

    public function count(): int
    {
        return $this->total;
    }

    public function getIterator(): \Generator
    {
        foreach ($this->words as $r) {
            yield new IndexedWord($r);
        }
    }
}
