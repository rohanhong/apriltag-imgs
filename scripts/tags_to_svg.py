#!/usr/bin/env python3
"""Convert every tag PNG of every family into SVG with tag_to_svg.py.

For each tag<Family>/ directory under --src, writes one SVG per tag into
<out>/<Family>/ and a reproducible archive <out>/<Family>.tar.gz whose
entries are <Family>/<name>.svg. The SVG markup comes from
tag_to_svg.gen_apriltag_svg(), so it matches what tag_to_svg.py writes for
one tag (except that line endings are always LF).

The edge length of each SVG is --cell times the tag width in pixels, so all
families share the same cell size; for example --cell=2mm gives 20mm for a
10 x 10 tag and 22mm for an 11 x 11 tag.
"""

import argparse
import contextlib
import gzip
import io
import os
import re
import sys
import tarfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from decimal import Decimal

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from PIL import Image  # noqa: E402

from tag_to_svg import gen_apriltag_svg  # noqa: E402

FAMILY_RE = re.compile(r'^tag[A-Za-z0-9]+$')
TAG_RE = re.compile(r'^tag\d+_\d+_\d+\.png$')
CELL_RE = re.compile(r'^(\d+(?:\.\d+)?)(mm|cm|in|pt|pc|px)?$')
# The gzip header stores the timestamp as an unsigned 32-bit value.
MAX_MTIME = 2**32 - 1
# ProcessPoolExecutor on Windows accepts at most 61 workers.
MAX_WORKERS = 61 if os.name == 'nt' else 1024


def parse_cell(text):
    match = CELL_RE.match(text)
    if not match:
        raise argparse.ArgumentTypeError(
            f'"{text}" is not a length such as "2mm", "0.1in", or "20px".')
    return Decimal(match.group(1)), match.group(2) or ''


def parse_mtime(text):
    try:
        value = int(text)
    except ValueError:
        value = -1
    if not 0 <= value <= MAX_MTIME:
        raise argparse.ArgumentTypeError(
            f'"{text}" is not a whole number of seconds from 0 to {MAX_MTIME}.')
    return value


def parse_jobs(text):
    try:
        value = int(text)
    except ValueError:
        value = 0
    if value < 1:
        raise argparse.ArgumentTypeError(f'"{text}" is not a positive whole number.')
    return value


def format_size(cell, width):
    value, unit = cell
    text = f'{value * width:f}'
    if '.' in text:
        text = text.rstrip('0').rstrip('.')
    return text + unit


def find_families(src, names):
    found = sorted(d for d in os.listdir(src)
                   if FAMILY_RE.match(d) and os.path.isdir(os.path.join(src, d)))
    if not names:
        return found
    missing = sorted(set(names) - set(found))
    if missing:
        sys.exit(f'Error: no family directory under {src} for: {", ".join(missing)}')
    return [d for d in found if d in names]


def list_tags(src, family):
    return sorted(f for f in os.listdir(os.path.join(src, family)) if TAG_RE.match(f))


