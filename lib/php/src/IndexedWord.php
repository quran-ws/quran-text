<?php

declare(strict_types=1);

namespace QuranText;

/** One record of out/word-index.json: a shared number and what it is. */
final class IndexedWord
{
    public function __construct(public readonly array $raw)
    {
    }

    public function number(): int { return $this->raw['number']; }
    public function surah(): int { return $this->raw['surah']; }
    public function index(): int { return $this->raw['index']; }
    public function key(): string { return $this->raw['key']; }
    public function rasm_uthmani(): string { return $this->raw['rasm_uthmani']; }
    public function plain(): string { return $this->raw['plain']; }
    public function rasm(): string { return $this->raw['rasm']; }
    public function pointed(): string { return $this->raw['pointed']; }
    public function status(): string { return $this->raw['status']; }
    /** {surah, ayah, position} in the Kūfī count, or null where Ḥafṣ lacks the word. */
    public function hafs(): ?array { return $this->raw['hafs']; }
    /** Āyah number per riwāyah. @return array<string,int> */
    public function ayah(): array { return $this->raw['ayah']; }
    /** Each riwāyah's own spelling; absent where it does not read the word. @return array<string,string> */
    public function forms(): array { return $this->raw['forms']; }
    public function groups(): array { return $this->raw['groups'] ?? []; }
    /** @return string[] */
    public function missing(): array { return $this->raw['missing'] ?? []; }
    /** @return string[] */
    public function writtenJoined(): array { return $this->raw['written_joined'] ?? []; }

    /** How one riwāyah spells it; null where it does not read the word. */
    public function form(string $riwayah): ?string
    {
        return $this->raw['forms'][$riwayah] ?? null;
    }
}
