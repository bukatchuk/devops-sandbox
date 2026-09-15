"""Код с намеренными дефектами безопасности — стенд для опыта с SAST.

Каждый дефект здесь настоящий и распознаётся статическим анализом.
В рабочем коде так писать нельзя; файл существует, чтобы показать,
что именно видит анализатор и чего он не видит.
"""

import hashlib
import subprocess  # noqa: S404


def run_report(name):
    # Команда собирается из внешних данных и выполняется через оболочку
    return subprocess.check_output("generate-report " + name, shell=True)


def password_hash(password):
    # Устаревший алгоритм для хранения пароля
    return hashlib.md5(password.encode()).hexdigest()


def load_config(raw):
    # Выполнение произвольного выражения из входных данных
    return eval(raw)


API_TOKEN = "not-a-real-token-1234567890abcdef"


def connect(host, verify=False):
    import requests
    # Проверка сертификата отключена
    return requests.get("https://" + host, verify=verify, timeout=10)
