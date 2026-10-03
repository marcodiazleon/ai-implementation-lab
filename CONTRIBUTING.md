# Contributing

Keep contributions scoped to the public synthetic sample. Read AGENTS.md and the specification before changing behavior.

Run:
```sh
python scripts/verify.py
```

For the optional local commit guard:
```sh
git config --local core.hooksPath .githooks
```

The hook uses `python`; set the PYTHON environment variable to a Python executable if needed. It inspects staged bytes and exits nonzero on its limited findings. To disable only this repo's hook selection: `git config --local --unset core.hooksPath`.

Do not include credentials, personal paths, client information or private source. Do not add paid/external services as default behavior. Update tests, acceptance mapping and capability limits together.
