# LogLens
A Python CLI for summarizing application logs. Counts severity levels, groups recurring error messages and optionally exports a JSON report. Streams log lines instead of loading the entire file into memory (unique error messages are retained for counting).

## Quick start
Python 3.10+; no third-party packages.
```sh
python loglens.py sample.log --top 5 --json report.json
python -m unittest -v
```
The sample contains 7 non-empty lines, 3 ERROR entries and a repeated database timeout. Use only logs you are authorised to inspect; reports can include sensitive log text.

## Limitations
The parser identifies the first known severity token in a line. It is designed for simple text logs, not arbitrary structured formats, multiline stack traces or security incident detection.
