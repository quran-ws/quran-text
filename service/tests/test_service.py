"""Run from service/:  .venv/bin/pytest"""

import csv
import hashlib
import io
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app  # noqa: E402

client = TestClient(app)

HEADER_MARK = "quran-text —"


def get(url, expect=200):
    r = client.get(url)
    assert r.status_code == expect, r.text[:300]
    return r


# --- every format is valid ---------------------------------------------------

def test_txt_default_is_one_ayah_per_line_with_prefix():
    body = get("/download?edition=hafs&format=txt&sura=112").text
    lines = [l for l in body.splitlines() if l and not l.startswith("#")]
    assert len(lines) == 4
    assert lines[0].startswith("112|1|قُلۡ هُوَ")
    assert body.startswith("# " + HEADER_MARK)


def test_json_is_valid_and_carries_provenance():
    doc = get("/download?edition=hafs&format=json&sura=1").json()
    assert doc["meta"]["source"]["package"] == "UthmanicHafs-v-3.0.zip"
    assert len(doc["meta"]["source"]["sha256"]) == 64
    assert doc["meta"]["license"].startswith("The text is the King Fahd")
    assert [a["ayah"] for a in doc["ayat"]] == list(range(1, 8))


def test_json_nested():
    doc = get("/download?edition=hafs&format=json&nested=1&sura=113-114").json()
    assert [s["number"] for s in doc["suras"]] == [113, 114]
    assert len(doc["suras"][1]["ayat"]) == 6
    assert "sura" not in doc["suras"][0]["ayat"][0]


def test_csv_parses():
    body = get("/download?edition=hafs&format=csv&sura=1&header=0").text
    rows = list(csv.reader(io.StringIO(body)))
    assert rows[0] == ["sura", "ayah", "text"]
    assert len(rows) == 8 and rows[1][:2] == ["1", "1"]


def test_xml_is_tanzil_compatible():
    body = get("/download?edition=hafs&format=xml&sura=112").text
    root = ET.fromstring(body)
    assert root.tag == "quran" and root.get("edition") == "hafs"
    sura = root.find("sura")
    assert sura.get("index") == "112" and sura.get("name")
    ayat = sura.findall("aya")
    assert [a.get("index") for a in ayat] == ["1", "2", "3", "4"]
    assert ayat[0].get("text").startswith("قُلۡ")


def test_sql_loads_into_sqlite():
    body = get("/download?edition=hafs&format=sql&sura=1&fields=sura,ayah,page").text
    db = sqlite3.connect(":memory:")
    db.executescript(body)
    assert db.execute("SELECT COUNT(*) FROM quran").fetchone()[0] == 7
    assert db.execute("SELECT page FROM quran WHERE ayah=1").fetchone()[0] == 1


def test_md_has_sura_heading():
    body = get("/download?edition=hafs&format=md&sura=114").text
    assert "## 114." in body and "`114:1`" in body
    assert "<" not in body.split("\n\n", 1)[1]        # plain Markdown, no HTML per line


# --- options change the output as advertised ---------------------------------

