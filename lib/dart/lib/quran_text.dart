/// quran-text — read the muṣḥaf files of the quran-text dataset.
///
/// ```dart
/// import 'package:quran_text/quran_text.dart';
/// final m = await Mushaf.hafs();                          // Dart VM
/// final m = await Mushaf.hafs(read: rootBundle.loadString); // Flutter
/// final m = Mushaf.fromJson(await rootBundle.loadString('assets/warsh.json')); // another riwāyah
/// m.ayah(2, 255).text;
/// m.ayah(2, 255).render(marks: true, ayahMarks: true);
/// m.page(3).lines;
/// m.juz(30).firstAyah!.key;        // "78:1"
/// ```
///
/// Everything is a slice of one `words` list.  A [Span] is a slice with
/// [Span.text] and [Span.render]; [Surah], [Ayah], [Page], [Line] and [Juz]
/// are spans that know their place.  Positions are 0-based indices into
/// `words`; sūrah, āyah, page, line and juz numbers are 1-based, as printed.
/// Āyah numbers are in this edition's own count; use [AyahMap] to convert
/// between editions.
///
/// No dependencies.
library quran_text;

import 'dart:convert';
import 'dart:io';
import 'dart:isolate';

const String ayahMarkSign = '۝';

const _arabicIndic = '٠١٢٣٤٥٦٧٨٩';

/// The end-of-āyah sign with its number, as the muṣḥaf prints it: ۝٢٥٥
String ayahMark(int number) => ayahMarkSign +
    number.toString().split('').map((d) => _arabicIndic[int.parse(d)]).join();

final _foldAlef = RegExp('[\\u0670\\u0671\\u0623\\u0625\\u0622\\u0870-\\u0882]');
final _foldYeh = RegExp('[\\u06D2\\u06D1\\u0649]');
final _foldDrop = RegExp(
    '[\\u0640\\u0610-\\u061A\\u064B-\\u065F\\u06D6-\\u06DC\\u06DF-\\u06E8\\u06EA-\\u06ED\\u08CA-\\u08FF\\u0888]');

/// Reduce a word to plain letters for matching: no harakah, no waqf
/// marks, one alif, one yāʾ.  For search only — it is not a spelling.
String fold(String text) => text
    .replaceAll(_foldAlef, '\u0627')
    .replaceAll(_foldYeh, '\u064A')
    .replaceAll(_foldDrop, '');

/// Index of the unit that contains [position] (-1 before the first).
int _indexOf(List<int> starts, int position) {
  var lo = 0, hi = starts.length;
  while (lo < hi) {
    final mid = (lo + hi) >> 1;
    if (starts[mid] <= position) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }
  return lo - 1;
}

// The names are the strings the data uses, so `byName` reads them directly.
// ignore: constant_identifier_names
enum MarkKind { waqf, division, sajdah, sajdah_line }

MarkKind _kindOf(String s) => MarkKind.values.byName(s);

Set<MarkKind> _markKinds(Object marks) {
  if (marks == true) return MarkKind.values.toSet();
  if (marks == false) return const {};
  return (marks as Iterable<MarkKind>).toSet();
}

/// The KFGQPC font a muṣḥaf's text is set in — the only one guaranteed to
/// draw every codepoint the words use.  For Ḥafṣ the package bundles it and
/// declares it in its pubspec, so in Flutter
/// `TextStyle(fontFamily: m.font.family, package: 'quran_text')` just works.
class Font {
  final String family;
  /// The file name; the copy lives under `data/fonts/` in the dataset.
  final String file;
  final String sha256;
  final String publisher;
  const Font(this.family, this.file, this.sha256, this.publisher);
  @override
  String toString() => family;
}

/// A sign printed against a word.
class Mark {
  final MarkKind kind;
  final String side; // "before" | "after"
  final String sign;
  const Mark(this.kind, this.side, this.sign);
  @override
  String toString() => sign;
}

/// One printed word and everything the muṣḥaf says about it.
class Word {
  final Mushaf _m;
  final int position;

  Word(this._m, this.position) {
    if (position < 0 || position >= _m.words.length) {
      throw RangeError('position $position is outside the muṣḥaf');
    }
  }

