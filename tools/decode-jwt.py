#!/usr/bin/env python3
"""Разобрать JWT и показать, что в нём объявлено (подпись НЕ проверяется).

    python3 tools/decode-jwt.py <токен>
    cat token.txt | python3 tools/decode-jwt.py -

Нужен, чтобы увидеть поля OIDC-токена GitHub: по ним настраивается доверие
на стороне облака. Подпись здесь сознательно не проверяется — это задача
принимающей стороны, а нам важно содержимое.

Внимание: сам токен — короткоживущий, но всё же ключ. Не печатайте его
целиком в журнал прогона; печатайте разобранные поля, как делает этот скрипт.
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import sys

# Поля, по которым обычно настраивают доверие; остальные печатаются следом.
INTERESTING = [
    "iss", "aud", "sub", "repository", "repository_owner", "repository_visibility",
    "environment", "ref", "ref_type", "event_name", "workflow", "workflow_ref",
    "job_workflow_ref", "runner_environment", "actor", "actor_id",
]


def decode_part(part: str) -> dict:
    part += "=" * (-len(part) % 4)
    return json.loads(base64.urlsafe_b64decode(part))


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    token = sys.stdin.read().strip() if sys.argv[1] == "-" else sys.argv[1].strip()
    parts = token.split(".")
    if len(parts) != 3:
        print("это не похоже на JWT: частей %d вместо трёх" % len(parts))
        return 3

    header, payload = decode_part(parts[0]), decode_part(parts[1])
    print("заголовок: %s" % json.dumps(header, ensure_ascii=False))
    print("полей в токене: %d" % len(payload))
    print()
    print("поля, по которым настраивают доверие:")
    for key in INTERESTING:
        if key in payload:
            print("  %-22s %s" % (key, payload[key]))

    rest = sorted(set(payload) - set(INTERESTING) - {"iat", "exp", "nbf", "jti"})
    if rest:
        print()
        print("остальные поля: %s" % ", ".join(rest))

    if "iat" in payload and "exp" in payload:
        life = payload["exp"] - payload["iat"]
        fmt = lambda ts: dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%H:%M:%S")
        print()
        print("выдан %s UTC, истекает %s UTC — срок жизни %d с (%d мин)"
              % (fmt(payload["iat"]), fmt(payload["exp"]), life, life // 60))
    return 0


if __name__ == "__main__":
    sys.exit(main())
