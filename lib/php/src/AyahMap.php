<?php

declare(strict_types=1);

namespace QuranText;

/** out/ayah-map.json: what a Ḥafṣ (Kūfī) reference is in every edition. */
final class AyahMap
{
    /** @var string[] */
    public readonly array $editions;
    private readonly array $rows;

    public function __construct(array $doc)
    {
        if (($doc['format'] ?? null) !== 'quran-ayah-map') {
            throw new \InvalidArgumentException('not a quran-ayah-map file');
        }
        $this->editions = $doc['editions'];
        $rows = [];
        foreach ($doc['ayat'] as $r) {
            $rows["{$r['sura']}:{$r['ayah']}"] = $r;
        }
        $this->rows = $rows;
    }

    public static function load(string $path): self
    {
        return self::fromJson(file_get_contents($path));
    }

    public static function fromJson(string|array $data): self
    {
        return new self(is_string($data) ? json_decode($data, true, 512, JSON_THROW_ON_ERROR) : $data);
    }

    /** convert(2, 255, 'warsh') → AyahRef(2, 253, 'split', 254) */
    public function convert(int $sura, int $ayah, string $to): AyahRef
    {
        $row = $this->rows["$sura:$ayah"] ?? null;
        if ($row === null) {
            throw new \OutOfRangeException("$sura:$ayah is not a Kūfī āyah");
        }
        if (!isset($row[$to])) {
            throw new \InvalidArgumentException("no edition '$to'; editions are " . implode(', ', $this->editions));
        }
        $r = $row[$to];
        return new AyahRef($r['sura'], $r['ayah'], $r['relation'], $r['ayah_last'] ?? null);
    }

    /** The reference in every edition. @return array<string, AyahRef> */
    public function all(int $sura, int $ayah): array
    {
        $out = [];
        foreach ($this->editions as $e) {
            $out[$e] = $this->convert($sura, $ayah, $e);
        }
        return $out;
    }
}
