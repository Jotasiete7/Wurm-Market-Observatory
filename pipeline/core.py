"""
core.py — Wurm Log Parser & Cleaner
Reads restored .txt corpus files and returns structured data.
No network. No database. Everything runs locally.
"""

import re
import json
from pathlib import Path
from datetime import date, timedelta
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Callable

# ─── Regex Patterns ──────────────────────────────────────────────────────────

DAY_RE   = re.compile(r'^Logging started (\d{4}-\d{2}-\d{2})')
LINE_RE  = re.compile(r'^\[(\d{2}:\d{2}:\d{2})\] <([^>]+)> \(([^)]+)\)\s+(.*)')
SYS_RE   = re.compile(r'^\[\d{2}:\d{2}:\d{2}\] <System>')


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class LogLine:
    timestamp: str
    player:    str
    server:    str
    message:   str
    day:       date


@dataclass
class ParseResult:
    lines:           list   = field(default_factory=list)   # list[LogLine]
    days_found:      set    = field(default_factory=set)    # set[date]
    total_raw_lines: int    = 0
    skipped_lines:   int    = 0
    file_path:       str    = ""
    period_start:    date   = None
    period_end:      date   = None
    servers_found:   set    = field(default_factory=set)    # set[str]


@dataclass
class CoverageResult:
    days_found:    list  = field(default_factory=list)   # sorted list[date]
    days_expected: list  = field(default_factory=list)   # all days in period
    gaps:          list  = field(default_factory=list)   # list[dict]
    coverage_pct:  float = 0.0


# ─── Parser ──────────────────────────────────────────────────────────────────

def parse_file(path: str | Path, config: dict, progress_cb: Callable = None) -> ParseResult:
    """
    Read a restored Wurm .txt corpus file line by line.
    Returns a ParseResult with all valid log lines.
    """
    result      = ParseResult(file_path=str(path))
    current_day = None
    cleaning    = config.get("cleaning", {})
    filter_sys  = cleaning.get("filter_system_messages", True)
    min_len     = cleaning.get("min_message_length", 5)
    seen        = set()  # for duplicate removal

    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    total = len(lines)
    result.total_raw_lines = total

    for i, raw in enumerate(lines):
        if progress_cb and i % 5000 == 0:
            progress_cb(i, total)

        line = raw.strip()
        if not line:
            continue

        # Day boundary
        day_m = DAY_RE.match(line)
        if day_m:
            current_day = date.fromisoformat(day_m.group(1))
            result.days_found.add(current_day)
            continue

        if current_day is None:
            result.skipped_lines += 1
            continue

        # Filter system messages
        if filter_sys and SYS_RE.match(line):
            result.skipped_lines += 1
            continue

        # Parse the message
        m = LINE_RE.match(line)
        if not m:
            result.skipped_lines += 1
            continue

        timestamp = m.group(1)
        player    = m.group(2).strip()
        server    = m.group(3).strip()
        message   = m.group(4).strip()

        # Minimum length check
        if len(message) < min_len:
            result.skipped_lines += 1
            continue

        # Duplicate removal (same player + message on same day)
        dedup_key = f"{current_day}|{player}|{message}"
        if cleaning.get("remove_duplicate_lines", True):
            if dedup_key in seen:
                result.skipped_lines += 1
                continue
            seen.add(dedup_key)

        result.servers_found.add(server)
        result.lines.append(LogLine(
            timestamp=timestamp,
            player=player,
            server=server,
            message=message,
            day=current_day
        ))

    if result.days_found:
        result.period_start = min(result.days_found)
        result.period_end   = max(result.days_found)

    return result


# ─── Coverage Calculator ─────────────────────────────────────────────────────

