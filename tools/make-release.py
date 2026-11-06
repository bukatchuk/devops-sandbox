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

import http.client
import json
import os
import sys


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

    # Хост фиксирован: схема и адрес не зависят от входных данных.
    conn = http.client.HTTPSConnection("api.github.com", timeout=30)
    try:
        conn.request(
            "POST",
            "/repos/%s/releases" % repo,
            body=payload,
            headers={
                "Authorization": "Bearer " + token,
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "devops-course-release",
            },
        )
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8", "replace")
        code = resp.status
    finally:
        conn.close()
    if code >= 400:
        print("GitHub ответил %s: %s" % (code, raw[:200]))
        return 1
    data = json.loads(raw)

    print("код ответа:      %s" % code)
    print("релиз:           %s" % data.get("html_url"))
    print("тег:             %s" % data.get("tag_name"))
    print("черновик:        %s" % data.get("draft"))
    print("создан из:       %s" % (data.get("target_commitish") or "?")[:7])
    print("длина changelog: %d символов" % len(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