  String get text => _m.words[position];

  /// Plain modern spelling, Ḥafṣ only; null elsewhere.
  String? get rasm_imlai => _m._rasm_imlai?[position];
  Surah get surah => _m.surahAt(position);

  /// The āyah this word is in; null for the unnumbered basmalah.
  Ayah? get ayah => _m.ayahAt(position);

  /// 1-based position within the āyah; null when unnumbered.
  int? get index {
    final a = ayah;
    return a == null ? null : position - a.start + 1;
  }

  Page get page => _m.pageAt(position);
  Line? get line => _m.lineAt(position);
  Juz? get juz => _m.juzAt(position);

  /// The shared number: the same word in every riwāyah.
  int get number => _m._numbers[position].$1;

  /// Equal to [number] except where this muṣḥaf writes two numbers as one word.
  int get numberLast => _m._numbers[position].$2;

  List<Mark> get marks => _m._marksAt[position] ?? const [];
  bool hasMark(MarkKind kind) => marks.any((mk) => mk.kind == kind);

  /// The same word in another riwāyah, by the shared number; null where it does not read it.
  Word? to(Mushaf other) => other.wordByNumber(number);

  /// The word with its signs: ۞ before, waqf and ۩ after.
  /// [marks] is `true` for every sign or an iterable of [MarkKind].
  String render({Object marks = true}) {
    final kinds = _markKinds(marks);
    var before = '', after = '';
    for (final mk in this.marks) {
      if (!kinds.contains(mk.kind)) continue;
      if (mk.side == 'before') {
        before += '${mk.sign} ';
      } else {
        after += mk.sign;
      }
    }
    return before + text + after;
  }

  @override
  String toString() => text;
}

/// A run of positions start … end-1 of one muṣḥaf.
class Span extends Iterable<Word> {
  final Mushaf _m;
  final int start;
  final int end;
  Span(this._m, this.start, this.end);

  Mushaf get mushaf => _m;
  @override
  int get length => end - start;
  List<String> get words => _m.words.sublist(start, end);
  List<Word> get wordList => [for (var p = start; p < end; p++) Word(_m, p)];
  @override
  Iterator<Word> get iterator => wordList.iterator;

  /// The words joined with spaces, without any sign.
  String get text => words.join(' ');

  /// The text as the muṣḥaf prints it, with what you ask for.
  ///
  /// [marks]: `true` for every sign, or an iterable of [MarkKind].
  /// [ayahMarks] appends ۝ with the āyah number after each āyah that ends
  /// inside the span.  [lines] breaks the text where the printed lines break.
  String render({Object marks = false, bool ayahMarks = false, bool lines = false}) {
    final kinds = _markKinds(marks);
    final lineStarts = lines ? _m._lineStartSet : null;
    final out = StringBuffer();
    for (var position = start; position < end; position++) {
      if (lineStarts != null && position != start && lineStarts.contains(position)) {
        out.write('\n');
      } else if (position != start) {
        out.write(' ');
      }
      var token = _m.words[position];
      for (final mk in _m._marksAt[position] ?? const <Mark>[]) {
        if (!kinds.contains(mk.kind)) continue;
        token = mk.side == 'before' ? '${mk.sign} $token' : token + mk.sign;
      }
      out.write(token);
      if (ayahMarks) {
        final k = _m._ayahEnds[position];
        if (k != null) out.write(' ${ayahMark(_m._ayahNumber(k))}');
      }
    }
    return out.toString();
  }

  /// Every numbered āyah with at least one word in the span.
  List<Ayah> get ayahs {
    final starts = _m._ayahStarts;
    final first = _indexOf(starts, start).clamp(0, starts.length);
    final last = _indexOf(starts, end - 1);
    return [for (var k = first; k <= last; k++) Ayah._fromIndex(_m, k)];
  }

  Ayah? get firstAyah => ayahs.firstOrNull;
  Ayah? get lastAyah => ayahs.lastOrNull;

  List<Surah> get surahs {
    final starts = _m._surahStarts;
    return _m.surahs.sublist(_indexOf(starts, start), _indexOf(starts, end - 1) + 1);
  }

