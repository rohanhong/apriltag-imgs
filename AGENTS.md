# Agent Instructions

Shared instructions for every AI agent tool working in this repository. This
file is the single source of instructions; edit it, never an adapter file.

## Project

AprilTag-imgs (fork): an unofficial fork of
[AprilRobotics/apriltag-imgs](https://github.com/AprilRobotics/apriltag-imgs),
which holds pre-generated images of every AprilTag 3 tag family. The fork adds
agent instructions, agent skills, documentation, and SVG archives of every
tag; the tag images and the upstream script are unchanged.

- `tag<Family>/`: one directory per tag family, each holding one PNG per tag
  (`tag<bits>_<hamming>_<id>.png`, 8 to 11 pixels wide), a `mosaic.png`, and an
  `alltags.ps` PostScript sheet. About 159,000 PNG files in total: never list
  these directories recursively or read them in full; count or sample them.
- `tag_to_svg.py`: converts one tag PNG into an SVG (Python 3 and Pillow).
- `scripts/tags_to_svg.py`: the fork's batch converter. It imports
  `tag_to_svg.py` and writes every tag of every family as an SVG, sized per
  cell (`--cell`, default 2mm, so a 10 x 10 tag is 20mm wide).
- `svg/<Family>.tar.gz`: tracked, reproducible archives of those SVGs
  (entries `<Family>/<name>.svg`), built at the default `--cell=2mm`, which
  the README size table documents. Regenerate them with the batch converter
  after any change to the tags or `tag_to_svg.py`; build other sizes into
  another `--out` directory. Rerunning with the same inputs, Python, and
  zlib build gives byte-identical archives; another zlib build (for example
  zlib-ng) may change the compressed bytes, not the SVGs.
- `svg/<Family>/`: the loose SVGs, git-ignored, about 159,000 files and
  1.4 GiB in total: same rule as the tag directories, never list or read them
  in full. They hold whatever the last run that wrote loose files produced
  (`--no-files` leaves them as they were); the script never deletes them.

## Commands

There is no build and no test suite.

- Convert a tag to SVG (needs `pip install Pillow`):
  `python3 tag_to_svg.py tagStandard52h13/tag52_13_00007.png tag52_13_00007.svg --size=20mm`
- Rebuild every tag into `svg/` (loose files and the tracked archives; about
  2.5 minutes, `--help` lists the options):
  `python3 scripts/tags_to_svg.py`
- Build another size outside the tracked archives:
  `python3 scripts/tags_to_svg.py --cell=5mm --out <dir>`
- Unpack one family's SVGs: `tar -xzf svg/tag36h11.tar.gz -C svg`
- Rescale a tag with ImageMagick:
  `convert <small_marker>.png -scale <percent>% <big_marker>.png`
- Check for non-ASCII text outside the README files:
  `LC_ALL=C git grep -nI '[^[:print:][:space:]]' -- . ':!README.md' ':!docs/i18n'`
  prints nothing.

## Conventions

- Commits and branching follow `.gitmessage` (see its `Workflow:` and
  `Adopted:` lines).
- The trunk is `master`, as upstream names it, on origin and locally. The
  skills and `.gitmessage` say `main`: read every `main` there as `master`,
  with the same rules (see the Trunk name note in `.gitmessage`). Never
  create a `main` branch.
- Use the git-* skills for git operations. `.gitmessage` is normative for
  the repository's commit and merge messages;
  `.agents/skills/git-commit/references/message-spec.md` is the skills'
  detailed reading of it and defers to `.gitmessage` on any conflict.
- `README.md` is canonical English; each translation
  (`docs/i18n/README.<locale>.md`) changes in the same change set. The
  `repo-docs` skill owns the front-page documents (README, and when added
  CONTRIBUTING, CODE_OF_CONDUCT, SECURITY), their translations, the header
  images in `.github/assets/`, and the settings record `.github/settings.yml`.
  README files may use emoji and non-English text.
- `.github/settings.yml` records the GitHub "About" panel (description,
  website, topics). GitHub does not read it: change the file first, then
  apply it on GitHub by hand; a change made on GitHub is copied back into the
  file.

## Fork rules

This repository is a fork, so these rules protect the upstream license and
attribution. They override any skill step that conflicts with them.

- `LICENSE` is the upstream BSD-2-Clause text with the University of
  Michigan copyright notice. Keep it byte-identical: never replace it, never
  add or remove a holder, and never let `repo-docs` treat it as residue. Its
  first condition requires keeping the notice in every redistribution.
- The fork's own additions (agent files, skills, docs, `scripts/`, and the
  `svg/` archives generated from the upstream images) are offered under the
  same BSD-2-Clause terms. Do not add another license file or notice without
  an explicit opt-in from the maintainer.
