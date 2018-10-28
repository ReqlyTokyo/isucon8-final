from __future__ import annotations

import isubank
import isulogger


BANK_ENDPOINT = "bank_endpoint"
BANK_APPID = "bank_appid"
LOG_ENDPOINT = "log_endpoint"
LOG_APPID = "log_appid"

global_logger = None

def set_setting(db, k: str, v: str):
    cur = db.cursor()
    cur.execute(
        "INSERT INTO setting (name, val) VALUES (%s, %s) ON DUPLICATE KEY UPDATE val = VALUES(val)",
        (k, v),
    )

def get_setting(db, k: str) -> str:
    cur = db.cursor()
    cur.execute("SELECT val FROM setting WHERE name = %s LIMIT 1", (k,))
    return cur.fetchone()[0]


def get_isubank(db):
    endpoint = get_setting(db, BANK_ENDPOINT)
    appid = get_setting(db, BANK_APPID)
    return isubank.IsuBank(endpoint, appid)

def set_isulogger(db):
    global global_logger
    endpoint = get_setting(db, LOG_ENDPOINT)
    appid = get_setting(db, LOG_APPID)
    global_logger = isulogger.IsuLogger(endpoint, appid)

def get_logger(db):
    global global_logger
    if global_logger is None:
        set_isulogger(db)
    return global_logger

def send_log(db, tag, v):
    logger = get_logger(db)
    logger.send(tag, v)
