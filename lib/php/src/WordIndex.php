<?php

declare(strict_types=1);

namespace QuranText;

/**
 * out/word-index.json: the numbering shared by all seven muṣḥafs.
 *
 * The file is 47 MB, and `json_decode`-ing it whole costs upwards of half a
 * gigabyte — PHP's array hashtables carry far more overhead per record than the
 * JSON does per byte, and the default `memory_limit` is 128 MB. So when the
 * index is read from a path it is not decoded up front: the build writes one
 * compact record per line, which lets us keep a byte offset per word (a packed
 * int list, a few MB) and decode a single line on demand.
 *
 * The in-memory constructor still accepts a decoded array, for callers who
 * already hold one; that path costs what it always did.
 */
final class WordIndex implements \Countable, \IteratorAggregate
{
    /** @var string[] */
    public readonly array $mushafs;
    public readonly int $total;

    /** Decoded records, when constructed from an array. Null in streaming mode. */
    private readonly ?array $words;
    /** Byte offset of each record's line, when streaming. Null otherwise. */
    private ?array $offsets = null;
    private ?string $path = null;
    /** @var resource|null */
    private $fh = null;

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

    /**
     * Read the index without decoding all of it: peak memory is a few MB
     * instead of ~600 MB, so this works under the stock `memory_limit`.
     *
     * The build writes one compact record per line, so the header can be read
     * on its own and each word reached by byte offset when it is asked for.
     */
    public static function load(string $path): self
    {
        $f = @fopen($path, 'rb');
        if ($f === false) {
            throw new \RuntimeException("cannot open $path");
        }

        $header = '';
        $offsets = [];
        try {
            // Everything before "words" is the header, and it still ends in the
            // comma that separated it — so closing it with an empty words array
            // gives valid JSON, no string surgery needed.
            while (($line = fgets($f)) !== false) {
                if (str_starts_with(ltrim($line), '"words"')) {
                    break;
                }
                $header .= $line;
            }
            while (($offset = ftell($f)) !== false && ($line = fgets($f)) !== false) {
                if (str_starts_with(ltrim($line), '{')) {
                    $offsets[] = $offset;
                }
            }
        } finally {
            fclose($f);
        }

        // The constructor does the validating, here as everywhere else.
        $doc = json_decode($header . '"words":[]}', true) ?? [];
        $doc['words'] = null;   // streaming: records are read from the file, not held
        $index = new self($doc);
        $index->offsets = $offsets;
        $index->path = $path;
        return $index;
    }

    public static function fromJson(string|array $data): self
    {
        return new self(is_string($data) ? json_decode($data, true, 512, JSON_THROW_ON_ERROR) : $data);
    }

    /** The file, opened once and kept for as long as the index is alive. */
    private function handle()
    {
        return $this->fh ??= fopen($this->path, 'rb');
    }

    /** The record at offset $i, decoded on its own. */
    private function record(int $i): array
    {
        if ($this->words !== null) {
            return $this->words[$i];
        }
        fseek($this->handle(), $this->offsets[$i]);
        return json_decode(rtrim(trim(fgets($this->handle())), ','), true, 512, JSON_THROW_ON_ERROR);
    }

    /** Every record in turn, one decode at a time. */
    private function records(): \Generator
    {
        if ($this->words !== null) {
            yield from $this->words;
            return;
        }
        foreach ($this->offsets as $i => $_) {
            yield $i => $this->record($i);
        }
    }

    public function word(int $number): IndexedWord
    {
        if ($number < 1 || $number > $this->total) {
            throw new \OutOfRangeException("number $number: the numbering is 1 … {$this->total}");
        }
        return new IndexedWord($this->record($number - 1));
    }

    /** By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word. */
    public function find(int $sura, int $ayah, int $index): ?IndexedWord
    {
        if ($this->byHafs === null) {
            // Keys to record numbers, not to records: holding 77k decoded
            // records here would put the memory straight back.
            $this->byHafs = [];
            foreach ($this->records() as $i => $r) {
                if ($h = $r['hafs']) {
                    $this->byHafs["{$h['sura']}:{$h['ayah']}:{$h['pos']}"] ??= $i;
                }
            }
        }
        $i = $this->byHafs["$sura:$ayah:$index"] ?? null;
        return $i === null ? null : new IndexedWord($this->record($i));
    }

    /** Every number whose folded spelling equals $text, folded. @return IndexedWord[] */
    public function search(string $text): array
    {
        if ($this->bySimple === null) {
            $this->bySimple = [];
            foreach ($this->records() as $i => $r) {
                $this->bySimple[Text::fold($r['uthmani'])][] = $i;
            }
        }
        return array_map(fn ($i) => new IndexedWord($this->record($i)),
                         $this->bySimple[Text::fold($text)] ?? []);
    }

    /**
     * Every number the riwāyāt spell in more than one way.
     *
     * Yields rather than returns a list: 53k of the 77k words differ, and
     * holding them all as decoded records at once costs several hundred MB.
     * Use `iterator_count()` if you only want how many.
     *
     * @return \Generator<IndexedWord>
     */
    public function differing(): \Generator
    {
        foreach ($this->records() as $r) {
            if (isset($r['groups'])) {
                yield new IndexedWord($r);
            }
        }
    }

    public function count(): int
    {
        return $this->total;
    }

    public function getIterator(): \Generator
    {
        foreach ($this->records() as $r) {
            yield new IndexedWord($r);
        }
    }
}
