#!/usr/bin/env python3
"""Создать релиз GitHub по данным из окружения.

Запускается из воркфлоу. Всё берётся из переменных окружения, а не
из аргументов командной строки: аргументы видны в /proc любому процессу
на машине (измерено в уроке 06.03), а окружение — нет.

  GH_TOKEN     токен с правом contents: write
  REPO         владелец/репозиторий
  VERSION      тег релиза
  TARGET       коммит, на который указывает тег
  DRAFT        true/false
  NOTES_FILE   файл с текстом changelog
"""

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    token = os.environ["GH_TOKEN"]
    repo = os.environ["REPO"]
    version = os.environ["VERSION"]
    notes = open(os.environ.get("NOTES_FILE", "notes.md"), encoding="utf-8").read()

    payload = json.dumps({
        "tag_name": version,
        "name": version,
        "body": notes,
        "draft": os.environ.get("DRAFT", "true") == "true",
        "target_commitish": os.environ.get("TARGET", "main"),
    }).encode()

    req = urllib.request.Request(
        "https://api.github.com/repos/%s/releases" % repo,
        data=payload,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "devops-course-release",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            code = resp.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        print("GitHub ответил %s: %s" % (exc.code, body[:200]))
        return 1

    print("код ответа:      %s" % code)
    print("релиз:           %s" % data.get("html_url"))
    print("тег:             %s" % data.get("tag_name"))
    print("черновик:        %s" % data.get("draft"))
    print("создан из:       %s" % (data.get("target_commitish") or "?")[:7])
    print("длина changelog: %d символов" % len(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
