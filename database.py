import sqlite3
import json
import hashlib
from datetime import datetime
import bcrypt

DB_NAME = "email_analysis.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------- MAIN ANALYSIS TABLE ----------------

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_hash TEXT UNIQUE,
            sender_domain TEXT,
            decision TEXT,
            risk_score REAL,
            nlp_cues TEXT,
            behavioral_flags TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- USER AUTH ----------------

def init_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash BLOB
        )
    """)

    conn.commit()
    conn.close()


def create_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE email = ?",
        (email,)
    )
    row = cursor.fetchone()
    conn.close()

    return row and bcrypt.checkpw(password.encode(), row[0])


# ---------------- USER EXCEPTIONS ----------------

def init_exception_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_exceptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            sender TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_exception(user_email, sender):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_exceptions (user_email, sender, created_at)
        VALUES (?, ?, datetime('now'))
    """, (user_email, sender))

    conn.commit()
    conn.close()


def is_exception(user_email, sender):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM user_exceptions
        WHERE user_email = ? AND sender = ?
    """, (user_email, sender))

    result = cursor.fetchone()
    conn.close()

    return result is not None


# ---------------- ANALYSIS STORAGE ----------------

def hash_email(headers, body):
    combined = (
        headers.get("from", "") +
        headers.get("to", "") +
        headers.get("subject", "") +
        body
    )
    return hashlib.sha256(combined.encode()).hexdigest()


def extract_sender_domain(headers):
    from_header = headers.get("from", "")
    if "@" in from_header:
        return from_header.split("@")[-1].replace(">", "").strip()
    return "unknown"


def save_analysis(headers, body, result):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO email_analysis (
                email_hash,
                sender_domain,
                decision,
                risk_score,
                nlp_cues,
                behavioral_flags,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            hash_email(headers, body),
            extract_sender_domain(headers),
            result["decision_engine"]["decision"],
            result["decision_engine"]["final_risk_score"],
            json.dumps(result["nlp_analysis"]["detected_cues"]),
            json.dumps(result["behavioral_analysis"]["behavioral_flags"]),
            datetime.utcnow().isoformat()
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
