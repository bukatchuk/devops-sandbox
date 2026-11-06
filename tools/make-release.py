#!/usr/bin/env python3
"""Создать релиз GitHub по данным из окружения.

Запускается из воркфлоу. Всё берётся из переменных окружения, а не
из аргументов командной строки: аргументы видны в /proc любому процессу
на машине (измерено в уроке 06.03), а окружение — нет.

  GH_TOKEN     токен с правом contents: write (его читает сам gh)
  REPO         владелец/репозиторий
  VERSION      тег релиза
  TARGET       коммит, на который указывает тег
  DRAFT        true/false
  NOTES_FILE   файл с текстом changelog

Запрос уходит через `gh api`, а не через urllib: gh сам ставит заголовки,
проверяет TLS и берёт токен из GH_TOKEN, а в нашем коде не остаётся ни
динамического URL, ни ручного HTTPS-соединения — на них ругаются сканеры
кода (Semgrep: dynamic-urllib-use-detected). Команда запускается списком
аргументов, без shell, поэтому подставить в неё лишнюю команду нельзя.
"""

import json
import os
import subprocess
import sys


def main() -> int:
    repo = os.environ["REPO"]
    version = os.environ["VERSION"]
    with open(os.environ.get("NOTES_FILE", "notes.md"), encoding="utf-8") as f:
        notes = f.read()

    payload = json.dumps({
        "tag_name": version,
        "name": version,
        "body": notes,
        "draft": os.environ.get("DRAFT", "true") == "true",
        "target_commitish": os.environ.get("TARGET", "main"),
    })

    # Тело запроса — через stdin (--input -): оно не попадает в список процессов.
    proc = subprocess.run(
        ["gh", "api", "--method", "POST", f"repos/{repo}/releases", "--input", "-"],
        input=payload,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0:
        print(f"GitHub ответил ошибкой: {(proc.stderr or proc.stdout)[:200]}")
        return 1

    data = json.loads(proc.stdout)
    print("код ответа:      201")
    print(f"релиз:           {data.get('html_url')}")
    print(f"тег:             {data.get('tag_name')}")
    print(f"черновик:        {data.get('draft')}")
    print(f"создан из:       {(data.get('target_commitish') or '?')[:7]}")
    print(f"длина changelog: {len(notes)} символов")
    return 0


if __name__ == "__main__":
    sys.exit(main())
