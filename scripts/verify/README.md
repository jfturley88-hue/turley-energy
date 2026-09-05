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
