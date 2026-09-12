# quran-text for PHP

```sh
composer require quran-ws/quran-text
```

> Composer reads this directory through
> [quran-ws/quran-text-php](https://github.com/quran-ws/quran-text-php), because
> Packagist only looks for a `composer.json` at a repository root. That mirror is
> generated from this directory and is read-only — issues and pull requests belong
> here.

PHP 8.1+, Composer, no dependencies beyond `ext-json` and `ext-mbstring`. Ḥafṣ
is bundled.

```php
use QuranText\Mushaf;
use QuranText\AyahMap;

$m = Mushaf::hafs();                                             // bundled Ḥafṣ
$m->ayah(2, 255)->text();                                        // plain words
$m->ayah(2, 255)->render(marks: true, ayahMarks: true);        // with waqf marks and ۝٢٥٥
$m->page(3)->render(marks: true, ayahMarks: true, lines: true);
$m->surah(112)->ayahs();                                           // [Ayah, …]
$m->juz(30)->firstAyah()->key();                                 // "78:1"
$m->word(1, 4, 1)->number();                                     // 11, the same word in every riwāyah
$m->sajdat();                                                    // every āyah printed with ۩
$m->search('مالك يوم الدين');                                    // [Span]

$w = Mushaf::load('data/mushaf/warsh.json');                      // another riwāyah
AyahMap::load('data/ayah-map.json')->convert(2, 255, 'warsh');    // MappedAyah(2, 253, 'split', 254)
```

The font the text needs is bundled too: `$m->font()->family` names it and
`$m->font()->path` is the `.ttf` to serve. For another riwāyah `load()` finds
its font beside `data/fonts/`.

Wrong numbers throw `OutOfRangeException`; a layer the file lacks (juz in
Bazzī) throws `LogicException` with the reason from the file. One muṣḥaf takes
about 20 MB; the word index (`WordIndex`) needs a few hundred MB, so load it in
a CLI or a queue worker, not a web request. The full API is in
[the repository README](https://github.com/quran-ws/quran-text/blob/main/README.md).

Test: `php -d memory_limit=1G tests/run.php` in this directory.
