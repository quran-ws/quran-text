import 'dart:convert';
import 'dart:io';

import 'package:quran_text/quran_text.dart';
import 'package:test/test.dart';

// Run from lib/dart with the dataset built:  dart test
const out = '../../out/';
Mushaf load(String key) =>
    Mushaf.fromJson(jsonDecode(File('${out}mushaf/$key.json').readAsStringSync()));

void main() {
  final hafs = load('hafs');
  final warsh = load('warsh');
  final bazzi = load('bazzi');

  test('ayah text, layers and rendering', () {
    final a = hafs.ayah(2, 255);
    expect(a.key, '2:255');
    expect(a.length, 50);
    expect([a.page.number, a.juz!.number, a.line!.number], [42, 3, 8]);
    expect(a.text, startsWith('ٱللَّهُ لَآ إِلَٰهَ'));
    expect(a.render(ayahMarkers: true), endsWith(' ۝٢٥٥'));
    expect(a.render(marks: true), contains('ۚ'));
    expect(a.render(marks: {MarkKind.waqf}), contains('ۚ'));
    expect(a.render(marks: {MarkKind.hizb}), isNot(contains('ۚ')));
    expect(a.render(), isNot(contains('ۚ')));
    expect(a.next()!.key, '2:256');
    expect(hafs.ayah(2, 286).next()!.key, '3:1');
    expect(hafs.ayah(1, 1).previous(), isNull);
    expect(() => hafs.ayah(2, 287), throwsRangeError);
  });

  test('sura, page, line, juz', () {
    final s = hafs.sura(112);
    expect(s.ayat.length, 4);
    expect('۝'.allMatches(s.render(ayahMarkers: true)).length, 4);
    expect(s.basmalah, isNull);
    final p = hafs.page(3);
    expect(p.lines.length, 15);
    expect([p.ayat.first.key, p.ayat.last.key], ['2:6', '2:16']);
    expect(p.render(lines: true).split('\n').length, 15);
    expect(p.line(1).text, p.lines.first.text);
    expect(hafs.juz(30).firstAyah!.key, '78:1');
    expect(hafs.juz(30).pages.last.number, 604);
    expect(hafs.sura(2).lastPage.number, 49);
    expect(hafs.line(1, 3).ayat.map((a) => a.key), ['1:3', '1:4']);
  });

  test('words, marks, numbering', () {
    final w = hafs.word(1, 4, 1);
    expect([w.text, w.number, w.imlaei, w.index], ['مَٰلِكِ', 11, 'مالك', 1]);
    expect(hafs.sajdat().take(2).map((a) => a.key), ['7:206', '13:15']);
    expect(hafs.sajdat().length, 15);
    expect(hafs.ayah(7, 206).hasSajdah, isTrue);
    expect(hafs.hizbMarks().length, 199);
    expect(hafs.hizbMarks().first.render(), '۞ إِنَّ');
    expect(hafs.numberAt(73948), 73950);
    expect(hafs.wordAt(73948).numberLast, 73951);
    expect(hafs.wordByNumber(25685), isNull);
    expect(hafs.wordByNumber(73951)!.text, 'وَأَلَّوِ');
    expect(hafs.wordByNumber(11)!.text, 'مَٰلِكِ');
  });

  test('unnumbered basmalah and absent layers', () {
    expect(warsh.basmalahCounted, isFalse);
    expect(warsh.sura(1).basmalah!.length, 4);
    expect(warsh.wordAt(0).ayah, isNull);
    expect(warsh.ayahAt(3), isNull);
    expect(warsh.ayah(1, 1).length, 4);
    expect(warsh.sura(1).ayat.length, 7);
    expect(warsh.ayah(2, 253).render(ayahMarkers: true), endsWith('۝٢٥٣'));
    expect(() => bazzi.juz(1), throwsStateError);
    expect(bazzi.wordAt(5).juz, isNull);
    expect(bazzi.has('juz'), isFalse);
    expect(bazzi.wordAt(5).imlaei, isNull);
  });

  test('search', () {
    final hits = hafs.search('مالك يوم الدين');
    expect(hits.length, 1);
    expect(hits.first.firstAyah!.key, '1:4');
    expect(fold('ٱلۡحَمۡدُ'), 'الحمد');
    expect(ayahMarker(255), '۝٢٥٥');
  });

  test('bundled hafs', () async {
    final m = await Mushaf.hafs();
    expect(m.key, 'hafs');
    expect(m.wordCount, hafs.wordCount);
    expect(m.font.family, 'KFGQPC HAFS Uthmanic Script');
    expect(warsh.font.file, 'out/fonts/UthmanicWarsh-v-3.0.ttf');
  });

  test('to(): the same ayah and word in another riwayah', () {
    final m = hafs.ayah(2, 255).to(warsh);
    expect(m.key, '2:253-254');
    expect(m.relation, 'split');
    expect(warsh.ayah(2, 253).to(hafs).key, '2:255');
    expect(hafs.ayah(1, 1).to(warsh).relation, 'unnumbered');
    expect(hafs.ayah(57, 24).to(warsh).relation, 'shifted');
    expect(hafs.ayah(112, 1).to(bazzi).relation, 'same');
    expect(hafs.word(57, 24, 10).to(warsh), isNull);
    expect(warsh.word(2, 253, 3).to(hafs)!.text, 'إِلَٰهَ');
  });

  test('ayah map', () {
    final map = AyahMap.fromJson(File('${out}ayah-map.json').readAsStringSync());
    final r = map.convert(2, 255, 'warsh');
    expect([r.sura, r.ayah, r.ayahLast, r.relation], [2, 253, 254, 'split']);
    expect(r.key, '2:253-254');
    expect(map.all(1, 1)['warsh']!.relation, 'unnumbered');
    expect(() => map.convert(2, 255, 'nope'), throwsArgumentError);
  });

  test('word index', () {
    final idx = WordIndex.fromJson(File('${out}word-index.json').readAsStringSync());
    expect(idx.word(11).form('warsh'), 'مَلِكِ');
    expect(idx.find(2, 255, 3)!.uthmani, 'إِلَٰهَ');
    expect(idx.search('مالك').map((w) => w.number), contains(11));
    expect(idx.differing().length, 53134);
  });
}
