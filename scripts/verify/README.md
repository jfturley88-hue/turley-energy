# Verifying the planner

These drive the real app in Chromium and report every page error. They live in the repo
because the previous set lived in a session scratchpad and was lost with the container.

```sh
npm i playwright                # once; Chromium at $CHROME or /opt/pw-browsers/chromium-*/chrome-linux/chrome
node scripts/verify/drive_all.js     # every mode, every export, every Rate Settings tab, save
node scripts/verify/drive2.js        # invariants: restore keeps actuals and figures; a tick
                                     #   moves the item into the priced section; a rate override
                                     #   reaches the plan and Reset All undoes it; schedule scope
                                     #   equals plan scope; no undefined/NaN in any print view;
                                     #   extensions; switching modes leaves nothing behind
node scripts/verify/determinism.js   # the same example prices the same across cold launches,
                                     #   a slow click, a double generate, and after another mode
node scripts/verify/tick.js          # the not-included tick, in detail
python3 scripts/verify/static_scan.py   # syntax on every script block; calls to undefined names
```

`drive_all` reports one error on reload in a sandbox that blocks Google Fonts; that is the
proxy, not the app. `static_scan` flags names it cannot see defined -- destructured helpers
(`merge: m1`) show up as false positives; anything else is real.

## On Windows

There is no container here, so nothing is preinstalled and the paths above do not exist.
Node and Python install per-user with no admin rights: unzip the official Node build, and
run the python.org installer with `/quiet InstallAllUsers=0 PrependPath=0 TargetDir=...`.

Do not `npm i` into the repo when it sits on a Google Drive letter — Drive's filesystem
truncates files mid-write and npm leaves a `package.json` that Node rejects with
`ERR_INVALID_PACKAGE_CONFIG`. Install into a directory on the real disk and point
`NODE_PATH` at its `node_modules`.

Playwright's own Chromium download fails behind some connections. It is not needed:
these scripts already take `$CHROME`, so aim it at an installed Chrome.

```sh
export NODE_PATH=".../planitber-deps/node_modules"
export CHROME="C:/Program Files/Google/Chrome/Application/chrome.exe"
export NODE="C:/Users/<you>/.local/node/node.exe"   # static_scan spawns this
node scripts/verify/drive2.js
PYTHONUTF8=1 python scripts/verify/static_scan.py
```

`static_scan` reads the app as UTF-8 explicitly; without `PYTHONUTF8=1` the rest of the
Python toolchain still defaults to cp1252 on this platform.
