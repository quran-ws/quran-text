<?php

declare(strict_types=1);

// Run from lib/php:  php tests/run.php
spl_autoload_register(function (string $class): void {
    if (str_starts_with($class, 'QuranText\\')) {
        require __DIR__ . '/../src/' . substr($class, 10) . '.php';
    }
});

use QuranText\AyahMap;
use QuranText\Mushaf;
use QuranText\Text;
use QuranText\WordIndex;

$out = __DIR__ . '/../../../data/';
$failures = 0;
function check(string $what, mixed $actual, mixed $expected): void
{
    global $failures;
    if ($actual !== $expected) {
        $failures++;
        fwrite(STDERR, "FAIL $what: got " . var_export($actual, true) . ", expected " . var_export($expected, true) . "\n");
    }
}

$hafs = Mushaf::load($out . 'mushaf/hafs.json');
$warsh = Mushaf::load($out . 'mushaf/warsh.json');
$bazzi = Mushaf::load($out . 'mushaf/bazzi.json');

$a = $hafs->ayah(2, 255);
check('key', $a->key(), '2:255');
check('length', count($a), 50);
check('page', $a->page()->number, 42);
check('juz', $a->juz()->number, 3);
check('line', $a->line()->number, 8);
check('text', str_starts_with($a->text(), 'ٱللَّهُ لَآ إِلَٰهَ'), true);
check('marker', str_ends_with($a->render(ayahMarks: true), ' ۝٢٥٥'), true);
check('waqf on', str_contains($a->render(marks: true), 'ۚ'), true);
check('waqf kinds', str_contains($a->render(marks: ['waqf']), 'ۚ'), true);
check('waqf off', str_contains($a->render(), 'ۚ'), false);
check('next', $a->next()->key(), '2:256');
check('next surah', $hafs->ayah(2, 286)->next()->key(), '3:1');
check('previous', $hafs->ayah(1, 1)->previous(), null);
try { $hafs->ayah(2, 287); check('range', false, true); } catch (OutOfRangeException) {}

$s = $hafs->surah(112);
check('surah ayahs', count($s->ayahs()), 4);
check('surah markers', substr_count($s->render(ayahMarks: true), '۝'), 4);
check('basmalah hafs', $s->basmalah(), null);
$p = $hafs->page(3);
check('lines', count($p->lines()), 15);
check('page first ayah', $p->ayahs()[0]->key(), '2:6');
check('page last ayah', $p->lastAyah()->key(), '2:16');
check('render lines', count(explode("\n", $p->render(lines: true))), 15);
check('line 1', $p->line(1)->text(), $p->lines()[0]->text());
check('juz 30', $hafs->juz(30)->firstAyah()->key(), '78:1');
$pages = $hafs->juz(30)->pages();
check('juz pages', end($pages)->number, 604);
check('surah 2 last page', $hafs->surah(2)->lastPage()->number, 49);
check('line 1:3', array_map(fn ($x) => $x->key(), $hafs->line(1, 3)->ayahs()), ['1:3', '1:4']);

$w = $hafs->word(1, 4, 1);
check('word', [$w->text(), $w->number(), $w->rasm_imlai(), $w->index()], ['مَٰلِكِ', 11, 'مالك', 1]);
check('sajdat', array_map(fn ($x) => $x->key(), array_slice($hafs->sajdat(), 0, 2)), ['7:206', '13:15']);
check('sajdat count', count($hafs->sajdat()), 15);
check('has sajdah', $hafs->ayah(7, 206)->hasSajdah(), true);
check('division count', count($hafs->divisionMarks()), 199);
check('division render', $hafs->divisionMarks()[0]->render(), '۞ إِنَّ');
check('numberAt', $hafs->numberAt(73948), 73950);
check('numberLast', $hafs->wordAt(73948)->numberLast(), 73951);
check('missing', $hafs->wordByNumber(25685), null);
check('joined', $hafs->wordByNumber(73951)->text(), 'وَأَلَّوِ');
check('by number', $hafs->wordByNumber(11)->text(), 'مَٰلِكِ');

check('warsh counted', $warsh->basmalahCounted, false);
check('warsh basmalah', count($warsh->surah(1)->basmalah()), 4);
check('warsh word 0', $warsh->wordAt(0)->ayah(), null);
check('warsh ayahAt 3', $warsh->ayahAt(3), null);
check('warsh 1:1', count($warsh->ayah(1, 1)), 4);
check('warsh ayahs', count($warsh->surah(1)->ayahs()), 7);
check('warsh marker', str_ends_with($warsh->ayah(2, 253)->render(ayahMarks: true), '۝٢٥٣'), true);
try { $bazzi->juz(1); check('bazzi juz', false, true); } catch (LogicException $e) { check('bazzi msg', str_contains($e->getMessage(), 'no juz layer'), true); }
check('bazzi juzAt', $bazzi->wordAt(5)->juz(), null);
check('bazzi has', $bazzi->has('juz'), false);
check('bazzi rasm_imlai', $bazzi->wordAt(5)->rasm_imlai(), null);

$hits = $hafs->search('مالك يوم الدين');
check('search', count($hits), 1);
check('search ayah', $hits[0]->firstAyah()->key(), '1:4');
check('fold', Text::fold('ٱلۡحَمۡدُ'), 'الحمد');
check('marker fn', Text::ayahMark(255), '۝٢٥٥');

check('bundled', Mushaf::hafs()->wordCount(), $hafs->wordCount());
check('font family', Mushaf::hafs()->font()->family, 'KFGQPC HAFS Uthmanic Script');
check('font bundled', is_file(Mushaf::hafs()->font()->path), true);
check('warsh font', is_file($warsh->font()->path), true);

$t = $hafs->ayah(2, 255)->to($warsh);
check('to key', $t->key(), '2:253-254');
check('to relation', $t->relation, 'split');
check('to back', $warsh->ayah(2, 253)->to($hafs)->key(), '2:255');
check('to unnumbered', $hafs->ayah(1, 1)->to($warsh)->relation, 'unnumbered');
check('to shifted', $hafs->ayah(57, 24)->to($warsh)->relation, 'shifted');
check('to same', $hafs->ayah(112, 1)->to($bazzi)->relation, 'same');
check('word to missing', $hafs->word(57, 24, 10)->to($warsh), null);
check('word to', $warsh->word(2, 253, 3)->to($hafs)->text(), 'إِلَٰهَ');

$map = AyahMap::load($out . 'ayah-map.json');
$r = $map->convert(2, 255, 'warsh');
check('convert', [$r->surah, $r->ayah, $r->ayahLast, $r->relation], [2, 253, 254, 'split']);
check('ref key', $r->key(), '2:253-254');
check('all', $map->all(1, 1)['warsh']->relation, 'unnumbered');
try { $map->convert(2, 255, 'nope'); check('no edition', false, true); } catch (InvalidArgumentException) {}

$idx = WordIndex::load($out . 'word-index.json');
check('form', $idx->word(11)->form('warsh'), 'مَلِكِ');
check('find', $idx->find(2, 255, 3)->rasm_uthmani(), 'إِلَٰهَ');
check('index search', in_array(11, array_map(fn ($x) => $x->number(), $idx->search('مالك')), true), true);
check('differing', count($idx->differing()), 53134);

echo $failures === 0 ? "OK\n" : "$failures failure(s)\n";
exit($failures === 0 ? 0 : 1);
