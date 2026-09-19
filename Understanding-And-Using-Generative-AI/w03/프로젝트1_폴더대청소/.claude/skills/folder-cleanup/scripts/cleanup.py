#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""folder-cleanup 보조 스크립트 (파이썬 표준 라이브러리만 사용)

  scan   SRC                    인벤토리 보고서 출력 + 원본 스냅샷 저장
  copy   SRC PLAN OUT           계획대로 복사 (사전 점검 통과 시에만, 덮어쓰기 없음)
  verify SRC PLAN OUT [--log]   개수·누락·중복배치·내용·원본무변경 검산, 정리로그 작성

PLAN은 탭으로 구분한 텍스트 파일이다. 한 줄이 파일 하나이고 열은 아래와 같다.
  원본상대경로 <TAB> 새폴더(/로 구분, 비우면 루트) <TAB> 새이름 <TAB> 비고(선택)
'#'으로 시작하는 줄과 빈 줄은 무시한다.

안전 원칙: 원본(SRC)은 읽기만 한다. 이 파일에는 삭제·이동·이름변경 코드가 없고,
쓰기는 OUT 폴더(정리된폴더/, 정리로그.md)와 스냅샷 파일에서만 일어난다.
"""
import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SORTED_DIR = "정리된폴더"
LOG_NAME = "정리로그.md"
SMALL_FILE = 64  # 이 크기 이하 파일은 해시가 같아도 진짜 중복인지 알 수 없다(더미·placeholder 가능)
TEXT_EXT = {".txt", ".md", ".csv", ".tsv", ".json", ".log", ".ini", ".yml", ".yaml", ".xml", ".html"}
RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
BAD_CHARS = re.compile(r'[<>:"|?*\x00-\x1f]')

AMBIGUOUS = re.compile(
    r"^(무제|제목\s*없음|untitled|새\s*(텍스트\s*)?문서|새\s*파일|메모장?|임시|temp|tmp|test|테스트|noname|"
    r"image\d*|img[_\-]?\d+|dsc[_\-]?\d+|pxl[_\-]?\d+|photo\d*|scan\d*|스크린샷|screenshot|screen\s*shot|"
    r"kakaotalk|카카오톡|download|다운로드|document\d*|문서\d*)",
    re.I,
)
TEMP_MARK = re.compile(r"(임시|temp|tmp|백업|backup)", re.I)


# ---------------------------------------------------------------- 공통 도구
def nfc(s):
    return unicodedata.normalize("NFC", s)


def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def fmt_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n} B" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_inside(child, parent):
    try:
        Path(child).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def code(s):
    """마크다운 코드 표기. 표 안에서 깨지지 않게 | 를 이스케이프한다."""
    s = str(s).replace("|", "\\|")
    return f"`` {s} ``" if "`" in s else f"`{s}`"


def walk_files(root, exclude=()):
    """root 아래 일반 파일 목록. 심볼릭 링크는 건너뛴다. rel은 항상 '/' 구분."""
    root = os.path.abspath(root)
    ex = {os.path.normcase(os.path.abspath(e)) for e in exclude}
    files, skipped, errors = [], [], []
    for cur, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if os.path.normcase(os.path.abspath(os.path.join(cur, d))) not in ex)
        for n in sorted(names):
            p = os.path.join(cur, n)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if os.path.islink(p):
                skipped.append(rel)
                continue
            try:
                st = os.stat(p)
            except OSError as e:
                errors.append(f"{rel}: {e}")
                continue
            files.append({"rel": rel, "size": st.st_size, "mtime_ns": st.st_mtime_ns})
    return files, skipped, errors


def take_snapshot(src, quick=False, exclude=()):
    files, skipped, errors = walk_files(src, exclude)
    if not quick:
        for f in files:
            try:
                f["md5"] = md5_of(os.path.join(src, f["rel"]))
            except OSError as e:
                f["md5"] = None
                errors.append(f"{f['rel']}: {e}")
    return {"src": os.path.abspath(src), "created": now(), "hash": "none" if quick else "md5",
            "files": files, "skipped_links": skipped, "errors": errors}


def diff_snapshot(src, snap, exclude=(), rehash=True):
    """스냅샷 이후 원본이 바뀌었는지: (삭제됨, 새로 생김, 바뀜) 목록."""
    files, _, _ = walk_files(src, exclude)
    cur = {nfc(f["rel"]): f for f in files}
    old = {nfc(f["rel"]): f for f in snap["files"]}
    deleted = sorted(old[k]["rel"] for k in old if k not in cur)
    added = sorted(cur[k]["rel"] for k in cur if k not in old)
    changed = []
    for k, o in old.items():
        c = cur.get(k)
        if not c:
            continue
        if c["size"] != o["size"] or c["mtime_ns"] != o["mtime_ns"]:
            changed.append(f"{o['rel']} (크기·수정시각 변경)")
        elif rehash and snap.get("hash") == "md5" and o.get("md5"):
            if md5_of(os.path.join(src, c["rel"])) != o["md5"]:
                changed.append(f"{o['rel']} (내용 변경)")
    return deleted, added, changed


def load_plan(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\r\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            c = line.split("\t")
            if len(c) < 3:
                sys.exit(f"계획 파일 {i}행: 열이 3개 미만입니다 (원본<TAB>새폴더<TAB>새이름[<TAB>비고]): {line[:60]}")
            rows.append({
                "orig": c[0],
                "folder": c[1].strip().replace("\\", "/").strip("/"),
                "new": c[2].strip(),
                "note": c[3].strip() if len(c) > 3 else "",
            })
    return rows


def dest_key(r):
    return nfc(f"{r['folder']}/{r['new']}" if r["folder"] else r["new"])


def coverage(rows, src_files):
    """계획이 원본 파일을 빠짐없이, 한 번씩만 다루는지."""
    idx = {nfc(f["rel"]): f["rel"] for f in src_files}
    seen = defaultdict(list)
    for r in rows:
        seen[nfc(r["orig"])].append(r["orig"])
    missing_in_plan = sorted(idx[k] for k in idx if k not in seen)
    unknown_in_plan = sorted(v[0] for k, v in seen.items() if k not in idx)
    dup_orig = sorted(v[0] for k, v in seen.items() if len(v) > 1)
    return missing_in_plan, unknown_in_plan, dup_orig


def validate_plan(rows, sorted_dir):
    problems = []
    seen_dest = defaultdict(list)
    for r in rows:
        tag = f"'{r['orig']}'"
        name, folder = r["new"], r["folder"]
        if not name:
            problems.append(f"{tag}: 새 이름이 비어 있음")
            continue
        if "/" in name or "\\" in name or BAD_CHARS.search(name):
            problems.append(f"{tag}: 새 이름 '{name}'에 쓸 수 없는 문자가 있음")
        if name.endswith("."):
            problems.append(f"{tag}: 새 이름 '{name}'이 마침표로 끝남")
        if Path(name).stem.upper() in RESERVED:
            problems.append(f"{tag}: 새 이름 '{name}'은 윈도우 예약어")
        if Path(r["orig"]).suffix.lower() != Path(name).suffix.lower():
            problems.append(f"{tag}: 확장자가 바뀜 ({Path(r['orig']).suffix or '없음'} → {Path(name).suffix or '없음'})")
        parts = folder.split("/") if folder else []
        for part in parts:
            if part in ("", ".", "..") or BAD_CHARS.search(part) or part != part.strip() or part.endswith(".") or part.upper() in RESERVED:
                problems.append(f"{tag}: 새 폴더 '{folder}'의 '{part}' 부분을 쓸 수 없음")
        if len(os.path.join(str(sorted_dir), *parts, name)) > 240:
            problems.append(f"{tag}: 복사될 경로가 너무 김(240자 초과)")
        seen_dest[dest_key(r).casefold()].append(r["orig"])
    for k, v in seen_dest.items():
        if len(v) > 1:
            problems.append(f"새 경로 충돌(대소문자 무시) '{k}' ← {', '.join(v)}")
    return problems


# ---------------------------------------------------------------- scan
def norm_stem(stem):
    s = re.sub(r"\s*[-_]?\s*(복사본|copy)(\s*\(\d+\))?", "", stem, flags=re.I)
    s = re.sub(r"\s*\(\d+\)", "", s)
    s = re.sub(r"(?:[\s_\-.]+|^)(?:v|ver)\.?\d+(?:\.\d+)*(?=$|[\s_\-.])", "", s, flags=re.I)
    s = re.sub(r"[\s_\-.]*(?:진짜최종|최최종|최종본|최종|final|draft|초안|사본|수정본|수정|backup|백업|old)", "", s, flags=re.I)
    return s.strip(" _-.")


def preview(path):
    text = None
    for enc in ("utf-8-sig", "cp949"):
        try:
            with open(path, encoding=enc) as f:
                text = f.read(2048)
            break
        except UnicodeDecodeError:
            continue
        except OSError:
            return None
    if text is None:
        return None
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()][:2]
    return " / ".join(ln[:80] for ln in lines) or "(내용 없음)"


def cmd_scan(a):
    src = Path(a.src).expanduser()
    if not src.is_dir():
        sys.exit(f"폴더가 아닙니다: {src}")
    src = src.resolve()
    if src.parent == src or src == Path.home():
        sys.exit("드라이브 루트나 홈 폴더 전체는 정리 대상으로 삼지 않습니다. 하위 폴더를 지정하세요.")
    snap = take_snapshot(src, a.quick, exclude=a.exclude or [])
    files = snap["files"]
    snap_path = a.snapshot or os.path.join(
        tempfile.gettempdir(), f"folder-cleanup-snapshot-{src.name}-{datetime.now():%Y%m%d-%H%M%S}.json")
    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1)

    total = sum(f["size"] for f in files)
    n_dirs = sum(len(d) for _, d, _ in os.walk(src))
    print(f"# 인벤토리: {src}\n")
    print(f"- 파일 {len(files)}개 / 하위 폴더 {n_dirs}개 / 총 {fmt_size(total)}")
    if snap["skipped_links"]:
        print(f"- 심볼릭 링크 {len(snap['skipped_links'])}개는 건너뜀")
    for e in snap["errors"]:
        print(f"- 읽기 오류: {e}")
    if len(files) > 2000:
        print("- 경고: 파일이 2000개를 넘습니다. 하위 폴더 하나씩 나눠서 정리하는 것을 권합니다.")
    if total > 2 * 1024 ** 3 and not a.quick:
        print("- 참고: 총 용량이 2GB를 넘습니다. 해시 계산이 오래 걸리면 --quick(크기만 비교)을 쓰세요.")

    by_ext = defaultdict(lambda: [0, 0])
    for f in files:
        e = Path(f["rel"]).suffix.lower() or "(확장자 없음)"
        by_ext[e][0] += 1
        by_ext[e][1] += f["size"]
    print("\n## 종류별 분포\n\n| 확장자 | 개수 | 용량 |\n|---|---|---|")
    for e, (n, sz) in sorted(by_ext.items(), key=lambda kv: (-kv[1][0], kv[0])):
        print(f"| {e} | {n} | {fmt_size(sz)} |")
    if n_dirs:
        tops = Counter(f["rel"].split("/")[0] if "/" in f["rel"] else "(루트)" for f in files)
        print("\n## 이미 있는 폴더 구조 (최상위 기준 파일 수)\n")
        for k, n in sorted(tops.items()):
            print(f"- {k}: {n}")

    print("\n## 눈에 띄는 문제")
    if snap["hash"] == "md5":
        groups = defaultdict(list)
        for f in files:
            if f.get("md5"):
                groups[(f["size"], f["md5"])].append(f)
        multi = [v for v in groups.values() if len(v) > 1]
        print("\n### 1. 내용이 같은 파일 (크기+MD5 일치)\n")
        if not multi:
            print("- 없음")
        for v in sorted(multi, key=lambda v: v[0]["rel"]):
            size = v[0]["size"]
            warn = " ← 빈 파일" if size == 0 else (" ← 작은 파일: 해시가 같아도 진짜 중복인지 내용 확인 필요" if size <= SMALL_FILE else "")
            print(f"- {len(v)}개 ({fmt_size(size)}){warn}: " + ", ".join(x["rel"] for x in v))
    else:
        print("\n### 1. 내용이 같은 파일\n\n- --quick 모드라 해시를 계산하지 않아 생략")

    ver = defaultdict(list)
    for f in files:
        p = Path(f["rel"])
        ver[(p.parent.as_posix(), norm_stem(p.stem).casefold(), p.suffix.lower())].append(p)
    print("\n### 2. 버전 의심 묶음 (이름에서 v1/최종/복사본/(1) 등을 뗀 뒤 같은 이름)\n")
    shown = False
    for (_, _, _), ps in sorted(ver.items()):
        if len(ps) >= 2 and any(norm_stem(p.stem) != p.stem.strip() for p in ps):
            print("- " + ", ".join(p.as_posix() for p in ps))
            shown = True
    if not shown:
        print("- 없음")

    ambiguous, tempmark, empties = [], [], []
    for f in files:
        stem = Path(f["rel"]).stem
        if f["size"] == 0:
            empties.append(f["rel"])
        if AMBIGUOUS.match(stem) or re.fullmatch(r"[\d\W_]+", stem) or len(stem) <= 2:
            ambiguous.append(f["rel"])
        elif TEMP_MARK.search(stem):
            tempmark.append(f["rel"])
    print("\n### 3. 이름만으로 내용을 알 수 없는 파일\n")
    print("\n".join(f"- {x}" for x in ambiguous) or "- 없음")
    print("\n### 4. 이름에 임시·백업 표시가 있는 파일\n")
    print("\n".join(f"- {x}" for x in tempmark) or "- 없음")
    print("\n### 5. 빈 파일(0바이트)\n")
    print("\n".join(f"- {x}" for x in empties) or "- 없음")

    if not a.no_preview:
        cand = [f for f in files if Path(f["rel"]).suffix.lower() in TEXT_EXT and 0 < f["size"] <= 2048][:60]
        if cand:
            print("\n## 작은 텍스트 파일 미리보기 (앞 2줄, 최대 60개)\n")
            for f in cand:
                pv = preview(os.path.join(src, f["rel"]))
                if pv is not None:
                    print(f"- {f['rel']}: {pv}")

    shown_n = 200
    print(f"\n## 전체 파일 목록 (크기 · 경로){' — 처음 200개만 표시' if len(files) > shown_n else ''}\n")
    for f in files[:shown_n]:
        print(f"- {fmt_size(f['size'])} · {f['rel']}")
    print(f"\n스냅샷 저장: {snap_path}  (해시 방식: {snap['hash']})")
    return 0


# ---------------------------------------------------------------- copy
def cmd_copy(a):
    src, out = Path(a.src).expanduser().resolve(), Path(a.out).expanduser().resolve()
    sd = out / SORTED_DIR
    problems = []
    if not src.is_dir():
        sys.exit(f"원본 폴더가 아닙니다: {src}")
    if is_inside(out, src):
        problems.append("결과 폴더(OUT)가 원본 폴더 안에 있습니다. 원본 밖으로 지정하세요.")
    if is_inside(src, sd):
        problems.append("원본 폴더가 결과 폴더 안에 있습니다.")
    rows = load_plan(a.plan)
    if not rows:
        problems.append("계획 파일에 행이 없습니다.")
    src_files, _, errs = walk_files(src, exclude=[out])
    problems += [f"원본 읽기 오류: {e}" for e in errs]

    snap_path = a.snapshot
    if snap_path:
        with open(snap_path, encoding="utf-8") as f:
            snap = json.load(f)
        deleted, added, changed = diff_snapshot(src, snap, exclude=[out], rehash=False)
        if deleted or added or changed:
            problems.append(f"scan 이후 원본이 바뀌었습니다 (삭제 {len(deleted)}, 추가 {len(added)}, 변경 {len(changed)}). 다시 scan 하세요.")
    else:
        snap = take_snapshot(src, quick=a.quick, exclude=[out])
        snap_path = os.path.join(tempfile.gettempdir(), f"folder-cleanup-snapshot-{src.name}-{datetime.now():%Y%m%d-%H%M%S}.json")
        if not a.dry_run:
            with open(snap_path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=1)
            print(f"(scan 스냅샷이 없어 지금 상태를 저장함: {snap_path})")

    missing, unknown, dups = coverage(rows, src_files)
    problems += [f"계획에 없는 원본 파일: {x}" for x in missing]
    problems += [f"원본에 없는 계획 행: {x}" for x in unknown]
    problems += [f"계획에 두 번 이상 나온 원본: {x}" for x in dups]
    problems += validate_plan(rows, sd)
    if sd.exists() and any(sd.rglob("*")):
        problems.append(f"결과 폴더 '{sd}'가 비어 있지 않습니다. 새 결과 폴더 경로를 쓰세요(덮어쓰지 않습니다).")

    if problems:
        print(f"사전 점검 실패 — 아무것도 복사하지 않았습니다 ({len(problems)}건)")
        for p in problems:
            print(f"- {p}")
        return 1
    print(f"사전 점검 통과: 원본 {len(src_files)}개 = 계획 {len(rows)}행, 충돌·덮어쓰기 없음")
    if a.dry_run:
        print("(--dry-run: 복사하지 않음)")
        return 0

    idx = {nfc(f["rel"]): f["rel"] for f in src_files}
    failed = 0
    for r in rows:
        dest = sd.joinpath(*(r["folder"].split("/") if r["folder"] else []), r["new"])
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src / idx[nfc(r["orig"])], dest)  # 원본은 읽기만
        except OSError as e:
            failed += 1
            print(f"복사 실패: {r['orig']} → {dest}: {e}")
    print(f"복사 {len(rows) - failed}/{len(rows)}건 완료 → {sd}")
    print("다음: verify 로 검산하고 --log 로 정리로그를 만드세요.")
    return 1 if failed else 0


# ---------------------------------------------------------------- verify / log
def dest_str(d):
    return f"{d['folder']}/{d['new']}" if d["folder"] else d["new"]


def items(names, limit=20):
    if not names:
        return "없음"
    shown = ", ".join(code(n) for n in names[:limit])
    return shown + (f" 외 {len(names) - limit}개" if len(names) > limit else "")


def verification_section(res, title):
    ok = lambda b: "O" if b else "**X**"
    L = [title, "", f"- 검증일시: {now()}",
         "- 방법: 원본 폴더와 정리된폴더를 다시 읽고, 정리 계획(원본→새 위치)과 서로 대조했다. 검증 중에는 어떤 파일도 만들거나 바꾸지 않았다.",
         f"- 내용 비교: {'크기만 비교(--quick)' if res['quick'] else '크기 + MD5'}", "",
         "### 개수 대조표", "", "| 항목 | 개수 | 일치 |", "|---|---|---|",
         f"| 원본 파일 수 | {res['src_n']} | |",
         f"| 정리된폴더 파일 수 (구버전·분류 보류 포함) | **{res['dst_n']}** | {ok(res['src_n'] == res['dst_n'])} |",
         f"| 계획 행 수 | {res['plan_n']} | {ok(res['src_n'] == res['plan_n'])} |", "",
         "### 폴더별 파일 수 (계획 vs 디스크)", "", "| 폴더 | 계획 | 디스크 | 일치 |", "|---|---|---|---|"]
    for folder, p, d in res["folder_rows"]:
        L.append(f"| {code(folder + '/' if folder != '(루트)' else folder)} | {p} | {d} | {ok(p == d)} |")
    L += ["", "### 누락 파일 목록", "", "| 검사 | 건수 | 파일 이름 |", "|---|---|---|"]
    for label, lst in (("원본에는 있는데 계획에 없는 파일", res["missing_in_plan"]),
                       ("계획에는 있는데 원본에 없는 파일", res["unknown_in_plan"]),
                       ("계획에는 있는데 정리된폴더에 복사본이 없는 파일", res["missing_copy"]),
                       ("원본과 복사본 내용이 다른 파일", [f"{n} ({why})" for n, why in res["bad_content"]])):
        L.append(f"| {label} | {len(lst)} | {items(lst)} |")
    L += ["", "### 중복 배치 목록", "", "| 검사 | 건수 | 파일 이름 |", "|---|---|---|",
          f"| 한 원본이 두 곳 이상에 배정된 경우 | {len(res['dup_orig'])} | {items(res['dup_orig'])} |",
          f"| 한 목적지에 두 원본이 배정된 경우 | {len(res['dup_dest'])} | {items(sorted(res['dup_dest']))} |",
          f"| 계획에 없는데 정리된폴더에 있는 파일 | {len(res['extras'])} | {items(res['extras'])} |",
          f"| 정리된폴더의 빈 폴더 | {len(res['empty_dirs'])} | {items(res['empty_dirs'])} |", ""]
    L += ["### 원본 무변경 확인", ""]
    if res["snapshot_used"]:
        L.append(f"복사 전 스냅샷(크기·수정시각{'' if res['quick'] else '·MD5'})과 지금의 원본을 비교했다. "
                 f"삭제 {len(res['deleted'])}건, 새로 생김 {len(res['added'])}건, 변경 {len(res['changed'])}건.")
        for label, lst in (("삭제됨", res["deleted"]), ("새로 생김", res["added"]), ("변경됨", res["changed"])):
            if lst:
                L.append(f"- {label}: {items(lst)}")
    else:
        L.append("스냅샷을 지정하지 않아 이 검사는 생략했다.")
    L += ["", "### 결론", ""]
    if res["passed"]:
        L.append(f"**원본 {res['src_n']}개 = 정리 후 {res['dst_n']}개로 일치한다.** 누락된 파일과 잘못 겹쳐 배치된 파일이 없다.")
    else:
        L.append(f"**검증 실패.** 원본 {res['src_n']}개, 정리 후 {res['dst_n']}개. 위 표의 항목을 확인하고 보완해야 한다.")
    return "\n".join(L) + "\n"


def dup_section(snap, plan_map):
    L = ["## 중복 후보 목록 (삭제하지 않음, 정리본에 모두 있음)", ""]
    if not snap or snap.get("hash") != "md5":
        return "\n".join(L + ["해시가 없어 자동 감지를 생략했다.", ""])
    groups = defaultdict(list)
    for f in snap["files"]:
        if f.get("md5"):
            groups[(f["size"], f["md5"])].append(f)
    multi = [(k, v) for k, v in groups.items() if len(v) > 1]
    if not multi:
        return "\n".join(L + ["내용(크기+MD5)이 완전히 같은 파일 묶음은 없다.", ""])
    L.append("크기와 MD5가 모두 같은 묶음이다. 어느 쪽을 남길지는 사람이 정한다.")
    if any(0 < k[0] <= SMALL_FILE for k, _ in multi):
        L.append(f"'작은 파일'(≤{SMALL_FILE}바이트) 묶음은 해시가 같아도 진짜 중복이 아닐 수 있다(더미·placeholder 등). "
                 "내용을 직접 확인하기 전에는 중복으로 판정하지 않는다.")
    L.append("")
    for (size, _), members in sorted(multi, key=lambda kv: kv[1][0]["rel"]):
        kind = " · 빈 파일" if size == 0 else (" · 작은 파일" if size <= SMALL_FILE else "")
        L.append(f"- **{len(members)}개 ({fmt_size(size)}{kind})**")
        for m in members:
            d = plan_map.get(nfc(m["rel"]))
            L.append(f"  - {code(m['rel'])} → {code(dest_str(d)) if d else '(계획에 없음)'}")
    L.append("")
    return "\n".join(L)


def build_log(src, sd, rows, res, snap, extra_text):
    plan_map = {nfc(r["orig"]): r for r in rows}
    verdict = f"**통과** — 원본 {res['src_n']}개 = 정리 후 {res['dst_n']}개" if res["passed"] else \
        f"**실패** — 원본 {res['src_n']}개, 정리 후 {res['dst_n']}개 (아래 검증 참고)"
    L = ["# 정리 로그", "",
         f"- 작업일시: {now()}",
         "- 방식: **복사** (원본은 수정·이동·삭제하지 않음)",
         f"- 원본: {code(src)} (파일 {res['src_n']}개)",
         f"- 결과: {code(sd)} (파일 {res['dst_n']}개)",
         f"- 검증: {verdict}", "",
         "## 폴더별 파일 수", "", "| 폴더 (정리된폴더 기준) | 파일 수 |", "|---|---|"]
    for folder, _, d in res["folder_rows"]:
        L.append(f"| {code(folder + '/' if folder != '(루트)' else folder)} | {d} |")
    L += ["", f"합계: {res['dst_n']}개", "", "## 원본 이름 → 새 위치 / 새 이름", "",
          "| # | 원본 이름 | 새 위치 | 새 이름 | 비고 |", "|---|---|---|---|---|"]
    for i, r in enumerate(sorted(rows, key=lambda r: (r["folder"], r["new"])), 1):
        loc = code(r["folder"] + "/") if r["folder"] else "(루트)"
        L.append(f"| {i} | {code(r['orig'])} | {loc} | {code(r['new'])} | {r['note'].replace('|', '/')} |")
    L.append("")
    L.append(dup_section(snap, plan_map))
    if extra_text:
        L.append(extra_text.strip() + "\n")
    L.append(verification_section(res, "## 검증"))
    return "\n".join(L)


def cmd_verify(a):
    src, out = Path(a.src).expanduser().resolve(), Path(a.out).expanduser().resolve()
    sd = out / SORTED_DIR
    rows = load_plan(a.plan)
    snap = None
    if a.snapshot:
        with open(a.snapshot, encoding="utf-8") as f:
            snap = json.load(f)
    quick = a.quick or (snap is not None and snap.get("hash") == "none")

    src_files, _, _ = walk_files(src, exclude=[out])
    dst_files = walk_files(sd)[0] if sd.is_dir() else []
    missing_in_plan, unknown_in_plan, dup_orig = coverage(rows, src_files)

    by_dest = defaultdict(list)
    for r in rows:
        by_dest[dest_key(r)].append(r)
    dup_dest = {k: [r["orig"] for r in v] for k, v in by_dest.items() if len(v) > 1}
    dst_idx = {nfc(f["rel"]): f for f in dst_files}
    src_idx = {nfc(f["rel"]): f for f in src_files}
    missing_copy = [r["orig"] for r in rows if dest_key(r) not in dst_idx]
    extras = [f["rel"] for f in dst_files if nfc(f["rel"]) not in by_dest]

    bad_content = []
    for r in rows:
        s, d = src_idx.get(nfc(r["orig"])), dst_idx.get(dest_key(r))
        if not s or not d:
            continue
        if s["size"] != d["size"]:
            bad_content.append((r["orig"], "크기 다름"))
        elif not quick and md5_of(src / s["rel"]) != md5_of(sd / d["rel"]):
            bad_content.append((r["orig"], "MD5 다름"))

    deleted = added = changed = []
    if snap:
        deleted, added, changed = diff_snapshot(src, snap, exclude=[out], rehash=not quick)

    plan_cnt = Counter(nfc(r["folder"]) or "(루트)" for r in rows)
    disk_cnt = Counter(nfc(posixpath.dirname(f["rel"])) or "(루트)" for f in dst_files)
    folder_rows = [(k, plan_cnt.get(k, 0), disk_cnt.get(k, 0)) for k in sorted(set(plan_cnt) | set(disk_cnt))]
    empty_dirs = []
    if sd.is_dir():
        for cur, dirs, names in os.walk(sd):
            if not dirs and not names and Path(cur) != sd:
                empty_dirs.append(os.path.relpath(cur, sd).replace(os.sep, "/"))

    res = {"src_n": len(src_files), "dst_n": len(dst_files), "plan_n": len(rows), "quick": quick,
           "missing_in_plan": missing_in_plan, "unknown_in_plan": unknown_in_plan, "dup_orig": dup_orig,
           "dup_dest": dup_dest, "missing_copy": missing_copy, "extras": extras, "bad_content": bad_content,
           "deleted": deleted, "added": added, "changed": changed, "folder_rows": folder_rows,
           "empty_dirs": empty_dirs, "snapshot_used": snap is not None}
    res["passed"] = (res["src_n"] == res["dst_n"] == res["plan_n"] and not any(
        [missing_in_plan, unknown_in_plan, dup_orig, dup_dest, missing_copy, extras, bad_content,
         deleted, added, changed, empty_dirs]))

    print(f"원본 {res['src_n']}개 / 정리 후 {res['dst_n']}개 / 계획 {res['plan_n']}행 → 개수 {'일치' if res['src_n'] == res['dst_n'] == res['plan_n'] else '불일치'} (개수만 본 결과. 파일 단위 검사는 아래)")
    for label, lst in (("계획에 없는 원본", missing_in_plan), ("원본에 없는 계획 행", unknown_in_plan),
                       ("복사본 없음", missing_copy), ("내용 다름", [f"{n} ({w})" for n, w in bad_content]),
                       ("원본 중복 배정", dup_orig), ("목적지 중복 배정", sorted(dup_dest)),
                       ("계획에 없는 정리본 파일", extras), ("빈 폴더", empty_dirs),
                       ("원본 삭제됨", deleted), ("원본에 새로 생김", added), ("원본 변경됨", changed)):
        print(f"- {label}: {len(lst)}건" + (" → " + ", ".join(lst[:20]) if lst else ""))
    if not snap:
        print("- 스냅샷 없음: 원본 무변경 검사는 생략")
    print("검증 결과: " + ("통과" if res["passed"] else "실패"))

    if a.log:
        log_path = out / LOG_NAME
        extra = ""
        if a.extra:
            try:
                extra = Path(a.extra).read_text(encoding="utf-8-sig")
            except OSError as e:
                print(f"--extra 파일을 읽지 못해 생략: {e}")
        out.mkdir(parents=True, exist_ok=True)
        if log_path.exists():
            with open(log_path, "a", encoding="utf-8", newline="\n") as f:
                f.write("\n" + verification_section(res, f"## 검증 (재검증 {now()})"))
            print(f"기존 정리로그 맨 아래에 재검증 결과를 추가함: {log_path}")
        else:
            with open(log_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(build_log(src, sd, rows, res, snap, extra))
            print(f"정리로그 저장: {log_path}")
    return 0 if res["passed"] else 1


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="folder-cleanup 보조 스크립트")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="인벤토리 보고 + 스냅샷")
    s.add_argument("src")
    s.add_argument("--snapshot", help="스냅샷 저장 경로(기본: 임시 폴더)")
    s.add_argument("--quick", action="store_true", help="해시 생략(크기만)")
    s.add_argument("--exclude", action="append", help="스캔에서 뺄 폴더(여러 번 지정 가능)")
    s.add_argument("--no-preview", action="store_true", help="텍스트 파일 미리보기 생략")
    c = sub.add_parser("copy", help="계획대로 복사")
    c.add_argument("src")
    c.add_argument("plan")
    c.add_argument("out")
    c.add_argument("--snapshot")
    c.add_argument("--quick", action="store_true")
    c.add_argument("--dry-run", action="store_true", help="사전 점검만 하고 복사하지 않음")
    v = sub.add_parser("verify", help="검산 (+ 정리로그)")
    v.add_argument("src")
    v.add_argument("plan")
    v.add_argument("out")
    v.add_argument("--snapshot")
    v.add_argument("--quick", action="store_true")
    v.add_argument("--log", action="store_true", help="OUT/정리로그.md 작성(있으면 맨 아래에 검증 추가)")
    v.add_argument("--extra", help="로그에 끼워 넣을 마크다운 파일(버전 처리·분류 보류·가정 등)")
    a = p.parse_args()
    sys.exit({"scan": cmd_scan, "copy": cmd_copy, "verify": cmd_verify}[a.cmd](a))


if __name__ == "__main__":
    main()