  List<Page> get pages {
    final starts = _m._pageStarts;
    return [
      for (var n = _indexOf(starts, start); n <= _indexOf(starts, end - 1); n++)
        Page(_m, n + 1)
    ];
  }

  /// The page the span starts on.
  Page get page => _m.pageAt(start);
  Juz? get juz => _m.juzAt(start);

  /// Every sign inside the span, with the word it is printed on.
  List<(Word, Mark)> get marks => [
        for (var p = start; p < end; p++)
          for (final mk in _m._marksAt[p] ?? const <Mark>[]) (Word(_m, p), mk)
      ];

  /// The [index]-th word of the span, 1-based.
  Word word(int index) {
    if (index < 1 || index > length) {
      throw RangeError('word $index: the span has $length words');
    }
    return Word(_m, start + index - 1);
  }

  @override
  String toString() => 'Span($start, $end)';
}

/// Where an āyah falls in another riwāyah.  [relation]: same (one āyah, the
/// same words), merged (one āyah holding more), split (several āyāt), shifted
/// (one āyah, boundaries crossing), unnumbered (the basmalah printed without
/// a number), missing (no word of it).
class AyahMatch {
  final List<Ayah> ayahs;
  final String relation;
  const AyahMatch(this.ayahs, this.relation);
  Ayah? get first => ayahs.firstOrNull;
  Ayah? get last => ayahs.lastOrNull;

  /// "2:253-254"
  String get key {
    if (ayahs.isEmpty) return '';
    final a = ayahs.first, b = ayahs.last;
    return a == b ? a.key : '${a.key}-${b.number}';
  }

  @override
  String toString() => '${key.isEmpty ? '-' : key} ($relation)';
}

/// One numbered āyah, in this edition's own count.
class Ayah extends Span {
  final Surah surah;
  final int number;

  /// 0-based ordinal of the āyah in the muṣḥaf.
  final int index;

  Ayah._(Mushaf m, this.surah, this.number, this.index)
      : super(m, m._ayahStarts[index],
            index + 1 < m._ayahStarts.length ? m._ayahStarts[index + 1] : m.words.length);

  factory Ayah(Mushaf m, int surah, int number) {
    final s = m.surah(surah);
    if (number < 1 || number > s.ayahCount) {
      throw RangeError('${s.nameEn} has ${s.ayahCount} āyāt in ${m.nameEn}, not $number');
    }
    return Ayah._(m, s, number, s._firstAyah + number - 1);
  }

  factory Ayah._fromIndex(Mushaf m, int k) {
    final s = m.surahs[m._surahOfAyahIndex(k)];
    return Ayah._(m, s, k - s._firstAyah + 1, k);
  }

  /// "2:255"
  String get key => '${surah.number}:$number';

  /// The printed line the āyah starts on.
  Line? get line => _m.lineAt(start);

  /// Every printed line the āyah touches.
  List<Line> get lines => _m._linesBetween(start, end);
  List<String?>? get rasm_imlai => _m._rasm_imlai?.sublist(start, end);
  bool get hasSajdah => marks.any((e) => e.$2.kind == MarkKind.sajdah);

  /// ۝٢٥٥
  String get marker => ayahMark(number);

  /// The shared numbers of this āyah's words.
  Set<int> get numbers {
    final first = _m._numbers[start].$1, last = _m._numbers[end - 1].$2;
    return {for (var n = first; n <= last; n++) if (!_m.missingNumbers.contains(n)) n};
  }

  /// This āyah in another riwāyah: `hafs.ayah(2, 255).to(warsh)` → 2:253-254, split.
  /// Computed from the shared numbering, so it works between any two riwāyāt.
  AyahMatch to(Mushaf other) {
    final mine = numbers;
    final hits = <Ayah>[];
    var unnumbered = false;
    for (final n in mine.toList()..sort()) {
      final w = other.wordByNumber(n);
      if (w == null) continue;
      final a = w.ayah;
      if (a == null) {
        unnumbered = true;
      } else if (hits.isEmpty || hits.last != a) {
        hits.add(a);
      }
    }
    if (hits.isEmpty) return AyahMatch(const [], unnumbered ? 'unnumbered' : 'missing');
    if (hits.length > 1) return AyahMatch(hits, 'split');
    final theirs = hits.first.numbers;
    final superset = theirs.containsAll(mine);
    final same = superset && theirs.length == mine.length;
    return AyahMatch(hits, same ? 'same' : superset ? 'merged' : 'shifted');
  }