- Leave the upstream content as it is: the `tag<Family>/` directories and
  `tag_to_svg.py`. Changes to them belong upstream, which is in maintenance
  mode and accepts no new functionality.
- Never present the fork as the official project, and never imply that the
  University of Michigan, the APRIL Robotics Laboratory, or the upstream
  maintainers endorse it. Use no upstream logo or branding; link the upstream
  repository by name.
- Sync from upstream through the `upstream` remote: `git fetch upstream`
  (`git-fetch` and `git-pull` work only with `origin`), then invoke
  `git-merge` with source `upstream/master`.

## Layout

Canonical content lives only in the two open-convention locations:

- `AGENTS.md` (this file): instructions.
- `.agents/skills/<name>/SKILL.md`: skills, one directory each.

A tool that does not read these locations gets a thin adapter, never a copy.
Add adapters only for such tools: a tool that reads both a canonical location
and an adapter may list the same content twice.

- Instruction adapter: a file in the tool's own format and location whose
  only content imports or points to `AGENTS.md` (for example, a single
  `@AGENTS.md` import line where the tool supports imports).
- Skills adapter: a relative symbolic link from the tool's skills directory to
  `.agents/skills` (for example, `.<tool>/skills -> ../.agents/skills`).

This repository ships two adapters, both for Claude Code:

- `CLAUDE.md` holds only the `@AGENTS.md` import. When a `CLAUDE.md` exists,
  Claude Code loads it instead of reading `AGENTS.md` directly, so this import
  is how `AGENTS.md` reaches Claude Code; it never loads the file twice.
- `.claude/skills` is an accepted exception to the adapter rule above: Claude
  Code discovers skills only in `.claude/skills`, but several other tools read
  both `.agents/skills` and `.claude/skills`, so they may list each skill
  twice. Some of those tools offer a setting to ignore the Claude location.
  Some tools read `.claude/skills` but not `.agents/skills` (Cline, for
  example), so for them this link is the only way to the skills: when it is
  broken (see the Windows notes below), those tools find no skills.

Some tools need an adapter the template does not ship. For example, Gemini
CLI reads `GEMINI.md` by default (an instruction adapter, or its setting for
the context file name), and Kiro reads skills only from `.kiro/skills` (a
skills adapter). Add a skills adapter with a relative link where symbolic
links work:

```sh
MSYS=winsymlinks:nativestrict ln -s ../.agents/skills .<tool>/skills &&
  [ -L .<tool>/skills ]
```

The `MSYS` setting is ignored outside Git Bash. Without it, Git Bash lacking
symlink permission silently copies the directory instead of linking it; with
it, `ln` fails with `Operation not permitted`, a nonzero exit status, and no
copy left behind.

Where links do not work (Windows without symlink permission), write the
target as a plain file and register it in the index as a link, so every
symlink-aware checkout gets a real link:

```sh
printf %s ../.agents/skills > .<tool>/skills
git update-index --add --cacheinfo "120000,$(printf %s ../.agents/skills | git hash-object -w --stdin),.<tool>/skills"
```

Adding support for a tool means adding its adapters, plus its directory and
root instruction file to the AI tool `export-ignore` list in `.gitattributes`
when not already listed (commented out while the other lines there are);
nothing canonical moves or is duplicated. Adapter links are recognized by
target, not by path: a symbolic link whose target ends in `.agents/skills`.
Where a link has to be written as a plain file, its content is the target
alone, with no trailing newline.

On Windows, links need Developer Mode or administrator rights, plus
`core.symlinks`. Before a fresh clone, run `git config --global core.symlinks
true` (or clone with `git clone -c core.symlinks=true <url>`); to repair an
existing checkout, run `git config core.symlinks true` in it, then `rm <link>
&& git checkout -- <link>` for each broken link. Otherwise git writes each
link as a plain text file and the tool reading it sees nothing.

## Skill authoring

Skills must run under any agent tool, so they follow these rules:

