#!/usr/bin/env -S uv run --script

# docs.zizmor.sh.py
# generate redirect pages from woodruffw.github.io to docs.zizmor.sh.

import string
import sys
from pathlib import Path

_TEMPLATE = string.Template(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="7; url=${real_dest}">
    <title>Redirecting to docs.zizmor.sh</title>
    <link rel="canonical" href="${real_dest}">
</head>
<body>
    <h1>Redirecting to docs.zizmor.sh 🌈</h1>

    <p>
        You're seeing this because you have an old link to zizmor's docs.
        Update your bookmarks to the redirected URL!
    </p>
    <p>
        If you are not redirected automatically, follow the
        <a id="dest" href="${real_dest}">link</a>.
    </p>

    <script>
        let fragment = window.location.hash;
        let redirectUrl = `${real_dest}$${fragment}`;
        setTimeout(function() {
            window.location=redirectUrl
        }, 5000);
        document.getElementById("dest").setAttribute("href", redirectUrl);
    </script>
</html>
""".strip()
)


_PAGES = [
    "",  # web root (can't use / because of path joining)
    "installation/",
    "quickstart/",
    "usage/",
    "release-notes/",
    "configuration/",
    "audits/",
    "development/",
    "trophy-case/",
]

_OUT = Path(__file__).parent.parent / "docs" / "zizmor"
assert _OUT.is_dir(), f"Output directory {_OUT} does not exist"

for page in _PAGES:
    dir_ = _OUT / page
    dir_.mkdir(exist_ok=True)

    index = dir_ / "index.html"
    with index.open("w") as io:
        real_dest = f"https://docs.zizmor.sh/{page}"
        io.write(_TEMPLATE.substitute(real_dest=real_dest))

    print(f"[+] wrote {index}", file=sys.stderr)