  Ayah? next() => index + 1 < _m.ayahCount ? Ayah._fromIndex(_m, index + 1) : null;
  Ayah? previous() => index > 0 ? Ayah._fromIndex(_m, index - 1) : null;

  @override
  bool operator ==(Object other) => other is Ayah && other._m == _m && other.index == index;
  @override
  int get hashCode => Object.hash(_m, index);
  @override
  String toString() => key;
}

class Surah extends Span {
  final int number;
  final String nameAr;
  final String nameEn;
  final String revelation;
  final bool hasBasmalah;
  final int ayahCount;
  final int _firstAyah;

  Surah._(Mushaf m, this.number, Map<String, dynamic> info)
      : nameAr = info['name_ar'] as String,
        nameEn = info['name_en'] as String,
        revelation = info['revelation'] as String,
        hasBasmalah = info['has_basmalah'] as bool,
        ayahCount = info['ayah_count'] as int,
        _firstAyah = info['first_ayah'] as int,
        super(m, m._surahStarts[number - 1],
            number < m._surahStarts.length ? m._surahStarts[number] : m.words.length);

  List<Ayah> get ayahs => [for (var n = 1; n <= ayahCount; n++) Ayah(_m, number, n)];
  Ayah ayah(int number) => Ayah(_m, this.number, number);

  /// The basmalah where it is printed unnumbered before āyah 1 (Warsh,
  /// Qālūn, Dūrī, Sūsī at al-Fātiḥah); null otherwise.
  Span? get basmalah {
    final first = _m._ayahStarts[_firstAyah];
    return first > start ? Span(_m, start, first) : null;
  }

  Page get firstPage => page;
  Page get lastPage => _m.pageAt(end - 1);
  @override
  String toString() => '$number $nameEn';
}

class Page extends Span {
  final int number;

  Page._(Mushaf m, this.number)
      : super(m, m._pageStarts[number - 1],
            number < m._pageStarts.length ? m._pageStarts[number] : m.words.length);

  factory Page(Mushaf m, int number) {
    if (number < 1 || number > m._pageStarts.length) {
      throw RangeError('page $number: ${m.nameEn} has ${m._pageStarts.length} pages');
    }
    return Page._(m, number);
  }

  List<Line> get lines => _m._linesBetween(start, end);
  Line line(int number) {
    final all = lines;
    if (number < 1 || number > all.length) {
      throw RangeError('line $number: page ${this.number} has ${all.length} lines');
    }
    return all[number - 1];
  }

  Page? next() => number < _m.pageCount ? Page(_m, number + 1) : null;
  Page? previous() => number > 1 ? Page(_m, number - 1) : null;
  @override
  String toString() => 'page $number';
}

/// One printed line.  Reconstructed, not read: see `layers.derived.line`.
class Line extends Span {
  @override
  final Page page;

  /// Within the page, 1-based.
  final int number;

  /// Within the muṣḥaf, 0-based.
  final int index;

  Line._(Mushaf m, this.page, this.number, this.index)
      : super(m, m._lineStarts![index],
            index + 1 < m._lineStarts!.length ? m._lineStarts![index + 1] : m.words.length);

  factory Line._fromIndex(Mushaf m, int index) {
    final starts = m._lineStarts!;
    final page = m.pageAt(starts[index]);
    return Line._(m, page, index - _indexOf(starts, page.start) + 1, index);
  }

  @override
  String toString() => 'page ${page.number}, line $number';
}

class Juz extends Span {
  final int number;

  Juz._(Mushaf m, this.number)
      : super(m, m._juzStarts![number - 1],
            number < m._juzStarts!.length ? m._juzStarts![number] : m.words.length);

  factory Juz(Mushaf m, int number) {
    final starts = m._juzStarts;
    if (starts == null) throw StateError(m._absent('juz'));
    if (number < 1 || number > starts.length) {
      throw RangeError('juz $number: there are ${starts.length}');
    }
    return Juz._(m, number);
  }