def convert_family(src, out, family, tags, cell, write_files, write_archive, mtime, level):
    svg_dir = os.path.join(out, family)
    if write_files:
        os.makedirs(svg_dir, exist_ok=True)

    archive = os.path.join(out, f'{family}.tar.gz') if write_archive else None
    part = archive + '.part' if archive else None
    sizes = set()
    try:
        # ExitStack closes tar, gzip, and file in turn even if one close fails.
        with contextlib.ExitStack() as stack:
            tar = None
            if archive:
                raw = stack.enter_context(open(part, 'wb'))
                # filename='' and a fixed mtime keep the gzip header reproducible.
                gz = stack.enter_context(gzip.GzipFile(
                    filename='', mode='wb', compresslevel=level, fileobj=raw, mtime=mtime))
                tar = stack.enter_context(tarfile.open(fileobj=gz, mode='w', format=tarfile.USTAR_FORMAT))
            for name in tags:
                with Image.open(os.path.join(src, family, name), 'r') as im:
                    width, height = im.size
                    size = format_size(cell, width)
                    svg = gen_apriltag_svg(width, height, im.load(), size).encode('ascii')
                sizes.add(size)
                svg_name = name[:-len('.png')] + '.svg'
                if write_files:
                    with open(os.path.join(svg_dir, svg_name), 'wb') as fp:
                        fp.write(svg)
                if tar is not None:
                    info = tarfile.TarInfo(f'{family}/{svg_name}')
                    info.size = len(svg)
                    info.mtime = mtime
                    info.mode = 0o644
                    tar.addfile(info, io.BytesIO(svg))
    except BaseException:
        # Never leave a truncated archive behind for git to pick up.
        if part:
            with contextlib.suppress(OSError):
                os.remove(part)
        raise
    if archive:
        os.replace(part, archive)

    archive_bytes = os.path.getsize(archive) if archive else 0
    return family, len(tags), sorted(sizes), archive_bytes


def main():
    parser = argparse.ArgumentParser(
        description='Convert all tag PNGs into SVG files and per-family tar.gz archives.',
        epilog='Example: "python scripts/tags_to_svg.py --cell=2mm"')
    parser.add_argument('--src', default=REPO_ROOT,
                        help='Directory holding the tag<Family>/ directories (default: repository root).')
    parser.add_argument('--out', default=os.path.join(REPO_ROOT, 'svg'),
                        help='Output directory (default: svg/ in the repository root).')
    parser.add_argument('--cell', type=parse_cell, default='2mm',
                        help='Edge length of one tag pixel (cell), such as "2mm" (default), "0.1in", "20px".')
    parser.add_argument('--families', nargs='+', metavar='FAMILY',
                        help='Convert only these families, such as "tag36h11" (default: all).')
    parser.add_argument('--no-files', dest='write_files', action='store_false',
                        help='Skip the loose SVG files; write archives only.')
    parser.add_argument('--no-archive', dest='write_archive', action='store_false',
                        help='Skip the tar.gz archives; write loose SVG files only.')
    parser.add_argument('--level', type=int, default=9, choices=range(1, 10), metavar='1-9',
                        help='gzip compression level (default: 9).')
    parser.add_argument('--mtime', type=parse_mtime,
                        help='Timestamp stored in the archives (default: $SOURCE_DATE_EPOCH, else 0).')
    parser.add_argument('--jobs', type=parse_jobs,
                        help='Number of worker processes (default: CPU count, at most one per family).')
    args = parser.parse_args()
    if not (args.write_files or args.write_archive):
        parser.error('--no-files and --no-archive together leave nothing to do.')
    if args.mtime is None:
        try:
            args.mtime = parse_mtime(os.environ.get('SOURCE_DATE_EPOCH', '0'))
        except argparse.ArgumentTypeError as err:
            parser.error(f'SOURCE_DATE_EPOCH: {err}')

    families = find_families(args.src, args.families)
    tags = {family: list_tags(args.src, family) for family in families}
    # Largest families first, so the longest jobs start earliest.
    families.sort(key=lambda family: -len(tags[family]))
    workers = min(args.jobs or os.cpu_count() or 1, len(families), MAX_WORKERS)
    os.makedirs(args.out, exist_ok=True)
    start = time.time()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        jobs = [pool.submit(convert_family, args.src, args.out, family, tags[family], args.cell,
                            args.write_files, args.write_archive, args.mtime, args.level)
                for family in families]
        total = 0
        for job in as_completed(jobs):
            family, count, sizes, archive_bytes = job.result()
            total += count
            archive_note = f', archive {archive_bytes / 2**20:.2f} MiB' if args.write_archive else ''
            print(f'{family}: {count} tags, size {", ".join(sizes)}{archive_note}', flush=True)
    print(f'Done: {total} tags from {len(families)} families into {args.out} in {time.time() - start:.0f} s')


if __name__ == '__main__':
    main()