def ayah_text(**params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    return get(f"/download?format=json&header=0&{q}").json()["ayat"][0]["text"]


def test_ayah_markers():
    assert ayah_text(edition="hafs", ayah="2:255", markers="sign").endswith(" ۝٢٥٥")
    assert ayah_text(edition="hafs", ayah="2:255", markers="brackets").endswith(" ﴿٢٥٥﴾")
    assert ayah_text(edition="hafs", ayah="2:255", markers="latin").endswith(" (255)")
    assert "۝" not in ayah_text(edition="hafs", ayah="2:255")


def test_waqf_marks_present_and_absent():
    with_marks = ayah_text(edition="hafs", ayah="2:255")
    without = ayah_text(edition="hafs", ayah="2:255", waqf=0)
    assert "ۚ" in with_marks and "ۚ" not in without
    assert with_marks.replace("ۚ", "").replace("ۗ", "").replace("ۖ", "") == without


def test_sajdah_and_hizb_signs():
    assert ayah_text(edition="hafs", ayah="7:206").endswith("۩")
    assert not ayah_text(edition="hafs", ayah="7:206", sajdah=0).endswith("۩")
    assert ayah_text(edition="hafs", ayah="2:26").startswith("۞ ")
    assert not ayah_text(edition="hafs", ayah="2:26", hizb=0).startswith("۞")


def test_lines_break_the_text():
    plain = ayah_text(edition="hafs", ayah="2:255")
    with_lines = ayah_text(edition="hafs", ayah="2:255", lines=1)
    assert "\n" not in plain and "\n" in with_lines
    assert with_lines.replace("\n", " ") == plain


def test_pages_in_txt():
    body = get("/download?edition=hafs&format=txt&sura=1&pages=1&header=0").text
    assert body.startswith("# page 1\n")


def test_text_forms():
    uth = ayah_text(edition="hafs", ayah="1:1")
    iml = ayah_text(edition="hafs", ayah="1:1", text="imlaei")
    plain = ayah_text(edition="hafs", ayah="1:1", text="plain")
    assert uth.startswith("بِسۡمِ ٱللَّهِ") and iml.startswith("بسم الله") and plain == "بسم الله الرحمان الرحيم"


def test_fields_and_hafs_reference_for_warsh():
    doc = get("/download?edition=warsh&format=json&fields=sura,ayah,page,line,juz,hafs&ayah=2:253").json()
    a = doc["ayat"][0]
    assert a["hafs"] == "2:255" and a["hafs_relation"] == "split"
    assert a["page"] and a["line"] and a["juz"] == 3


def test_per_word_records():
    doc = get("/download?edition=hafs&format=json&by=word&ayah=7:206").json()
    words = doc["words"]
    assert words[0]["pos"] == 1 and words[0]["number"] > 0
    assert words[-1]["sajdah"] == "۩" and words[-1]["waqf"] == "" and "hizb" in words[-1]
    assert "۩" not in words[-1]["text"]
    assert len(words) == 11


def test_per_word_signs_attached_or_in_columns():
    cols = get("/download?edition=hafs&format=csv&by=word&ayah=7:206&header=0").text.splitlines()[0]
    assert cols == "sura,ayah,pos,number,text,waqf,sajdah,hizb"
    cols = get("/download?edition=hafs&format=csv&by=word&ayah=7:206&header=0&sajdah=0").text.splitlines()[0]
    assert cols == "sura,ayah,pos,number,text,waqf,hizb"
    doc = get("/download?edition=hafs&format=json&by=word&ayah=7:206&signs=attached").json()
    last = doc["words"][-1]
    assert last["text"].endswith("۩") and "sajdah" not in last and "waqf" not in last
    hizb = get("/download?edition=hafs&format=json&by=word&ayah=2:26&signs=attached&header=0").json()["words"][0]
    assert hizb["text"].startswith("۞ ")
    plain = get("/download?edition=hafs&format=json&by=word&ayah=7:206&signs=attached&text=uthmani,plain&header=0").json()["words"][-1]
    assert plain["text"].endswith("۩") and not plain["plain"].endswith("۩")


def test_unnumbered_basmalah_is_ayah_zero_in_warsh():
    doc = get("/download?edition=warsh&format=json&sura=1").json()
    assert doc["ayat"][0]["ayah"] == 0 and doc["ayat"][0]["text"].startswith("بِسْمِ")
    assert len(doc["ayat"]) == 8
    doc = get("/download?edition=hafs&format=json&sura=1").json()
    assert doc["ayat"][0]["ayah"] == 1


def test_warsh_ayah_markers_render():
    body = get("/download?edition=warsh&format=txt&sura=1&markers=sign&header=0").text
    assert "۝٧" in body


def test_limit_previews():
    doc = get("/download?edition=hafs&format=json&limit=3").json()
    assert len(doc["ayat"]) == 3 and doc["meta"]["limited"] is True
    assert "limit" not in doc["meta"]["url"]


# --- scope validation and edition limits -------------------------------------

@pytest.mark.parametrize("url,fragment", [
    ("/download?edition=hafs&ayah=2:300", "286 āyāt in Ḥafṣ, not 300"),
    ("/download?edition=warsh&ayah=2:286", "285 āyāt in Warsh"),
    ("/download?edition=hafs&sura=115", "there are 114"),
    ("/download?edition=hafs&sura=3-2", "runs backwards"),
    ("/download?edition=hafs&page=605", "604 pages"),
    ("/download?edition=hafs&juz=31", "there are 30"),
    ("/download?edition=hafs&ayah=abc", "write sura:ayah"),
    ("/download?edition=hafs&sura=2&juz=1", "give one scope"),
    ("/download?edition=nope", "unknown edition"),
    ("/download?edition=hafs&fields=colour", "fields="),
])
def test_bad_requests(url, fragment):
    r = get(url, expect=400)
    assert fragment in r.json()["error"]


def test_bazzi_has_no_juz():
    assert "no juz layer" in get("/download?edition=bazzi&juz=1", 400).json()["error"]
    assert "no juz layer" in get("/download?edition=bazzi&fields=sura,ayah,juz", 400).json()["error"]
    assert get("/download?edition=bazzi&page=1").status_code == 200


def test_imlaei_only_for_hafs():
    assert "Ḥafṣ only" in get("/download?edition=warsh&text=imlaei", 400).json()["error"]
    assert get("/download?edition=hafs&text=imlaei&sura=1").status_code == 200


# --- headers -----------------------------------------------------------------

def test_checksum_and_disposition():
    r = get("/download?edition=warsh&format=json&sura=1")
    assert r.headers["x-checksum-sha256"] == hashlib.sha256(r.content).hexdigest()
    assert r.headers["content-disposition"] == "attachment; filename*=UTF-8''quran-warsh-uthmani-sura1.json"
    assert r.headers["content-type"].startswith("application/json")


# --- the rest of the API -----------------------------------------------------

def test_page_and_docs():
    assert "<title>quran-text" in get("/").text
    paths = get("/openapi.json").json()["paths"]
    assert {"/download", "/editions", "/compare", "/files"} <= set(paths)
    assert all(p["description"] for p in paths["/download"]["get"]["parameters"])


def test_editions():
    e = {x["key"]: x for x in get("/editions").json()}
    assert e["bazzi"]["has"]["juz"] is False and e["hafs"]["has"]["imlaei"] is True
    assert e["warsh"]["ayah_count"] == 6214


def test_compare():
    d = get("/compare?ayah=1:4").json()
    by = {e["key"]: e for e in d["editions"]}
    assert by["warsh"]["ref"] == "1:3" and by["hafs"]["ref"] == "1:4"
    assert by["hafs"]["words"][0]["differs"] is True      # مَٰلِكِ / مَلِكِ
    assert get("/compare?ayah=2:999", 400).json()["error"]


def test_files():
    files = get("/files").json()
    hafs = next(f for f in files if f["path"] == "mushaf/hafs.json")
    assert hafs["normative"] is True and len(hafs["sha256"]) == 64
    r = get("/files/catalog.json")
    assert json.loads(r.content)["format"] == "quran-catalog"
    get("/files/../app.py", 404)
    get("/files/nothing.json", 404)


def test_several_text_forms_become_columns():
    r = get("/download?edition=hafs&ayah=1:1&text=uthmani,imlaei,plain&format=csv&header=0")
    rows = list(csv.DictReader(io.StringIO(r.text)))
    assert list(rows[0].keys()) == ["sura", "ayah", "text", "imlaei", "plain"]
    assert rows[0]["imlaei"].startswith("بسم") and rows[0]["plain"].startswith("بسم")
    assert rows[0]["text"] != rows[0]["plain"]
    txt = get("/download?edition=hafs&ayah=1:1&text=uthmani,imlaei&header=0").text.strip()
    assert txt.count("|") == 3                     # sura|ayah|uthmani|imlaei
    j = get("/download?edition=hafs&ayah=1:1&text=imlaei,uthmani&format=json&header=0").json()
    assert set(j["ayat"][0]) == {"sura", "ayah", "text", "uthmani"}
    assert j["ayat"][0]["text"].startswith("بسم")
    assert get("/download?edition=hafs&ayah=1:1&text=uthmani,uthmani&format=csv&header=0").text.splitlines()[0] == "sura,ayah,text"
    assert "Ḥafṣ only" in get("/download?edition=warsh&text=uthmani,imlaei", 400).json()["error"]
    assert "text=" in get("/download?edition=hafs&text=uthmani,bogus", 400).json()["error"] or "bogus" in get("/download?edition=hafs&text=uthmani,bogus", 400).json()["error"]


def test_every_edition_has_a_sample_with_all_its_signs():
    for e in get("/editions").json():
        assert "sajdah" in e["sample"]["signs"] and "hizb" in e["sample"]["signs"], e["key"]
        if e["marks"].get("waqf"):
            assert "waqf" in e["sample"]["signs"], e["key"]
        body = get(f"/download?edition={e['key']}&ayah={e['sample']['ayah']}&header=0").text
        assert "۩" in body and "۞" in body, e["key"]


def test_map_dataset_by_ayah_and_by_word():
    d = get("/map?from=hafs&to=warsh&ayah=2:255").json()
    row = d["rows"][0]
    assert row["warsh_ayah"] == "2:253-254" and row["warsh_relation"] == "split"
    assert d["meta"]["columns"] == ["sura", "ayah", "first_number", "last_number", "warsh_ayah", "warsh_relation"]
    d = get("/map?from=warsh&ayah=2:253").json()
    assert d["meta"]["to"] == ["hafs", "shuba", "qaloun", "douri", "sousi", "bazzi"]
    assert d["rows"][0]["hafs_ayah"] == "2:255" and d["rows"][0]["douri_relation"] == "merged"
    assert get("/map?from=hafs&to=warsh&ayah=1:1").json()["rows"][0]["warsh_relation"] == "unnumbered"
    w = get("/map?from=hafs&to=warsh&ayah=57:24&by=word").json()["rows"]
    huwa = next(r for r in w if r["text"] == "هُوَ")
    assert huwa["warsh_word"] is None and huwa["warsh_text"] is None
    assert w[0]["warsh_word"].startswith("57:23:")
    csv_ = get("/map?from=hafs&to=warsh,douri&sura=1&format=csv&header=0").text.splitlines()
    assert csv_[0] == "sura,ayah,first_number,last_number,warsh_ayah,warsh_relation,douri_ayah,douri_relation"
    assert len(csv_) == 8
    whole = get("/map?from=hafs&to=warsh&format=csv&header=0").text.splitlines()
    assert len(whole) == 6237                            # every Kūfī āyah, once
    r = get("/map?from=hafs&to=warsh&sura=1&format=sql&header=0")
    con = sqlite3.connect(":memory:"); con.executescript(r.text)
    assert con.execute("select count(*) from quran_map").fetchone()[0] == 7
    assert ET.fromstring(get("/map?from=hafs&to=warsh&sura=1&format=xml").text).tag == "map"
    assert "no riwāyah" in get("/map?from=hafs&to=nope&ayah=2:255", 400).json()["error"]
    assert "being mapped from" in get("/map?from=hafs&to=hafs&ayah=2:255", 400).json()["error"]