  @override
  String toString() => 'juz $number';
}

/// One muṣḥaf file, `data/mushaf/<key>.json`.
class Mushaf {
  final Map<String, dynamic> _doc;
  final List<String> words;
  final String key;
  final String nameEn;
  final String nameAr;
  final String? qiraahEn;
  final String? qiraahAr;
  final String countingSystem;
  final bool basmalahCounted;
  late final List<Surah> surahs;

  final List<String?>? _rasm_imlai;
  final List<int> _surahStarts;
  final List<int> _ayahStarts;
  final List<int> _pageStarts;
  final List<int>? _lineStarts;
  final List<int>? _juzStarts;
  late final List<int> _surahFirstAyah;
  final Map<int, int> _ayahEnds = {};
  final Map<int, List<Mark>> _marksAt = {};
  late final Set<int> _lineStartSet;
  List<(int, int)>? _numbersCache;
  List<String>? _foldCache;

  Mushaf._(this._doc)
      : words = List<String>.from(_doc['words'] as List),
        key = _doc['mushaf']['key'] as String,
        nameEn = _doc['mushaf']['name_en'] as String,
        nameAr = _doc['mushaf']['name_ar'] as String,
        qiraahEn = _doc['mushaf']['qiraah_en'] as String?,
        qiraahAr = _doc['mushaf']['qiraah_ar'] as String?,
        countingSystem = _doc['counting']['system'] as String,
        basmalahCounted = _doc['counting']['basmalah_counted'] as bool,
        _rasm_imlai = _doc['rasm_imlai'] == null ? null : List<String?>.from(_doc['rasm_imlai'] as List),
        _surahStarts = List<int>.from(_doc['surah_starts'] as List),
        _ayahStarts = List<int>.from(_doc['ayah_starts'] as List),
        _pageStarts = List<int>.from(_doc['page_starts'] as List),
        _lineStarts = _doc['line_starts'] == null ? null : List<int>.from(_doc['line_starts'] as List),
        _juzStarts = _doc['juz_starts'] == null ? null : List<int>.from(_doc['juz_starts'] as List) {
    surahs = [for (var n = 1; n <= 114; n++) Surah._(this, n, (_doc['surahs'] as List)[n - 1])];
    _surahFirstAyah = [for (final s in surahs) s._firstAyah];
    for (var k = 0; k < _ayahStarts.length; k++) {
      final end = k + 1 < _ayahStarts.length ? _ayahStarts[k + 1] : words.length;
      _ayahEnds[end - 1] = k;
    }
    final types = [
      for (final t in _doc['mark_types'] as List)
        Mark(_kindOf(t['kind'] as String), t['side'] as String, t['sign'] as String)
    ];
    for (final pair in _doc['marks'] as List) {
      _marksAt.putIfAbsent(pair[0] as int, () => []).add(types[pair[1] as int]);
    }
    _lineStartSet = (_lineStarts ?? const []).toSet();
  }

  /// Ḥafṣ, the riwāyah nearly every app uses, bundled with the package.
  ///
  /// In Flutter pass the asset loader: `Mushaf.hafs(read: rootBundle.loadString)`.
  /// On the Dart VM (CLI, server, tests) no argument is needed.
  static Future<Mushaf> hafs({Future<String> Function(String path)? read}) async {
    if (read != null) return Mushaf.fromJson(await read('packages/quran_text/assets/hafs.json'));
    final lib = await Isolate.resolvePackageUri(Uri.parse('package:quran_text/quran_text.dart'));
    if (lib == null) throw StateError('cannot locate the bundled hafs.json; pass read:');
    return Mushaf.fromJson(await File.fromUri(lib.resolve('../assets/hafs.json')).readAsString());
  }

  /// Any of the seven riwāyāt, from a decoded JSON map or a JSON string.
  factory Mushaf.fromJson(Object data) {
    final doc = data is String ? jsonDecode(data) : data;
    if (doc is! Map<String, dynamic> || doc['format'] != 'quran-mushaf') {
      throw ArgumentError('not a quran-mushaf file');
    }
    return Mushaf._(doc);
  }