def compute_coverage(result: ParseResult) -> CoverageResult:
    """
    Given a ParseResult, compute coverage, expected days, and gaps.
    A gap is any stretch of consecutive missing days within the period.
    """
    cov = CoverageResult()
    if not result.period_start or not result.period_end:
        return cov

    # All expected days in the period
    current = result.period_start
    while current <= result.period_end:
        cov.days_expected.append(current)
        current += timedelta(days=1)

    found_set    = result.days_found
    cov.days_found = sorted(found_set)

    # Compute coverage %
    if cov.days_expected:
        cov.coverage_pct = len(found_set) / len(cov.days_expected)

    # Gap detection: find runs of missing days
    missing = [d for d in cov.days_expected if d not in found_set]
    if missing:
        runs = []
        run_start = missing[0]
        prev      = missing[0]
        for d in missing[1:]:
            if (d - prev).days == 1:
                prev = d
            else:
                runs.append((run_start, prev))
                run_start = d
                prev      = d
        runs.append((run_start, prev))

        for (gs, ge) in runs:
            label = (f"{gs.strftime('%b %-d')}–{ge.strftime('%-d')}"
                     if gs.month == ge.month
                     else f"{gs.strftime('%b %-d')}–{ge.strftime('%b %-d')}")
            # Windows strftime doesn't support %-d, use lstrip('0')
            try:
                label = label  # may fail on windows
            except Exception:
                label = f"{gs.isoformat()} – {ge.isoformat()}"

            cov.gaps.append({
                "start": gs.isoformat(),
                "end":   ge.isoformat(),
                "label": _fmt_gap_label(gs, ge)
            })

    return cov


def _fmt_gap_label(gs: date, ge: date) -> str:
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    ms = months[gs.month - 1]
    me = months[ge.month - 1]
    if gs == ge:
        return f"{ms} {gs.day}"
    elif gs.month == ge.month:
        return f"{ms} {gs.day}–{ge.day}"
    else:
        return f"{ms} {gs.day} – {me} {ge.day}"


# ─── Corpus Meta Generator ───────────────────────────────────────────────────

def build_corpus_meta(result: ParseResult, cov: CoverageResult, config: dict) -> dict:
    """
    Build the corpus-meta.json structure the Observatory expects.
    """
    obs_cfg = config.get("observatory", {})
    server  = obs_cfg.get("server", "SFI")
    pv      = obs_cfg.get("pipeline_version", "1.0.0")
    path    = Path(result.file_path)

    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    active = {
        "filename":         path.name,
        "server":           server,
        "period":           _period_label(result.period_start, result.period_end),
        "period_start":     result.period_start.isoformat() if result.period_start else "",
        "period_end":       result.period_end.isoformat()   if result.period_end   else "",
        "coverage":         round(cov.coverage_pct, 4),
        "log_lines":        len(result.lines),
        "gaps":             cov.gaps,
        "generated_at":     today,
        "pipeline_version": pv
    }

    # Build all_corpora: one entry per month in the period
    all_corpora = []
    if result.period_start and result.period_end:
        # Group found days by month
        month_days = defaultdict(set)
        for d in cov.days_found:
            month_days[(d.year, d.month)].add(d)

        current = date(result.period_start.year, result.period_start.month, 1)
        end     = date(result.period_end.year,   result.period_end.month,   1)
        months  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

        while current <= end:
            yr, mo   = current.year, current.month
            days_in  = (date(yr, mo % 12 + 1, 1) - timedelta(days=1)).day if mo < 12 else 31
            found_mo = len(month_days.get((yr, mo), set()))
            cov_mo   = round(found_mo / days_in, 4)
            label    = f"{months[mo-1]} {yr}"
            all_corpora.append({"month": label, "coverage": cov_mo, "server": server})

            # Advance one month
            if mo == 12:
                current = date(yr + 1, 1, 1)
            else:
                current = date(yr, mo + 1, 1)

    return {"active": active, "all_corpora": all_corpora}


def _period_label(start: date, end: date) -> str:
    if not start or not end:
        return "Unknown"
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if start.year == end.year and start.month == end.month:
        return f"{months[start.month-1]} {start.year}"
    elif start.year == end.year:
        return f"{months[start.month-1]}–{months[end.month-1]} {start.year}"
    else:
        return f"{months[start.month-1]} {start.year} – {months[end.month-1]} {end.year}"