- Frontmatter requires `name` and `description`. The only optional field
  allowed is `compatibility` (Agent Skills specification, at most 500
  characters), for environment needs such as network access or an installed
  program. Frontmatter must be valid YAML: quote a value, or use a block
  scalar such as `>-`, when it contains `: `.
- Skills need git 2.22 or later (they use `git branch --show-current`) and a
  POSIX shell.
- A skill may use another skill's file only through a path relative to its
  own directory (`../<skill>/...`) and must name that dependency in its body;
  the template ships the skills as one set.
- Every SKILL.md begins its Procedure with this line: "Terms such as choice
  question, independent reads, invoke, and suggest follow AGENTS.md (Skill
  authoring); in a non-interactive session every gate ends this skill."
- Name capabilities, never a specific tool's feature or tool names. Each tool
  maps these terms to its own features:
  - **gate**: a step whose action waits on the user: a choice question used
    as a gate, a confirmation, or an explicit in-turn opt-in.
  - **choice question**: 2 to 4 options, mutually exclusive unless the
    question is multi-select, each with its tradeoff; the user may always
    answer in their own words. Use the tool's structured question interface
    when it has one, otherwise numbered options in plain text, then wait. A
    choice question used as a gate blocks the gated action until the user
    answers.
  - **explicit in-turn opt-in**: a reply in the current turn that names the
    protected action and its target, either typed or by choosing an option
    whose label states that action and target (for example `yes, merge
    directly into main`). A generic yes, or approval from an earlier turn, is
    not an opt-in.
  - **non-interactive session**: when the session cannot put a question to
    the user and receive the answer (batch, CI, or cloud runs), every gate
    ends the skill: stop, report the pending question and the current state,
    and take no gated action. Never pick an option on the user's behalf; an
    explicit in-turn opt-in can only come from the user.
  - **POSIX shell**: run commands in a POSIX shell (Git Bash on Windows);
    snippets use POSIX redirections and heredocs. When the agent's default
    shell is not POSIX (for example PowerShell on Windows), run each snippet
    through bash. From Windows PowerShell 5.1, pass the snippet verbatim in a
    single-quoted here-string on stdin:

    ```powershell
    try { $bash = (Resolve-Path -ErrorAction Stop (Join-Path (git --exec-path) '../../../bin/bash.exe')).Path } catch { throw "Git Bash not found: $_" }
    $OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
    @'
    <snippet, unchanged>
    '@ | & $bash -c "tr -d '\r' | bash /dev/fd/3 3<&0 </dev/null"
    ```

    The first line finds Git Bash next to git (a bare `bash` may be WSL's)
    and throws, ending the command, when git or Git Bash is missing, so a
    stale `$LASTEXITCODE` is never read as the snippet's status; report that
    and stop. The single-quoted here-string keeps quotes, `$`, and quoted
    heredocs literal; stdin avoids the 5.1 bug that drops double quotes from
    native arguments such as `bash -c '<snippet>'`. The encoding line stops
    5.1 from prepending a byte order mark and makes non-ASCII output decode
    as UTF-8; these settings persist for the rest of that PowerShell session.
    `tr` drops the carriage returns PowerShell adds. The inner bash reads the
    script from descriptor 3 and gives its commands an empty stdin, so a
    command that reads stdin cannot swallow the rest of the snippet (with
    `bash -s`, later lines would silently never run and the status would
    still be 0). The closing `'@` must start its line, so a snippet cannot
    contain a line that starts with `'@`. `$LASTEXITCODE` holds the snippet's
    exit status.
  - **independent reads**: commands that do not depend on each other; run
    them concurrently when the agent can, otherwise one after another in any
    order.
  - **in-place edit** / **write the file**: change part of a file while
    preserving the rest, versus create or replace a whole file.
  - **the agent**: whichever tool is executing the skill.
  - **skill directory** (`<skill-dir>`): the absolute path of the directory
    holding the running skill's SKILL.md. Paths such as `references/x.md` or
    `scripts/x.sh` in a skill resolve against it, and `../<skill>/...`
    reaches a sibling skill. When the tool does not show it, use
    `<repository toplevel>/.agents/skills/<name>`. Quote it in commands,
    since it may contain spaces.
  - **invoke `<skill>`**: the agent runs that skill now, under that skill's
    own gates, however the tool triggers skills.
  - **suggest `<skill>`**: name that skill to the user as a next step without
    running it.