  // -- what the file carries --

  /// The font to ship with this text; see [Font].
  Font get font {
    final f = _doc['font'] as Map<String, dynamic>;
    return Font(f['family'] as String, f['file'] as String, f['sha256'] as String, f['publisher'] as String);
  }

  List<String> get layers => List<String>.from(_doc['layers']['present'] as List);

  /// `has('juz')`, `has('rasm_imlai')`, `has('lines')` …
  bool has(String layer) => layers.contains(layer);
  String _absent(String layer) {
    final why = (_doc['layers']['absent'] as Map)[layer] ?? 'not in this file';
    return '$nameEn has no $layer layer: $why';
  }

  Map<String, dynamic> get counting => _doc['counting'] as Map<String, dynamic>;
  Map<String, dynamic> get provenance => _doc['provenance'] as Map<String, dynamic>;
  int get wordCount => words.length;
  int get ayahCount => _ayahStarts.length;
  int get pageCount => _pageStarts.length;
  int get lineCount => _lineStarts?.length ?? 0;
  int get juzCount => _juzStarts?.length ?? 0;

  // -- units by number --

  Surah surah(int number) {
    if (number < 1 || number > 114) throw RangeError('sūrah $number: there are 114');
    return surahs[number - 1];
  }

  /// Āyah [number] of [surah] in this edition's own count.
  Ayah ayah(int surah, int number) => Ayah(this, surah, number);
  Page page(int number) => Page(this, number);
  Juz juz(int number) => Juz(this, number);
  Line line(int page, int number) => Page(this, page).line(number);

  /// Word [index] (1-based) of an āyah.
  Word word(int surah, int ayah, int index) => Ayah(this, surah, ayah).word(index);

  /// Any run of positions, e.g. to render a selection.
  Span span(int start, int end) {
    if (start < 0 || start >= end || end > words.length) {
      throw RangeError('span $start:$end is outside the muṣḥaf');
    }
    return Span(this, start, end);
  }

  Span get all => Span(this, 0, words.length);
  List<Ayah> get ayahs => [for (var k = 0; k < ayahCount; k++) Ayah._fromIndex(this, k)];
  List<Page> get pages => [for (var n = 1; n <= pageCount; n++) Page(this, n)];
  List<Juz> get ajza => [for (var n = 1; n <= juzCount; n++) Juz(this, n)];

  // -- units by position --

  Word wordAt(int position) => Word(this, position);
  Ayah? ayahAt(int position) {
    final k = _indexOf(_ayahStarts, position);
    return k >= 0 ? Ayah._fromIndex(this, k) : null;
  }

  Surah surahAt(int position) => surahs[_indexOf(_surahStarts, position)];
  Page pageAt(int position) => Page(this, _indexOf(_pageStarts, position) + 1);
  Line? lineAt(int position) =>
      _lineStarts == null ? null : Line._fromIndex(this, _indexOf(_lineStarts!, position));
  Juz? juzAt(int position) =>
      _juzStarts == null ? null : Juz(this, _indexOf(_juzStarts!, position) + 1);

  List<Line> _linesBetween(int start, int end) {
    final starts = _lineStarts;
    if (starts == null) return const [];
    return [
      for (var i = _indexOf(starts, start); i <= _indexOf(starts, end - 1); i++)
        Line._fromIndex(this, i)
    ];
  }

  // -- the shared numbering --

  List<(int, int)> get _numbers {
    if (_numbersCache == null) {
      final block = _doc['numbering'] as Map<String, dynamic>;
      final missing = Set<int>.from(block['missing'] as List);
      final joined = {
        for (final j in block['written_joined'] as List)
          j['position'] as int: ((j['numbers'] as List)[0] as int, (j['numbers'] as List)[1] as int)
      };
      final runs = <(int, int)>[];
      var n = 1;
      for (var position = 0; position < words.length; position++) {
        while (missing.contains(n)) {
          n++;
        }
        final run = joined[position] ?? (n, n);
        runs.add(run);
        n = run.$2 + 1;
      }
      _numbersCache = runs;
    }
    return _numbersCache!;
  }

  /// The shared numbers this riwāyah does not read.
  late final Set<int> missingNumbers = Set<int>.from((_doc['numbering'] as Map)['missing'] as List);

