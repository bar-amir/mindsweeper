#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python3 -m virtualenv .env --prompt "[mindsweeper] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt
    ./scripts/compile-protos.sh
    npm install --prefix ./mindsweeper/gui
}

main "$@"