  /// The shared number of the word at [position].
  int numberAt(int position) => _numbers[position].$1;

  /// The printed word carrying a shared number; null where this muṣḥaf does not read it.
  Word? wordByNumber(int number) {
    final runs = _numbers;
    var lo = 0, hi = runs.length;
    while (lo < hi) {
      final mid = (lo + hi) >> 1;
      if (runs[mid].$1 <= number) {
        lo = mid + 1;
      } else {
        hi = mid;
      }
    }
    final i = lo - 1;
    return i >= 0 && runs[i].$1 <= number && number <= runs[i].$2 ? Word(this, i) : null;
  }

  // -- signs and search --

  /// Every āyah printed with ۩.
  List<Ayah> sajdat() => [for (final p in _positionsWith(MarkKind.sajdah)) ayahAt(p)!];

  /// Every word printed with ۞ before it, as the release prints them.
  List<Word> divisionMarks() => [for (final p in _positionsWith(MarkKind.division)) Word(this, p)];

  List<int> _positionsWith(MarkKind kind) => [
        for (final e in _marksAt.entries)
          if (e.value.any((mk) => mk.kind == kind)) e.key
      ]..sort();

  /// Every place the words of [text] occur in sequence, matched on [fold]:
  /// harakah and hamzah forms do not matter.
  List<Span> search(String text) {
    final query = text.trim().split(RegExp(r'\s+')).where((t) => t.isNotEmpty).map(fold).toList();
    if (query.isEmpty || query.any((q) => q.isEmpty)) return const [];
    final folded = _foldCache ??= words.map(fold).toList();
    final n = query.length;
    final out = <Span>[];
    for (var i = 0; i + n <= folded.length; i++) {
      if (folded[i] != query[0]) continue;
      var ok = true;
      for (var j = 1; j < n; j++) {
        if (folded[i + j] != query[j]) {
          ok = false;
          break;
        }
      }
      if (ok) out.add(Span(this, i, i + n));
    }
    return out;
  }

  int _surahOfAyahIndex(int k) => _indexOf(_surahFirstAyah, k);
  int _ayahNumber(int k) => k - _surahFirstAyah[_surahOfAyahIndex(k)] + 1;

  @override
  String toString() => 'Mushaf($key)';
}

// --- āyah map ----------------------------------------------------------------

/// Where a Kūfī āyah falls in one edition.  [relation] is same, merged,
/// split (then [ayahLast] is set), shifted or unnumbered ([ayah] is 0).
class MappedAyah {
  final int surah;
  final int ayah;
  final String relation;
  final int? ayahLast;
  const MappedAyah(this.surah, this.ayah, this.relation, [this.ayahLast]);

  /// "2:253-254"
  String get key => ayahLast != null ? '$surah:$ayah-$ayahLast' : '$surah:$ayah';
  @override
  String toString() => key;
}

/// `data/ayah-map.json`: what a Ḥafṣ (Kūfī) reference is in every edition.
class AyahMap {
  final List<String> editions;
  final Map<String, Map<String, dynamic>> _rows;

  AyahMap._(this.editions, this._rows);

  factory AyahMap.fromJson(Object data) {
    final doc = data is String ? jsonDecode(data) : data;
    if (doc is! Map<String, dynamic> || doc['format'] != 'quran-ayah-map') {
      throw ArgumentError('not a quran-ayah-map file');
    }
    return AyahMap._(List<String>.from(doc['editions'] as List), {
      for (final r in doc['ayahs'] as List) '${r['surah']}:${r['ayah']}': r as Map<String, dynamic>
    });
  }

  /// `convert(2, 255, 'warsh')` → `MappedAyah(2, 253, 'split', 254)`
  MappedAyah convert(int surah, int ayah, String to) {
    final row = _rows['$surah:$ayah'];
    if (row == null) throw RangeError('$surah:$ayah is not a Kūfī āyah');
    final r = row[to];
    if (r == null) throw ArgumentError('no edition "$to"; editions are $editions');
    return MappedAyah(r['surah'] as int, r['ayah'] as int, r['relation'] as String, r['ayah_last'] as int?);
  }

  /// The reference in every edition.
  Map<String, MappedAyah> all(int surah, int ayah) =>
      {for (final e in editions) e: convert(surah, ayah, e)};
}

// --- word index --------------------------------------------------------------

/// One record of `data/word-index.json`: a shared number and what it is.
class IndexedWord {
  final Map<String, dynamic> raw;
  const IndexedWord(this.raw);

  int get number => raw['number'] as int;
  int get surah => raw['surah'] as int;
  int get index => raw['index'] as int;
  String get key => raw['key'] as String;
  String get rasm_uthmani => raw['rasm_uthmani'] as String;
  String get plain => raw['plain'] as String;
  String get rasm => raw['rasm'] as String;
  String get pointed => raw['pointed'] as String;
  String get status => raw['status'] as String;

  /// `{surah, ayah, position}` in the Kūfī count, or null where Ḥafṣ lacks the word.
  Map<String, dynamic>? get hafs => raw['hafs'] as Map<String, dynamic>?;

  /// Āyah number per riwāyah.
  Map<String, int> get ayah => Map<String, int>.from(raw['ayah'] as Map);

  /// Each riwāyah's own spelling; absent where it does not read the word.
  Map<String, String> get forms => Map<String, String>.from(raw['forms'] as Map);
  List<Map<String, dynamic>> get groups =>
      List<Map<String, dynamic>>.from(raw['groups'] as List? ?? const []);
  List<String> get missing => List<String>.from(raw['missing'] as List? ?? const []);
  List<String> get writtenJoined => List<String>.from(raw['written_joined'] as List? ?? const []);

  /// How one riwāyah spells it; null where it does not read the word.
  String? form(String riwayah) => (raw['forms'] as Map)[riwayah] as String?;
  @override
  String toString() => '$number $rasm_uthmani';
}

/// `data/word-index.json`: the numbering shared by all seven muṣḥafs.
class WordIndex extends Iterable<IndexedWord> {
  final List<String> mushafs;
  final int total;
  final List _words;
  Map<String, Map<String, dynamic>>? _byHafs;
  Map<String, List<Map<String, dynamic>>>? _byPlain;

  WordIndex._(this.mushafs, this.total, this._words);

  factory WordIndex.fromJson(Object data) {
    final doc = data is String ? jsonDecode(data) : data;
    if (doc is! Map<String, dynamic> || doc['format'] != 'quran-word-index') {
      throw ArgumentError('not a quran-word-index file');
    }
    return WordIndex._(List<String>.from(doc['mushafs'] as List), doc['total'] as int, doc['words'] as List);
  }

  IndexedWord word(int number) {
    if (number < 1 || number > total) throw RangeError('number $number: the numbering is 1 … $total');
    return IndexedWord(_words[number - 1] as Map<String, dynamic>);
  }

  /// By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word.
  IndexedWord? find(int surah, int ayah, int index) {
    _byHafs ??= {
      for (final r in _words.cast<Map<String, dynamic>>())
        if (r['hafs'] != null) '${r['hafs']['surah']}:${r['hafs']['ayah']}:${r['hafs']['position']}': r
    };
    final r = _byHafs!['$surah:$ayah:$index'];
    return r == null ? null : IndexedWord(r);
  }

  /// Every number whose folded spelling equals [text], folded.
  List<IndexedWord> search(String text) {
    if (_byPlain == null) {
      final by = <String, List<Map<String, dynamic>>>{};
      for (final r in _words.cast<Map<String, dynamic>>()) {
        by.putIfAbsent(fold(r['rasm_uthmani'] as String), () => []).add(r);
      }
      _byPlain = by;
    }
    return [for (final r in _byPlain![fold(text)] ?? const []) IndexedWord(r)];
  }

  /// Every number the riwāyāt spell in more than one way.
  List<IndexedWord> differing() => [
        for (final r in _words.cast<Map<String, dynamic>>())
          if (r.containsKey('groups')) IndexedWord(r)
      ];

  @override
  int get length => total;
  @override
  Iterator<IndexedWord> get iterator =>
      _words.map((r) => IndexedWord(r as Map<String, dynamic>)).iterator;
}
