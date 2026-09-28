"""FastAPI backend for the OIL-SIF React application."""
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
import base64
import threading
import smtplib
import re
import os
import urllib.request
from pathlib import Path
from email.message import EmailMessage
from urllib.request import Request, urlopen
from datetime import datetime, timezone, timedelta
from io import StringIO
from pathlib import Path


from dotenv import load_dotenv
import joblib
import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

APP_ROOT = Path(__file__).parent
APP_CORE = APP_ROOT / 'app_core'
load_dotenv(APP_CORE / '.env')
sys.path.insert(0, str(APP_CORE))


# ---------------------------------------------------------------------------
# Deployment datasets
# ---------------------------------------------------------------------------
# The large datasets are kept out of GitHub's normal repository history and
# stored as GitHub Release assets. Render downloads them automatically when
# they are missing from app_core.
DATASET_URLS = {
    'January2015toNovember2025.csv':
        'https://github.com/aditya-sultania/OIL-SIF-SIH/releases/download/datasets-v1/January2015toNovember2025.csv',
    'SIF_Dashboard_Master_v4.csv':
        'https://github.com/aditya-sultania/OIL-SIF-SIH/releases/download/datasets-v1/SIF_Dashboard_Master_v4.csv',
}


def ensure_datasets():
    APP_CORE.mkdir(parents=True, exist_ok=True)

    for filename, url in DATASET_URLS.items():
        destination = APP_CORE / filename

        if destination.exists() and destination.stat().st_size > 0:
            print(f'[OIL-SIF] Dataset already present: {filename}')
            continue

        temp_destination = destination.with_suffix(destination.suffix + '.download')

        print(f'[OIL-SIF] Downloading dataset: {filename}')
        try:
            if temp_destination.exists():
                temp_destination.unlink()

            request = Request(
                url,
                headers={'User-Agent': 'OIL-SIF-Render/1.0'},
            )

            with urlopen(request, timeout=120) as response, open(temp_destination, 'wb') as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)

            if not temp_destination.exists() or temp_destination.stat().st_size == 0:
                raise RuntimeError('Downloaded file is empty.')

            temp_destination.replace(destination)
            print(f'[OIL-SIF] Dataset downloaded: {filename}')

        except Exception as exc:
            if temp_destination.exists():
                temp_destination.unlink()
            print(f'[OIL-SIF] Dataset download failed for {filename}: {exc}')
            raise


ensure_datasets()


app = FastAPI(title='OIL-SIF API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',') if x.strip()],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ---------------------------------------------------------------------------
# Models / datasets: loaded exactly once at process startup.
# ---------------------------------------------------------------------------
_sif_model = None
_lsr_model = None

def load_model(path):
    try:
        return joblib.load(path) if path.exists() else None
    except Exception as exc:
        print(f'[OIL-SIF] Could not load model {path.name}: {exc}')
        return None

_sif_model = load_model(APP_CORE / 'SIF_Model_v4_DomainAware.joblib')
_lsr_model = load_model(APP_CORE / 'IOGP_Life_Saving_Rule_Classifier_v2.joblib')

def read_csv(name):
    path = APP_CORE / name
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as exc:
        print(f'[OIL-SIF] Could not load {name}: {exc}')
        return pd.DataFrame()

barrier_df = read_csv('SIF_Barrier_Ranking_v4.csv')
activity_df = read_csv('SIF_Activity_Ranking_v4.csv')
# The 209 MB historical master dataset is loaded lazily so authentication and the
# application shell become available immediately.
master_df = pd.DataFrame()
_MASTER_LOCK = threading.RLock()
def get_master_df():
    global master_df
    if master_df.empty:
        with _MASTER_LOCK:
            if master_df.empty:
                master_df = read_csv('SIF_Dashboard_Master_v4.csv')
    return master_df
queue_df = read_csv('SIF_HSE_Review_Queue_v2.csv')
lsr_df = read_csv('SIF_LSR_Ranking_v4.csv')
precursor_df = read_csv('SIF_Precursor_Ranking_v4.csv')

# Precompute compact dashboard data once. The frontend receives this instead
# of repeatedly serializing the 366k-row master CSV.
def build_overview(df):
    if df.empty:
        return {
            'kpis': {'total_reports': 0, 'sif_potential': 0, 'high_probability': 0, 'awaiting_review': len(queue_df)},
            'sif_distribution': [], 'sif_trend': [], 'precursors': [], 'industries': [], 'recent_high_risk': []
        }

    work = df.copy()
    work['parsed_date'] = pd.to_datetime(work.get('date_of_incident'), format='%d%b%Y', errors='coerce')
    prediction = work['sif_prediction'].astype(str).str.strip().str.lower()
    band = work['confidence_band'].astype(str).str.strip()

    distribution = [
        {'band': 'Low SIF probability', 'count': int((band == 'Low SIF probability').sum())},
        {'band': 'Review zone', 'count': int((band == 'Review zone').sum())},
        {'band': 'High SIF probability', 'count': int((band == 'High SIF probability').sum())},
    ]

    tmp = work.dropna(subset=['parsed_date']).copy()
    if not tmp.empty:
        tmp['week'] = tmp['parsed_date'].dt.to_period('W').apply(lambda x: x.start_time)
        weekly = tmp.groupby(['week', 'confidence_band']).size().reset_index(name='count')
        trend = []
        for week in sorted(weekly['week'].unique()):
            wd = weekly[weekly['week'] == week]
            trend.append({
                'date': week.strftime('%d %b %Y'),
                'low': int(wd.loc[wd['confidence_band'] == 'Low SIF probability', 'count'].sum()),
                'review': int(wd.loc[wd['confidence_band'] == 'Review zone', 'count'].sum()),
                'high': int(wd.loc[wd['confidence_band'] == 'High SIF probability', 'count'].sum()),
            })
    else:
        trend = []

    precursors = []
    for _, row in precursor_df.head(6).iterrows():
        precursors.append({
            'rank': int(row.get('rank', len(precursors) + 1)),
            'precursor': row.get('precursor', 'Unknown'),
            'total_reports': int(row.get('total_reports', 0)),
            'sif_reports': int(row.get('sif_reports', 0)),
            'sif_density_pct': float(row.get('sif_density_pct', 0)),
        })

    industries = []
    if 'industry_description' in work:
        for _, row in work.groupby('industry_description').size().reset_index(name='total_reports').sort_values('total_reports', ascending=False).head(6).iterrows():
            industries.append({'industry': row['industry_description'], 'total_reports': int(row['total_reports'])})

    recent = work[prediction.eq('sif potential')].sort_values('parsed_date', ascending=False).head(8)
    recent_rows = []
    for _, row in recent.iterrows():
        recent_rows.append({
            'report_id': row.get('report_id'),
            'date': row['parsed_date'].strftime('%d %b %Y') if pd.notna(row['parsed_date']) else None,
            'activity': row.get('activity_group'),
            'sif_probability': float(row['sif_probability']) if pd.notna(row.get('sif_probability')) else None,
            'life_saving_rule': row.get('life_saving_rule'),
            'review_status': row.get('hse_review_status'),
        })

    return {
        'kpis': {
            'total_reports': int(len(work)),
            'sif_potential': int(prediction.eq('sif potential').sum()),
            'high_probability': int((band.str.lower() == 'high sif probability').sum()),
            'awaiting_review': int(len(queue_df)),
        },
        'sif_distribution': distribution,
        'sif_trend': trend[-24:],
        'precursors': precursors,
        'industries': industries,
        'recent_high_risk': recent_rows,
    }

_overview_cache_path = APP_CORE / 'overview_cache.json'
OVERVIEW_CACHE = None
if _overview_cache_path.exists():
    try:
        OVERVIEW_CACHE = json.loads(_overview_cache_path.read_text(encoding='utf-8'))
    except Exception:
        OVERVIEW_CACHE = None
if not OVERVIEW_CACHE:
    # Fallback for older project copies that do not contain the compact cache.
    OVERVIEW_CACHE = build_overview(get_master_df())

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
USERS_FILE = APP_CORE / 'users_db.json'
DATA_DIR = APP_CORE / 'runtime_data'
UPLOAD_DIR = DATA_DIR / 'uploads'
REPORTS_FILE = DATA_DIR / 'submitted_reports.json'
REVIEWS_FILE = DATA_DIR / 'hse_reviews.json'
NOTIFICATIONS_FILE = DATA_DIR / 'notifications.json'
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
STORE_LOCK = threading.RLock()

def read_json_file(path, default):
    try:
        if path.exists():
            value = json.loads(path.read_text(encoding='utf-8'))
            return value
    except Exception as exc:
        print(f'[OIL-SIF] Could not read {path.name}: {exc}')
    return default

def write_json_file(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    tmp.replace(path)

submitted_reports = read_json_file(REPORTS_FILE, [])
hse_reviews = read_json_file(REVIEWS_FILE, {})
notifications_store = read_json_file(NOTIFICATIONS_FILE, {})

def save_runtime_state():
    with STORE_LOCK:
        write_json_file(REPORTS_FILE, submitted_reports[-5000:])
        write_json_file(REVIEWS_FILE, hse_reviews)
        write_json_file(NOTIFICATIONS_FILE, notifications_store)

DEFAULT_USERS = {
    'employee': {'password': 'employee123', 'role': 'Employee', 'name': 'Rajesh Kumar (Field Operator)'},
    'hse': {'password': 'hse123', 'role': 'HSE Officer', 'name': 'Sarah Jenkins (Lead Safety Inspector)'},
    'management': {'password': 'management123', 'role': 'Management', 'name': 'Dr. Aris Thorne (Operations Director)'},
}

def load_users():
    data = dict(DEFAULT_USERS)
    if USERS_FILE.exists():
        try:
            raw = json.loads(USERS_FILE.read_text(encoding='utf-8'))
            if isinstance(raw, dict):
                data.update(raw)
        except Exception:
            pass
    return data

users_db = load_users()
sessions = {}

# In-memory Gemini chat sessions, keyed by username, so the AI Copilot keeps
# conversation context (follow-up questions) across separate HTTP requests.
# This is intentionally simple (single-process, in-memory) for the prototype;
# it is cleared on logout and capped to avoid unbounded growth.
_chat_sessions = {}
_CHAT_SESSION_LIMIT = 200

# Store passwords securely for newly created users. Legacy plain passwords in
# users_db are still supported so the default accounts continue to work.
def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 120000)
    return f'pbkdf2$120000${salt}${digest.hex()}'

def verify_password(password, user):
    # New users use PBKDF2. Older users in the project used either a plain
    # password field or salt/password_hash from the original prototype.
    stored = user.get('password') if isinstance(user, dict) else user
    if isinstance(stored, str) and stored.startswith('pbkdf2$'):
        try:
            _, rounds, salt, digest = stored.split('$', 3)
            actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), int(rounds)).hex()
            return hmac.compare_digest(actual, digest)
        except Exception:
            return False
    if isinstance(user, dict) and user.get('password_hash') and user.get('salt'):
        digest = hashlib.sha256((user['salt'] + password).encode('utf-8')).hexdigest()
        if hmac.compare_digest(digest, str(user['password_hash'])):
            return True
        legacy = hashlib.sha256(f"{user['salt']}:{password}".encode('utf-8')).hexdigest()
        return hmac.compare_digest(legacy, str(user['password_hash']))
    return hmac.compare_digest(str(stored or ''), password)

def persist_users():
    USERS_FILE.write_text(json.dumps(users_db, indent=2, ensure_ascii=False), encoding='utf-8')

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    username: str
    password: str
    role: str

class ScanRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    question: str = ''
    reset: bool = False

class TranslateRequest(BaseModel):
    language: str
    texts: list[str]

class SubmitReportRequest(BaseModel):
    text: str
    site: str = 'Unknown'
    location: str = 'Unknown'
    report_type: str = 'Unsafe Act / Unsafe Condition'
    photo_data: str | None = None
    immediate_danger: bool = False

class ReviewRequest(BaseModel):
    decision: str
    reason: str = ''
    action: str = ''

TRANSLATION_CACHE = {}

@app.post('/api/i18n/translate')
def translate_interface(req: TranslateRequest):
    """Translate visible UI strings in reliable Gemini batches."""
    language = str(req.language).strip()
    texts = []
    seen = set()
    for text in req.texts[:240]:
        value = ' '.join(str(text).split()).strip()
        if value and value not in seen and len(value) <= 220:
            texts.append(value)
            seen.add(value)
    if not texts or language == 'English':
        return {'translations': {text: text for text in texts}}

    cache = TRANSLATION_CACHE.setdefault(language, {})
    missing = [text for text in texts if text not in cache]
    api_key = os.getenv('GEMINI_API_KEY', '').strip()
    if missing and api_key:
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=api_key)
            for offset in range(0, len(missing), 60):
                batch = missing[offset:offset + 60]
                prompt = f"""Translate every item below from English into {language}.
This is the complete visible user interface of an industrial safety application.
Return ONLY a JSON object. The JSON keys MUST be the exact original English strings
and every key MUST have a translated value. Do not omit items.
Preserve placeholders, punctuation, arrows, numbers, report IDs, and acronyms such as
OIL-SIF, SIF, HSE, AI, IOGP, LOTO, API, ID. Use clear, natural, professional UI language.
Items:
{json.dumps(batch, ensure_ascii=False)}"""
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type='application/json',
                        temperature=0.0,
                    ),
                )
                raw = getattr(response, 'text', '') or '{}'
                translated = json.loads(raw)
                if isinstance(translated, dict):
                    for source in batch:
                        value = translated.get(source)
                        if isinstance(value, str) and value.strip():
                            cache[source] = value.strip()
        except Exception as exc:
            print(f'[OIL-SIF] Interface translation error ({language}): {exc}')
    elif missing and not api_key:
        print('[OIL-SIF] GEMINI_API_KEY is not loaded; interface translation will use local/static text only.')

    return {'translations': {text: cache.get(text, text) for text in texts}}

ROLE_MAP = {
    'employee': 'Employee',
    'employee / worker': 'Employee',
    'field worker': 'Employee',
    'hse officer': 'HSE Officer',
    'management': 'Management',
}

def normalize_role(role):
    key = ' '.join(str(role).strip().lower().split())
    return ROLE_MAP.get(key, role if role in ('Employee', 'HSE Officer', 'Management') else 'Employee')

def current_user(authorization: str = Header(default='')):
    if not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Authentication required.')
    token = authorization[7:].strip()
    session = sessions.get(token)
    if not session:
        raise HTTPException(status_code=401, detail='Session expired. Please sign in again.')
    return session

def require_role(*allowed_roles):
    def dependency(user=Depends(current_user)):
        if user.get('role') not in allowed_roles:
            raise HTTPException(status_code=403, detail='This area is not available for your role.')
        return user
    return dependency

@app.post('/api/auth/login')
def login(req: LoginRequest):
    username = req.username.strip().lower()
    user = users_db.get(username)
    if not user or not verify_password(req.password, user):
        raise HTTPException(status_code=401, detail='Authentication rejected. Invalid credentials.')
    token = secrets.token_urlsafe(32)
    role = normalize_role(user.get('role'))
    payload = {'username': username, 'name': user.get('name', username), 'role': role}
    sessions[token] = payload
    return {'ok': True, 'token': token, 'user': payload}

@app.get('/api/auth/me')
def me(user=Depends(current_user)):
    return {'ok': True, 'user': user}

@app.post('/api/auth/logout')
def logout(authorization: str = Header(default='')):
    if authorization.startswith('Bearer '):
        token = authorization[7:].strip()
        session = sessions.pop(token, None)
        if session:
            _chat_sessions.pop(session.get('username'), None)
    return {'ok': True}

@app.post('/api/auth/register')
def register(req: RegisterRequest):
    name = req.name.strip()
    username = req.username.strip().lower()
    password = req.password
    role = normalize_role(req.role)
    if not name or not username or not password:
        raise HTTPException(status_code=400, detail='All fields are required.')
    if len(username) < 3:
        raise HTTPException(status_code=400, detail='Username must contain at least 3 characters.')
    if len(password) < 6:
        raise HTTPException(status_code=400, detail='Password must contain at least 6 characters.')
    if username in users_db:
        raise HTTPException(status_code=409, detail='Username already registered.')
    users_db[username] = {'password': hash_password(password), 'role': role, 'name': f'{name} ({role})'}
    persist_users()
    return {'ok': True, 'message': 'Account created successfully.'}

# ---------------------------------------------------------------------------
# Protected application endpoints
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Operational report workflow helpers
# ---------------------------------------------------------------------------
LSR_RULES = {
    'height': 'Working at Height', 'harness': 'Working at Height', 'scaffold': 'Working at Height',
    'crane': 'Lifting Operations', 'suspended load': 'Lifting Operations', 'lifting': 'Lifting Operations',
    'lockout': 'Energy Isolation', 'loto': 'Energy Isolation', 'zero energy': 'Energy Isolation',
    'valve': 'Energy Isolation', 'pressure': 'Energy Isolation', 'hot work': 'Hot Work',
    'welding': 'Hot Work', 'confined': 'Confined Space', 'tank': 'Confined Space',
    'line of fire': 'Line of Fire', 'struck': 'Line of Fire', 'forklift': 'Line of Fire',
    'vehicle': 'Line of Fire', 'excavation': 'Excavation', 'excavat': 'Excavation',
    'electrical': 'Electrical Safety', 'energized': 'Electrical Safety',
}

# ---------------------------------------------------------------------------
# Safety evidence / backstop rules
# ---------------------------------------------------------------------------
# The ML model is useful for broad triage, but short employee narratives are
# often too sparse for a text-only classifier.  These deterministic rules are
# deliberately conservative: they do NOT claim that every injury is an SIF.
# They identify the safety mechanism first, then place the report into one of
# three screening levels: critical, review, or model-only/low-risk.

SAFETY_EVIDENCE_RULES = [
    ('critical', 'Actual fall from height',
     r'\b(?:fell|fallen|falling|fall|dropped)\b.{0,100}\b(?:\d+(?:st|nd|rd|th)?\s*(?:floor|storey|story)|from\s+(?:a\s+)?height|from\s+(?:the\s+)?roof|from\s+(?:a\s+)?scaffold|from\s+(?:a\s+)?ladder|from\s+(?:an?\s+)?elevated|to\s+(?:a\s+)?lower\s+level)\b|\b(?:\d+(?:st|nd|rd|th)?\s*(?:floor|storey|story))\b.{0,50}\b(?:fell|fallen|fall)\b'),
    ('critical', 'Caught/crushed by machinery or moving equipment',
     r'\b(?:caught|trapped|pinned|crushed|smashed|entangled)\b.{0,100}\b(?:machine|machinery|equipment|conveyor|roller|press|splicer|drill|drilling|lathe|vehicle|forklift|crane|pipe|steel|metal)\b|\b(?:machine|machinery|conveyor|roller|press)\b.{0,100}\b(?:caught|trapped|pinned|crushed|smashed|amputat)\b'),
    ('critical', 'Amputation or loss of body part',
     r'\b(?:amputat(?:ed|ion)|lost\s+(?:a\s+)?(?:finger|thumb|hand|arm|leg|limb)|severed\s+(?:finger|thumb|hand|arm|leg|limb)|finger\s+cut\s+off|limb\s+cut\s+off)\b'),
    ('critical', 'Electrocution / severe electrical exposure',
     r'\b(?:electrocution|electrocuted|arc\s*flash|electrical\s+shock|electric\s+shock|high\s+voltage|energized\s+and\s+(?:shocked|contacted)|contacted\s+an?\s+energized)\b'),
    ('critical', 'Struck by vehicle, crane or suspended load',
     r'\b(?:struck|hit|run\s+over|backed\s+over|crushed)\b.{0,100}\b(?:forklift|vehicle|truck|crane|loader|excavator|suspended\s+load|moving\s+equipment)\b|\b(?:forklift|vehicle|truck|crane|suspended\s+load)\b.{0,100}\b(?:struck|hit|crushed|fell\s+on|landed\s+on)\b'),
    ('critical', 'Explosion / flash fire / major fire event',
     r'\b(?:explosion|exploded|flash\s+fire|fireball|major\s+fire|uncontrolled\s+fire|flammable\s+gas\s+ignited|gas\s+ignition)\b'),
    ('critical', 'Confined-space life-threatening exposure',
     r'\b(?:confined\s+space|confined\s+vessel|tank)\b.{0,120}\b(?:unconscious|collapsed|asphyxi|h2s|hydrogen\s+sulfide|oxygen\s+deficient|no\s+oxygen|engulfed|rescue)\b'),
    ('critical', 'Drowning / man overboard',
     r'\b(?:drowned|drowning|man\s+overboard|fell\s+overboard|submerged|underwater\s+and\s+(?:unconscious|unable))\b'),
    ('critical', 'High-pressure release / rupture',
     r'\b(?:high\s+pressure|pressurized|pressure\s+line|pressure\s+vessel)\b.{0,100}\b(?:ruptured|rupture|burst|exploded|released|recoil|release)\b'),
    ('high', 'Burning smell / smoke / overheating precursor',
     r'\b(?:smell(?:ed|s)?|odor|odour|noticed|detected)\b.{0,80}\b(?:burn(?:ing|t)?|smoke|scorch(?:ed|ing)?|overheat(?:ed|ing)?|hot\s+plastic|burnt\s+plastic|burnt\s+rubber)\b|\b(?:burning|burnt|scorch(?:ed|ing)?|smoke|overheat(?:ed|ing)?)\b.{0,80}\b(?:smell|odor|odour|odourous|scent)\b'),
    ('high', 'Sparks / arcing / visible electrical fault',
     r'\b(?:sparks?|sparking|arcing|arc\s*flash|flashing|short\s+circuit|electrical\s+fault|burnt\s+wire|exposed\s+wire|live\s+wire|energized\s+wire)\b'),
    ('high', 'Gas / fuel / chemical odor or release precursor',
     r'\b(?:smell(?:ed|s)?|odor|odour|noticed|detected)\b.{0,80}\b(?:gas|fuel|diesel|petrol|solvent|chemical|h2s|hydrogen\s+sulfide)\b|\b(?:gas|fuel|diesel|petrol|solvent|chemical|h2s|hydrogen\s+sulfide)\b.{0,80}\b(?:smell|odor|odour|leak|leaking|hissing)\b'),
    ('high', 'Overheating / fire-risk equipment condition',
     r'\b(?:motor|motor\s+housing|bearing|panel|switchboard|transformer|cable|socket|outlet|charger|battery|equipment|machine)\b.{0,100}\b(?:overheat(?:ed|ing)?|too\s+hot|burning|smoke|scorch(?:ed|ing)?|melting|melted)\b'),
    ('high', 'Severe injury / fracture / serious burn',
     r'\b(?:fractured|fracture|broken\s+(?:bone|arm|leg|hand|finger)|dislocated|second\s+degree\s+burn|third\s+degree\s+burn|severe\s+burn|serious\s+burn|hospitalized|hospitalised|loss\s+of\s+eye|eye\s+lost)\b'),
    ('high', 'High-risk exposure without required control',
     r'\b(?:without|no|not\s+wearing|missing|failed\s+to|bypassed|bypass(?:ed|ing)?|without\s+(?:a\s+)?permit)\b.{0,120}\b(?:harness|fall\s+protection|lock[- ]?out|tag[- ]?out|isolation|permit|confined\s+space|energized|suspended\s+load|crane|excavation|trench|guard|interlock|machine\s+guard)\b'),
    ('high', 'Suspended-load / line-of-fire exposure',
     r'\b(?:under|beneath|near|beside|inside)\b.{0,80}\b(?:suspended\s+load|hanging\s+load|crane\s+load)\b|\b(?:suspended\s+load|hanging\s+load|crane\s+load)\b.{0,80}\b(?:worker|person|employee)\b'),
    ('high', 'Gas leak / hazardous release',
     r'\b(?:gas\s+leak|h2s|hydrogen\s+sulfide|toxic\s+gas|chemical\s+release|loss\s+of\s+containment|leak(?:ed|ing)?)\b'),
    ('high', 'Immediate chemical / toxic exposure',
     r'\b(?:chemical|acid|caustic|toxic|h2s|hydrogen\s+sulfide|gas\s+leak|poisonous)\b.{0,100}\b(?:exposure|exposed|inhaled|breathed|splashed|burned|burn|unconscious)\b'),
    ('high', 'Powered-tool injury',
     r'\b(?:drill|drilled|drilling|grinder|grinding|saw|sawing|circular\s+saw|power\s+tool|machine|machinery|press|lathe|conveyor)\b.{0,100}\b(?:hand|finger|thumb|arm|wrist|leg|foot|eye|face)\b|\b(?:hand|finger|thumb|arm|wrist|leg|foot|eye|face)\b.{0,100}\b(?:drill|drilled|drilling|grinder|grinding|saw|power\s+tool|machine|machinery|press|lathe)\b'),
    ('review', 'Slip/trip/fall on same level',
     r'\b(?:slipped|tripped|fell|fallen)\b.{0,80}\b(?:same\s+level|floor|ground|stairs|stairway|walkway|pavement)\b'),
    ('review', 'Tool / machinery injury',
     r'\b(?:drilled|drill(?:ed|ing)?|punctured|pierced|cut|lacerat(?:ed|ion)|sliced|stabbed|pinched|hit)\b.{0,100}\b(?:hand|finger|thumb|arm|wrist|leg|foot|eye|face)\b|\b(?:hand|finger|thumb|arm|wrist|leg|foot|eye|face)\b.{0,100}\b(?:drill|drilled|machine|tool|saw|knife|blade|equipment)\b'),
    ('review', 'Other reported injury',
     r'\b(?:injured|injury|hurt|pain|bruise|bruised|sprain|strain|swollen|swelling|burned|burnt|burn|bleeding|wound)\b'),
    ('review', 'Near miss involving a serious-risk mechanism',
     r'\b(?:near\s+miss|almost|nearly|came\s+close|could\s+have)\b.{0,120}\b(?:fall|forklift|vehicle|crane|suspended\s+load|electrical|energized|confined|explosion|pressure|caught|crushed|fire|smoke|gas|leak)\b'),
]

def assess_safety_evidence(text):
    low = text.lower()
    for level, reason, pattern in SAFETY_EVIDENCE_RULES:
        if re.search(pattern, low):
            return level, reason
    return 'model', 'No explicit high-consequence mechanism detected'


def infer_operational_fields(text, rule):
    low = text.lower()
    activity = 'General operations'
    if any(k in low for k in ('forklift','vehicle','driving','truck','excavat')): activity = 'Mobile equipment / vehicle operations'
    elif any(k in low for k in ('crane','lifting','suspended load','rigging')): activity = 'Lifting operations'
    elif re.search(r'\b(?:same\s+level|stairs?|stairway|walkway|ground|wet\s+floor)\b', low) and re.search(r'\b(?:slip|slipped|trip|tripped|fell|fallen)\b', low): activity = 'Access / walkway operations'
    elif any(k in low for k in ('harness','scaffold','ladder','height','fall','fell','fallen','falling','roof')): activity = 'Working at height'
    elif any(k in low for k in ('drill','drilled','drilling','machine','machinery','conveyor','roller','press','lathe','tool','equipment','knife','blade','sawing')): activity = 'Machinery / tool operations'
    elif any(k in low for k in ('lockout','loto','isolation','valve','pressure','zero energy','energized')): activity = 'Energy isolation / maintenance'
    elif any(k in low for k in ('weld','grind','flame','hot work','cutting')): activity = 'Hot work'
    elif 'confined' in low or 'tank' in low: activity = 'Confined space entry'
    elif any(k in low for k in ('excavat','trench','digging')): activity = 'Excavation / ground disturbance'
    elif any(k in low for k in ('chemical','acid','caustic','toxic','gas leak','gas smell','fuel smell','burning smell','burnt smell','smoke','sparking','overheat','overheating')): activity = 'Process / equipment safety'

    hazard = 'Unsafe condition or unsafe act'
    if re.search(r'\b(?:same\s+level|stairs?|stairway|walkway|ground|wet\s+floor)\b', low) and re.search(r'\b(?:slip|slipped|trip|tripped|fell|fallen)\b', low): hazard = 'Slip / trip / fall on same level'
    elif any(k in low for k in ('fall','fell','fallen','falling','height','harness','scaffold','ladder','roof')): hazard = 'Fall from height'
    elif any(k in low for k in ('caught','trapped','pinned','crushed','smashed','entangled','drill','drilled','machine','conveyor','roller','press','tool')): hazard = 'Machinery / tool contact and caught-in exposure'
    elif any(k in low for k in ('electric shock','electrical shock','electrocution','live wire','energized','arc flash','sparking','arcing')): hazard = 'Electrical shock / arc-flash exposure'
    elif any(k in low for k in ('pressure','valve','isolation','lockout','loto','energized')): hazard = 'Unexpected energy release'
    elif any(k in low for k in ('crane','suspended','forklift','struck','vehicle','run over','backed over')): hazard = 'Struck-by / line-of-fire exposure'
    elif 'confined' in low: hazard = 'Confined-space exposure'
    elif re.search(r'(?:smell(?:ed|s)?|odor|odour|scent).{0,50}(?:burning|burnt|smoke|scorch|overheat)|(?:burning|burnt|smoke|scorch|overheat|overheating).{0,50}(?:smell|odor|odour|scent)?', low): hazard = 'Fire / overheating / possible ignition source'
    elif re.search(r'(?:smell(?:ed|s)?|odor|odour|scent).{0,50}(?:gas|fuel|diesel|petrol|chemical|h2s)|(?:gas|fuel|diesel|petrol|chemical|h2s).{0,50}(?:smell|odor|odour|leak|leaking|hissing)', low): hazard = 'Gas / chemical release or toxic exposure'
    elif any(k in low for k in ('chemical','acid','caustic','toxic','gas leak','gas smell','fuel smell','h2s')): hazard = 'Chemical / toxic exposure'
    elif any(k in low for k in ('cut','lacerat','puncture','pierce','knife','blade')): hazard = 'Cut / puncture injury'

    barrier = 'Required work control / physical barrier'
    if rule == 'Energy Isolation': barrier = 'Lockout / tagout and zero-energy verification'
    elif rule == 'Working at Height': barrier = 'Fall protection and safe access'
    elif rule == 'Lifting Operations': barrier = 'Exclusion zone and lifting controls'
    elif rule == 'Line of Fire': barrier = 'Exclusion zone and line-of-fire controls'
    elif rule == 'Hot Work': barrier = 'Hot-work permit and fire protection'
    elif rule == 'Confined Space': barrier = 'Permit, gas testing and standby control'
    elif any(k in low for k in ('drill','drilled','drilling','machine','machinery','conveyor','roller','press','lathe','tool')): barrier = 'Machine guarding, tool safety and safe operating procedure'
    elif re.search(r'(?:smell(?:ed|s)?|odor|odour|scent).{0,50}(?:burning|burnt|smoke|scorch|overheat)|(?:burning|burnt|smoke|scorch|overheat|overheating).{0,50}(?:smell|odor|odour|scent)?', low): barrier = 'Isolate the suspected source, investigate and verify fire/electrical controls before continuing'
    elif any(k in low for k in ('chemical','acid','caustic','toxic','gas leak','gas smell','fuel smell','h2s')): barrier = 'Chemical controls, PPE and exposure monitoring'
    elif any(k in low for k in ('cut','lacerat','puncture','knife','blade')): barrier = 'Tool control, guarding and cut-resistant PPE'
    if any(k in low for k in ('drill','drilled','drilling','machine','machinery','conveyor','roller','press','lathe','tool','caught','trapped','pinned','crushed')):
        barrier = 'Machine guarding, tool safety and safe operating procedure'
    elif any(k in low for k in ('cut','lacerat','puncture','pierce','knife','blade')):
        barrier = 'Tool control, guarding and cut-resistant PPE'

    consequence = 'Potential serious injury if the control fails.'
    if any(k in low for k in ('fall','fell','fallen','falling','height')): consequence = 'Potential fall resulting in serious injury or fatality.'
    elif any(k in low for k in ('caught','trapped','pinned','crushed','smashed','entangled')): consequence = 'Potential crush injury, amputation or fatality.'
    elif any(k in low for k in ('drill','drilled','drilling','cut','lacerat','puncture','knife','blade','tool')): consequence = 'Potential hand, limb or other contact injury; severity requires HSE review.'
    elif any(k in low for k in ('electric shock','electrical shock','electrocution','live wire','energized','arc flash','sparking','arcing')): consequence = 'Potential electric shock, arc flash, burns or fatality.'
    elif re.search(r'(?:smell(?:ed|s)?|odor|odour|scent).{0,50}(?:gas|fuel|diesel|petrol|chemical|h2s)|(?:gas|fuel|diesel|petrol|chemical|h2s).{0,50}(?:smell|odor|odour|leak|leaking|hissing)', low): consequence = 'Potential toxic exposure, fire or explosion if the source is not isolated and investigated.'
    elif any(k in low for k in ('pressure','valve','energy','loto','lockout','energized')): consequence = 'Potential unexpected energy release with serious injury or fatality.'
    elif any(k in low for k in ('crane','suspended','forklift','vehicle','struck','run over')): consequence = 'Potential struck-by or crushing injury.'
    elif re.search(r'(?:smell(?:ed|s)?|odor|odour|scent).{0,50}(?:burning|burnt|smoke|scorch|overheat)|(?:burning|burnt|smoke|scorch|overheat|overheating).{0,50}(?:smell|odor|odour|scent)?', low): consequence = 'Potential fire, electrical failure or equipment damage if the source is not isolated and investigated.'
    elif any(k in low for k in ('chemical','acid','caustic','toxic','gas leak','gas smell','fuel smell','h2s')): consequence = 'Potential toxic exposure, chemical burn or serious injury.'
    return activity, hazard, barrier, consequence


def semantic_safety_review(text, model_sif_probability):
    """Use Gemini only for ambiguous narratives the local safety ontology cannot map."""
    api_key = os.getenv('GEMINI_API_KEY', '').strip()
    if not api_key or not text.strip() or not (10.0 <= float(model_sif_probability) <= 80.0):
        return None
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        prompt = f"""You are a conservative industrial HSE safety screener. Analyze this employee observation:

{json.dumps(text.strip())}

Classify the strongest safety concern using ONLY this JSON schema:
{{"level":"critical|high|review|model","reason":"short mechanism description","rule":"Working at Height|Energy Isolation|Lifting Operations|Line of Fire|Hot Work|Confined Space|Excavation|Driving / Mobile Equipment|General Safety","hazard":"short hazard description","action":"short immediate control/review action"}}

Guidance:
- critical = an actual event/exposure with a credible fatality or permanent-harm mechanism.
- high = a credible serious-risk precursor or dangerous condition that needs prompt HSE attention even if nobody was hurt (for example burning smell, smoke, sparks, gas odor/leak, overheating equipment, missing critical controls).
- review = injury or concern needing HSE review but with no clear serious-risk mechanism.
- model = no explicit serious-risk mechanism.
- Do not invent an injury or hazard source not stated.
Return JSON only."""
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0, response_mime_type='application/json')
        )
        raw=(response.text or '').strip()
        if raw.startswith('```'):
            raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw,flags=re.I|re.S).strip()
        data=json.loads(raw)
        if data.get('level') in {'critical','high','review','model'}:
            return data
    except Exception as exc:
        print(f'[OIL-SIF] Semantic safety review skipped: {exc}')
    return None

def classify_text(text):
    """Hybrid safety screening: ML model + deterministic high-consequence rules.

    The ML probability is retained as model_sif_probability.  A separate
    screening score is raised when the narrative explicitly describes a known
    high-consequence mechanism.  This prevents short employee reports such as
    'guy fell from 10th floor' or 'a guy drilled his hand' from being treated as
    ordinary text-classification examples, while avoiding the claim that every
    injury is automatically an SIF.
    """
    clean = text.strip()
    evidence_level, evidence_reason = assess_safety_evidence(clean)

    is_sif = False
    confidence = 76.0
    model_sif_probability = 24.0
    sif_model_backed = False
    lsr_model_backed = False
    rule_name = 'General Safety'
    lsr_model_prediction = 'General Safety'
    lsr_confidence = 0.0

    if _sif_model is not None:
        try:
            pred = _sif_model.predict([clean])[0]
            is_sif = bool(pred == 1 or 'SIF' in str(pred))
            if hasattr(_sif_model, 'predict_proba'):
                probs = _sif_model.predict_proba([clean])[0]
                classes = list(getattr(_sif_model, 'classes_', range(len(probs))))
                positive = 0.0
                for c, prob in zip(classes, probs):
                    if str(c).strip().lower() in {'1','true','sif','sif potential'} or 'sif' in str(c).strip().lower():
                        positive = float(prob)
                        break
                else:
                    positive = float(probs[-1]) if len(probs) else 0.0
                model_sif_probability = round(positive * 100, 1)
                confidence = round((positive if is_sif else 1-positive) * 100, 1)
            else:
                model_sif_probability = 100.0 if is_sif else 0.0
                confidence = 100.0
            sif_model_backed = True
        except Exception as exc:
            print(f'[OIL-SIF] SIF inference error: {exc}')

    if not sif_model_backed:
        lowered = clean.lower()
        is_sif = any(k in lowered for k in ('harness','height','fall','pressure','crane','valve','fire','confined','lockout','loto','suspended','forklift'))
        model_sif_probability = 91.0 if is_sif else 9.0
        confidence = 91.0

    semantic = None
    semantic_hazard = None
    if evidence_level == 'model':
        semantic = semantic_safety_review(clean, model_sif_probability)
        if semantic:
            evidence_level = semantic.get('level', 'model')
            evidence_reason = semantic.get('reason', 'Semantic safety concern detected')
            semantic_hazard = semantic.get('hazard')
            if semantic.get('rule'):
                rule_name = semantic['rule']

    aliases = {
        'Safe mechanical lifting':'Lifting Operations',
        'Working at height':'Working at Height',
        'Bypassing safety controls':'Energy Isolation',
        'Hot work':'Hot Work',
        'Confined space':'Confined Space',
        'Driving':'Driving / Mobile Equipment',
        'Driving / mobile equipment':'Driving / Mobile Equipment',
        'Excavation':'Excavation',
    }
    if _lsr_model is not None:
        try:
            raw_rule = str(_lsr_model.predict([clean])[0])
            lsr_model_prediction = aliases.get(raw_rule, raw_rule)
            rule_name = lsr_model_prediction
            if hasattr(_lsr_model, 'predict_proba'):
                lsr_probs = _lsr_model.predict_proba([clean])[0]
                lsr_confidence = round(float(np.max(lsr_probs)) * 100, 1)
            else:
                lsr_confidence = 100.0
            lsr_model_backed = True
        except Exception as exc:
            print(f'[OIL-SIF] LSR inference error: {exc}')

    low = clean.lower()
    explicit_rule_patterns = [
        ('Working at Height', r'\b(?:fall|fell|fallen|falling|roof|scaffold|ladder|height|elevated)\b'),
        ('Energy Isolation', r'\b(?:lock[- ]?out|tag[- ]?out|loto|isolation|energized|live\s+wire|electric(?:al)?\s+shock|electrocution|high\s+voltage|pressure\s+release|arc\s*flash|sparking|arcing|short\s+circuit)\b'),
        ('Confined Space', r'\b(?:confined\s+space|confined\s+vessel|tank)\b'),
        ('Hot Work', r'\b(?:hot\s+work|welding|weld(?:ed|ing)?|cutting|grinding|flame|explosion|flash\s+fire|fireball)\b'),
        ('Lifting Operations', r'\b(?:crane|lifting|rigging|hoist|suspended\s+load|hanging\s+load)\b'),
        ('Driving / Mobile Equipment', r'\b(?:forklift|vehicle|truck|driving|excavator|mobile\s+equipment|run\s+over|backed\s+over)\b'),
        ('Excavation', r'\b(?:excavat(?:ion|e|ed|ing)|trench|cave[- ]?in|buried)\b'),
        ('Line of Fire', r'\b(?:struck|caught|trapped|pinned|crushed|smashed|entangled|line\s+of\s+fire|falling\s+object|machine|machinery|conveyor|roller|press|lathe|drill|drilling|(?:circular\s+)?sawing|saw\s+blade|tool)\b'),
    ]
    explicit_rule = next((name for name, pattern in explicit_rule_patterns if re.search(pattern, low)), None)
    if explicit_rule:
        rule_name = explicit_rule
    elif not lsr_model_backed or lsr_confidence < 55.0:
        rule_name = 'General Safety'
        if not lsr_model_backed:
            lsr_confidence = 0.0

    if rule_name in ('None','nan','', 'Unknown'):
        rule_name='General Safety'

    # Deterministic screening backstop.  The score is a screening score, not
    # a calibrated probability.  Keep the raw ML probability separately.
    if evidence_level == 'critical':
        is_sif = True
        sif_probability = max(95.0, model_sif_probability)
        confidence = max(95.0, confidence)
    elif evidence_level == 'high':
        is_sif = True
        sif_probability = max(82.0, model_sif_probability)
        confidence = max(82.0, confidence)
    elif evidence_level == 'review':
        # A reported injury needs human review, but is not automatically an SIF.
        is_sif = bool(model_sif_probability >= 50.0)
        sif_probability = max(65.0, model_sif_probability)
        confidence = max(65.0, confidence)
    else:
        sif_probability = model_sif_probability

    if semantic and semantic.get('level') == 'critical':
        is_sif = True
        sif_probability = max(95.0, model_sif_probability)
        confidence = max(95.0, confidence)
    elif semantic and semantic.get('level') == 'high':
        is_sif = True
        sif_probability = max(80.0, model_sif_probability)
        confidence = max(80.0, confidence)
    elif semantic and semantic.get('level') == 'review':
        is_sif = bool(model_sif_probability >= 50.0)
        sif_probability = max(65.0, model_sif_probability)
        confidence = max(65.0, confidence)

    # Make the rule mapping consistent with explicit evidence.
    if evidence_reason == 'Actual fall from height':
        rule_name = 'Working at Height'; lsr_model_prediction = 'Working at Height'
    elif any(x in evidence_reason for x in ('Caught/crushed','Amputation','Struck by vehicle','suspended load')):
        rule_name = 'Line of Fire'; lsr_model_prediction = 'Line of Fire'
    elif 'Electrocution' in evidence_reason or 'High-pressure' in evidence_reason:
        rule_name = 'Energy Isolation'; lsr_model_prediction = 'Energy Isolation'
    elif 'Explosion' in evidence_reason:
        rule_name = 'Hot Work'; lsr_model_prediction = 'Hot Work'
    elif 'Confined-space' in evidence_reason:
        rule_name = 'Confined Space'; lsr_model_prediction = 'Confined Space'
    elif any(x in evidence_reason for x in ('Tool / machinery injury','Powered-tool injury','Caught/crushed','Amputation','Suspended-load / line-of-fire')):
        rule_name = 'Line of Fire'; lsr_model_prediction = 'Line of Fire'
    elif evidence_reason == 'Gas leak / hazardous release':
        rule_name = 'General Safety'; lsr_model_prediction = 'General Safety'
    elif any(x in evidence_reason for x in ('Severe injury','Other reported injury')) and evidence_level in ('high','review') and rule_name == 'Hot Work':
        rule_name = 'General Safety'; lsr_model_prediction = 'General Safety'

    activity, hazard, barrier, consequence = infer_operational_fields(clean, rule_name)
    if semantic_hazard:
        hazard = semantic_hazard
    if semantic and semantic.get('action'):
        barrier = semantic.get('action')
    if evidence_level == 'critical':
        band = 'Critical screening'
        priority = 100
    elif evidence_level == 'high':
        band = 'High-priority review'
        priority = 90
    elif evidence_level == 'review':
        band = 'HSE review'
        priority = 70
    else:
        band = 'High SIF probability' if sif_probability >= 80 else 'Review zone' if sif_probability >= 45 else 'Low SIF probability'
        priority = 70 if is_sif else 30

    return {
        'is_sif': is_sif, 'confidence': confidence, 'sif_probability': round(float(sif_probability),1),
        'model_sif_probability': round(float(model_sif_probability),1),
        'screening_score': round(float(sif_probability),1),
        'evidence_level': evidence_level, 'evidence_reason': evidence_reason,
        'rule_name': rule_name, 'lsr_model_prediction': lsr_model_prediction, 'lsr_confidence': lsr_confidence,
        'model_backed': bool(sif_model_backed or lsr_model_backed),
        'sif_model_backed': sif_model_backed, 'lsr_model_backed': lsr_model_backed,
        'activity': activity, 'hazard': hazard, 'barrier': barrier, 'potential_consequence': consequence,
        'confidence_band': band, 'priority_score': priority
    }

def make_notification(username, title, text, icon='ℹ️'):
    with STORE_LOCK:
        bucket = notifications_store.setdefault(username, [])
        bucket.append({'id': secrets.token_urlsafe(8), 'title': title, 'text': text, 'icon': icon,
                       'time': datetime.now().astimezone().strftime('%d %b %Y, %I:%M %p'), 'read': False})
        notifications_store[username] = bucket[-50:]
        save_runtime_state()


def _split_recipients(value):
    return [x.strip() for x in str(value or '').replace(';', ',').split(',') if x.strip()]

def send_hse_email(subject, body, immediate=False):
    # Every submitted employee safety report is eligible for an HSE email alert.
    # HSE_ALERT_EMAILS is preferred; HSE_EMERGENCY_EMAIL is a convenient fallback.
    configured_recipients=os.getenv('HSE_ALERT_EMAILS','').strip() or os.getenv('HSE_EMERGENCY_EMAIL','').strip()
    recipients=_split_recipients(configured_recipients)
    host=os.getenv('SMTP_HOST','').strip(); sender=os.getenv('SMTP_FROM','').strip()
    username=os.getenv('SMTP_USERNAME','').strip(); password=os.getenv('SMTP_PASSWORD','')
    if not recipients or not host or not sender:
        return {'sent':False,'configured':False,'reason':'SMTP is not configured. Set HSE_ALERT_EMAILS (or HSE_EMERGENCY_EMAIL), SMTP_HOST and SMTP_FROM in .env.'}
    try:
        msg=EmailMessage()
        msg['Subject']=('🚨 ' if immediate else '')+subject
        msg['From']=sender
        msg['To']=', '.join(recipients)
        msg.set_content(body)
        with smtplib.SMTP(host,int(os.getenv('SMTP_PORT','587')),timeout=15) as smtp:
            if os.getenv('SMTP_TLS','true').lower()=='true': smtp.starttls()
            if username: smtp.login(username,password)
            smtp.send_message(msg)
        return {'sent':True,'configured':True,'recipients':recipients}
    except Exception as exc:
        print(f'[OIL-SIF] HSE email alert failed: {exc}')
        return {'sent':False,'configured':True,'reason':str(exc)}

def notify_hse_team(record):
    probability=float(record.get('sif_probability',0)); emergency=bool(record.get('immediate_danger')); critical=probability>=80
    level='EMERGENCY' if emergency else 'CRITICAL' if critical else 'HIGH'
    title=f'{level}: New safety report {record["report_id"]}'
    submitted_at=record.get('created_at','')
    body=(f'OIL-SIF Safety Intelligence Platform\n\n'
          f'A new safety report has been submitted and requires HSE review.\n\n'
          f'Report ID: {record["report_id"]}\n'
          f'Submitted by: {record.get("submitted_by_name") or record.get("username")}\n'
          f'Submitted at: {submitted_at}\n'
          f'Site: {record.get("site")}\n'
          f'Location: {record.get("location")}\n'
          f'Report type: {record.get("report_type")}\n'
          f'Immediate danger: {"YES" if emergency else "No"}\n'
          f'SIF probability: {probability:.1f}%\n'
          f'Life-Saving Rule: {record.get("life_saving_rule")}\n'
          f'Hazard: {record.get("hazard")}\n'
          f'Barrier: {record.get("barrier")}\n'
          f'Potential consequence: {record.get("potential_consequence")}\n\n'
          f'Observation:\n{record.get("text")}\n\n'
          f'Photo attached in the report system: {"Yes" if record.get("photo_url") else "No"}\n\n'
          'Please review the report in the HSE Review Queue and record the corrective action.')
    for uname,u in users_db.items():
        if normalize_role(u.get('role'))=='HSE Officer':
            make_notification(uname,title,body,'🚨' if emergency or critical else '⚠️')
    # Email is sent for every report, not only SIF/critical reports.
    email=send_hse_email(title,body,immediate=emergency or critical)
    return {'email':email}

def submitted_for_user(username):
    return [r for r in submitted_reports if r.get('username') == username]

def operational_row(r):
    return {
        'report_id': r.get('report_id'), 'date_of_incident': r.get('created_at','')[:10],
        'activity_group': r.get('activity'), 'precursor': r.get('hazard'),
        'life_saving_rule': r.get('life_saving_rule'), 'sif_probability': float(r.get('sif_probability',0))/100 if float(r.get('sif_probability',0)) > 1 else float(r.get('sif_probability',0)),
        'model_sif_probability': float(r.get('model_sif_probability', r.get('sif_probability',0))),
        'evidence_level': r.get('evidence_level','model'), 'evidence_reason': r.get('evidence_reason',''),
        'model_backed': bool(r.get('sif_model_backed', False) or r.get('lsr_model_backed', False)), 'sif_model_backed': bool(r.get('sif_model_backed', False)), 'lsr_model_backed': bool(r.get('lsr_model_backed', False)), 'lsr_confidence': float(r.get('lsr_confidence',0)),
        'sif_prediction': 'SIF Potential' if r.get('is_sif') else 'Non-SIF Potential',
        'confidence_band': r.get('confidence_band'), 'hse_review_status': r.get('review_status','Pending HSE review'),
        'report_text': r.get('text'), 'site': r.get('site'), 'location': r.get('location'), 'barrier': r.get('barrier'),
        'potential_consequence': r.get('potential_consequence'), 'submitted_by': r.get('username'), 'photo_url': r.get('photo_url'),
        'immediate_danger': r.get('immediate_danger',False), 'hse_decision': r.get('hse_decision'), 'hse_reason': r.get('hse_reason'), 'corrective_action': r.get('corrective_action')
    }

def all_operational_rows():
    rows = [operational_row(r) for r in submitted_reports]
    return rows

@app.post('/api/scan')
def scan_hazard(req: ScanRequest, user=Depends(require_role('Employee', 'HSE Officer'))):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail='Please enter observation details first.')
    result = classify_text(text)
    return {'is_sif': result['is_sif'], 'confidence': result['confidence'], 'sif_probability': result.get('sif_probability', result['confidence']), 'rule_name': result['rule_name'],
            'lsr_confidence': result.get('lsr_confidence', 0), 'lsr_model_prediction': result.get('lsr_model_prediction', result['rule_name']), 'model_backed': result['model_backed'], 'sif_model_backed': result.get('sif_model_backed', False), 'lsr_model_backed': result.get('lsr_model_backed', False), 'activity': result['activity'], 'hazard': result['hazard'],
            'barrier': result['barrier'], 'potential_consequence': result['potential_consequence'],
            'confidence_band': result['confidence_band'], 'priority_score': result['priority_score']}

@app.post('/api/chat')
def chat(req: ChatRequest, user=Depends(require_role('HSE Officer'))):
    username = user.get('username')

    if req.reset:
        _chat_sessions.pop(username, None)

    question = (req.question or '').strip()
    if not question:
        return {'reply': 'Conversation cleared.' if req.reset else 'Please enter a question.', 'source': 'system'}

    try:
        from chatbot.assistant import answer_question
        existing_chat = _chat_sessions.get(username)
        answer, updated_chat = answer_question(question, existing_chat)

        if updated_chat is not None:
            if username not in _chat_sessions and len(_chat_sessions) >= _CHAT_SESSION_LIMIT:
                # Simple cap so a long-running demo process can't accumulate
                # sessions forever; the oldest-inserted session is evicted.
                _chat_sessions.pop(next(iter(_chat_sessions)))
            _chat_sessions[username] = updated_chat

        return {'reply': str(answer), 'source': 'gemini'}
    except Exception as exc:
        print(f'[OIL-SIF] Chat error: {exc}')
        return {'reply': 'The AI Copilot is temporarily unavailable. The dashboard data is still available.', 'source': 'fallback'}

def compact_records(df, limit=None):
    if df.empty:
        return []
    work = df.head(limit).copy() if limit else df.copy()
    # Avoid sending giant report text unless the endpoint explicitly needs it.
    clean = work.astype(object).where(pd.notnull(work), None).replace([np.inf, -np.inf], None)
    return clean.to_dict(orient='records')

@app.post('/api/reports')
def submit_report(req: SubmitReportRequest, user=Depends(require_role('Employee', 'HSE Officer'))):
    text = req.text.strip()
    if not text: raise HTTPException(status_code=400, detail='Please describe the safety concern.')
    if len(text) > 10000: raise HTTPException(status_code=400, detail='The report description is too long.')
    result = classify_text(text)
    report_id = f"OIL-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
    photo_url = None
    if req.photo_data:
        try:
            header, encoded = req.photo_data.split(',',1) if ',' in req.photo_data else ('',req.photo_data)
            raw = base64.b64decode(encoded, validate=True)
            if len(raw) > 5 * 1024 * 1024: raise ValueError('photo too large')
            ext = '.jpg'
            if 'png' in header.lower(): ext='.png'
            elif 'webp' in header.lower(): ext='.webp'
            filename = report_id + ext
            (UPLOAD_DIR/filename).write_bytes(raw)
            photo_url = f'/api/reports/{report_id}/photo'
        except Exception:
            raise HTTPException(status_code=400, detail='The photo could not be saved. Please try a smaller image.')
    record = {'report_id':report_id,'username':user['username'],'submitted_by_name':user.get('name'),
              'created_at':datetime.now(timezone.utc).isoformat(),'text':text,'site':req.site,'location':req.location,
              'report_type':req.report_type,'immediate_danger':req.immediate_danger,'photo_url':photo_url,
              'is_sif':result['is_sif'],'sif_probability':result.get('sif_probability', result['confidence']),'model_sif_probability':result.get('model_sif_probability', result.get('sif_probability', result['confidence'])),'screening_score':result.get('screening_score', result.get('sif_probability', result['confidence'])),'evidence_level':result.get('evidence_level','model'),'evidence_reason':result.get('evidence_reason',''),'confidence':result['confidence'],'lsr_confidence':result.get('lsr_confidence',0),'lsr_model_prediction':result.get('lsr_model_prediction',result['rule_name']),'sif_model_backed':result.get('sif_model_backed',False),'lsr_model_backed':result.get('lsr_model_backed',False),'confidence_band':result['confidence_band'],
              'activity':result['activity'],'hazard':result['hazard'],'life_saving_rule':result['rule_name'],
              'barrier':result['barrier'],'potential_consequence':result['potential_consequence'],
              'priority_score':result['priority_score'],'review_status':'Pending HSE review'}
    with STORE_LOCK:
        submitted_reports.append(record); save_runtime_state()
    make_notification(user['username'],'Safety report submitted',f'{report_id} has been saved and sent for HSE review.','✓')
    if req.immediate_danger:
        make_notification(user['username'],'Immediate danger reported',f'{report_id} was marked as immediate danger. Stop the work if safe to do so and contact HSE/supervision.','🚨')
    alerts=notify_hse_team(record)
    return {'ok':True,'report':operational_row(record),'scan':result,'alerts':alerts}

@app.get('/api/reports/my')
def my_reports(user=Depends(require_role('Employee'))):
    rows = sorted(submitted_for_user(user['username']), key=lambda x:x.get('created_at',''), reverse=True)
    return {'rows':[operational_row(r) for r in rows], 'total':len(rows)}

@app.get('/api/reports/{report_id}')
def get_report_detail(report_id: str, user=Depends(current_user)):
    for r in submitted_reports:
        if r.get('report_id') == report_id:
            if user['role'] == 'Employee' and r.get('username') != user['username']:
                raise HTTPException(status_code=403, detail='You can only view your own submitted reports.')
            return {'report':operational_row(r), 'source':'submitted'}
    if user['role'] != 'HSE Officer': raise HTTPException(status_code=404, detail='Report not found.')
    mdf = get_master_df()
    match = mdf[mdf.get('report_id', pd.Series(dtype=str)).astype(str).eq(report_id)] if not mdf.empty else pd.DataFrame()
    if match.empty: raise HTTPException(status_code=404, detail='Report not found.')
    row = compact_records(match.head(1))[0]
    review = hse_reviews.get(report_id, {})
    row.update({'hse_decision':review.get('decision'),'hse_reason':review.get('reason'),'corrective_action':review.get('action')})
    if review:
        row['hse_review_status'] = 'Needs more information' if review.get('decision') == 'Needs More Information' else 'Reviewed'
    return {'report':row,'source':'dataset'}

@app.get('/api/reports/{report_id}/photo')
def get_report_photo(report_id: str, user=Depends(current_user)):
    for ext in ('.jpg','.png','.webp'):
        path=UPLOAD_DIR/(report_id+ext)
        if path.exists():
            from fastapi.responses import FileResponse
            return FileResponse(path)
    raise HTTPException(status_code=404, detail='No photo attached.')

@app.post('/api/reports/{report_id}/review')
def review_report(report_id: str, req: ReviewRequest, user=Depends(require_role('HSE Officer'))):
    decision = req.decision.strip()
    allowed = {'Confirm SIF','Not SIF','Needs More Information'}
    if decision not in allowed: raise HTTPException(status_code=400, detail='Invalid HSE decision.')
    target = next((r for r in submitted_reports if r.get('report_id')==report_id), None)
    if target:
        target['hse_decision']=decision; target['hse_reason']=req.reason.strip(); target['corrective_action']=req.action.strip()
        target['review_status']='Reviewed' if decision != 'Needs More Information' else 'Needs more information'
        with STORE_LOCK: save_runtime_state()
        owner=target.get('username')
    else:
        owner=None
        mdf = get_master_df()
        if mdf.empty or not mdf.get('report_id',pd.Series(dtype=str)).astype(str).eq(report_id).any():
            raise HTTPException(status_code=404, detail='Report not found.')
        hse_reviews[report_id]={'decision':decision,'reason':req.reason.strip(),'action':req.action.strip(),'reviewed_by':user['username'],'at':datetime.now(timezone.utc).isoformat()}
        save_runtime_state()
    if owner:
        make_notification(owner,'HSE review updated',f'{report_id}: {decision}.','✓')
    return {'ok':True,'report_id':report_id,'decision':decision,'reason':req.reason.strip(),'action':req.action.strip()}

@app.get('/api/emergency-contact')
def emergency_contact(user=Depends(current_user)):
    return {'hse_email': os.getenv('HSE_EMERGENCY_EMAIL', os.getenv('HSE_ALERT_EMAILS','')).split(',')[0].strip(),
            'hse_phone': os.getenv('HSE_EMERGENCY_PHONE','').strip(),
            'emergency_number': os.getenv('SITE_EMERGENCY_NUMBER','').strip()}

@app.get('/api/notifications')
def get_notifications(user=Depends(current_user)):
    return {'notifications':notifications_store.get(user['username'], [])[-30:]}

@app.post('/api/notifications/read')
def mark_notifications_read(user=Depends(current_user)):
    with STORE_LOCK:
        for item in notifications_store.get(user['username'],[]): item['read']=True
        save_runtime_state()
    return {'ok':True}

@app.get('/api/dashboard/summary')
def dashboard_summary(days:int=30,site:str='',user=Depends(require_role('HSE Officer','Management'))):
    days=max(1,min(days,3650)); cutoff=datetime.now(timezone.utc)-timedelta(days=days)
    recent=[r for r in submitted_reports if r.get('created_at') and r.get('created_at') >= cutoff.isoformat() and (not site or r.get('site')==site)]
    sif=sum(bool(r.get('is_sif')) for r in recent); critical=sum(bool(r.get('is_sif')) and float(r.get('sif_probability',0))>=80 for r in recent)
    pending=sum(r.get('review_status')=='Pending HSE review' and (not site or r.get('site')==site) for r in submitted_reports)
    by_rule={}
    by_activity={}
    for r in recent:
        if r.get('is_sif'): by_rule[r.get('life_saving_rule','General Safety')]=by_rule.get(r.get('life_saving_rule','General Safety'),0)+1
        by_activity[r.get('activity','General operations')]=by_activity.get(r.get('activity','General operations'),0)+1
    return {'period_days':days,'site':site or 'All facilities','submitted_reports':len(recent),'sif_potential':sif,'critical':critical,'pending_hse_review':pending,
            'top_life_saving_rules':sorted([{'name':k,'count':v} for k,v in by_rule.items()],key=lambda x:x['count'],reverse=True)[:8],
            'top_activities':sorted([{'name':k,'count':v} for k,v in by_activity.items()],key=lambda x:x['count'],reverse=True)[:8]}

# ---------------------------------------------------------------------------
# Management demonstration facility data
# ---------------------------------------------------------------------------
# The historical OSHA/ITA master dataset does not contain the OIL-SIF facility
# identifier, so it cannot truthfully be distributed across the four demo sites.
# Instead, empty facilities get a small deterministic demonstration dataset.
# These records are used only by Management's site comparison/drill-down and are
# clearly marked as demo evidence; employee/HSE live submissions always win.
DEMO_SITE_REPORTS = [
    # Site A — high density
    *[{'report_id': f'DEMO-A-{i:02d}', 'site': 'Offshore Platform Alpha', 'activity': a, 'hazard': h, 'barrier': b,
       'life_saving_rule': rule, 'is_sif': True, 'sif_probability': prob, 'confidence_band': 'High SIF probability',
       'text': f'Demonstration SIF precursor: {h}.', 'location': 'Demo area', 'review_status': 'Demonstration baseline'}
      for i,(a,h,b,rule,prob) in enumerate([
        ('Working at height','Dropped object / fall exposure','Fall protection and dropped-object controls','Working at height',91),
        ('Energy isolation / maintenance','Unexpected energy release','Lockout / tagout and zero-energy verification','Energy Isolation',88),
        ('Lifting operations','Suspended load / line of fire','Lift plan and exclusion zone','Line of Fire',86),
        ('Confined space entry','Hazardous atmosphere','Gas testing and entry permit','Confined Space',83),
        ('Hot work','Fire / explosion exposure','Hot-work permit and gas testing','Hot Work',81),
      ], start=1)],
    *[{'report_id': f'DEMO-A-{i:02d}', 'site': 'Offshore Platform Alpha', 'activity': a, 'hazard': h, 'barrier': b,
       'life_saving_rule': rule, 'is_sif': False, 'sif_probability': prob, 'confidence_band': 'Review zone',
       'text': f'Demonstration precursor: {h}.', 'location': 'Demo area', 'review_status': 'Demonstration baseline'}
      for i,(a,h,b,rule,prob) in enumerate([
        ('Material handling','Manual handling strain','Mechanical aid / correct lifting technique','Safe Lifting',57),
        ('Inspection','Slip / trip exposure','Housekeeping and access controls','Working at height',51),
        ('Process operations','Minor process deviation','Process alarms and operating procedure','Process Safety',48),
        ('Driving','Roadway incident exposure','Seatbelt and journey controls','Driving Safety',45),
        ('Maintenance','Tool-related injury','Tool inspection and correct use','Safe Lifting',42),
        ('Warehouse operations','Falling object exposure','Storage and exclusion controls','Line of Fire',38),
        ('Electrical maintenance','Electrical contact exposure','Isolation and test-before-touch','Energy Isolation',34),
        ('Patrolling','Environmental exposure','Journey and field controls','Driving Safety',29),
        ('Housekeeping','Slip / trip exposure','Housekeeping controls','Working at height',24),
      ], start=6)],
    # Site B — moderate density
    *[{'report_id': f'DEMO-B-{i:02d}', 'site': 'Refinery Complex Beta', 'activity': a, 'hazard': h, 'barrier': b,
       'life_saving_rule': rule, 'is_sif': True, 'sif_probability': prob, 'confidence_band': 'High SIF probability',
       'text': f'Demonstration SIF precursor: {h}.', 'location': 'Demo area', 'review_status': 'Demonstration baseline'}
      for i,(a,h,b,rule,prob) in enumerate([
        ('Mobile equipment','Vehicle / pedestrian interaction','Segregation and spotter controls','Line of Fire',82),
      ], start=1)],
    *[{'report_id': f'DEMO-B-{i:02d}', 'site': 'Refinery Complex Beta', 'activity': a, 'hazard': h, 'barrier': b,
       'life_saving_rule': rule, 'is_sif': False, 'sif_probability': prob, 'confidence_band': 'Review zone',
       'text': f'Demonstration precursor: {h}.', 'location': 'Demo area', 'review_status': 'Demonstration baseline'}
      for i,(a,h,b,rule,prob) in enumerate([
        ('Material handling','Manual handling strain','Mechanical aid / correct lifting technique','Safe Lifting',54),
        ('Maintenance','Unexpected equipment movement','Isolation verification','Energy Isolation',47),
        ('Process operations','Loss of containment','Process alarms and inspection','Process Safety',43),
        ('Driving','Roadway incident exposure','Seatbelt and journey controls','Driving Safety',39),
        ('Working at height','Slip / trip exposure','Housekeeping and access controls','Working at height',35),
        ('Hot work','Localized ignition source','Permit and fire watch','Hot Work',31),
        ('Inspection','Contact with equipment','Safe positioning','Line of Fire',28),
        ('Warehouse operations','Falling object exposure','Storage and exclusion controls','Line of Fire',24),
        ('Electrical maintenance','Electrical contact exposure','Isolation and test-before-touch','Energy Isolation',21),
      ], start=2)],
    # Site C — low density
    *[{'report_id': f'DEMO-C-{i:02d}', 'site': 'Pipeline Sector 4', 'activity': a, 'hazard': h, 'barrier': b,
       'life_saving_rule': rule, 'is_sif': i == 1, 'sif_probability': prob,
       'confidence_band': 'High SIF probability' if i == 1 else 'Review zone',
       'text': f'Demonstration precursor: {h}.', 'location': 'Demo area', 'review_status': 'Demonstration baseline'}
      for i,(a,h,b,rule,prob) in enumerate([
        ('Line maintenance','Unexpected line pressure','Isolation and pressure verification','Energy Isolation',84),
        ('Vehicle movement','Vehicle / pedestrian interaction','Traffic management plan','Line of Fire',52),
        ('Inspection','Slip / trip exposure','Housekeeping and access controls','Working at height',44),
        ('Valve operations','Unexpected release','Isolation verification','Energy Isolation',41),
        ('Excavation','Ground instability','Permit and excavation controls','Ground Disturbance',38),
        ('Lifting operations','Load movement','Lift plan and exclusion zone','Line of Fire',36),
        ('Maintenance','Stored energy','Isolation verification','Energy Isolation',34),
        ('Patrolling','Environmental exposure','Journey and field controls','Driving Safety',32),
        ('Sampling','Chemical exposure','PPE and sampling procedure','Chemical Safety',29),
        ('Housekeeping','Slip / trip exposure','Housekeeping controls','Working at height',27),
        ('Inspection','Contact with equipment','Safe positioning','Line of Fire',25),
        ('Driving','Roadway incident exposure','Seatbelt and journey controls','Driving Safety',23),
        ('Valve operations','Loss of containment','Process controls and inspection','Process Safety',22),
        ('Maintenance','Manual handling strain','Mechanical aid / correct technique','Safe Lifting',20),
        ('Inspection','Dropped object exposure','Dropped-object controls','Working at height',19),
        ('Patrolling','Heat exposure','Heat management controls','Environmental Safety',18),
        ('Line maintenance','Tool-related injury','Tool inspection and correct use','Safe Lifting',17),
        ('Warehouse operations','Falling object exposure','Storage controls','Line of Fire',16),
        ('Sampling','Chemical splash','Chemical handling controls','Chemical Safety',15),
        ('Administration','Ergonomic strain','Ergonomic controls','Other',12),
      ], start=1)],
]

def management_demo_rows(site):
    return [r.copy() for r in DEMO_SITE_REPORTS if r.get('site') == site]

def management_source_rows(site):
    live = [r for r in submitted_reports if r.get('site') == site]
    return live if live else management_demo_rows(site)

@app.get('/api/management/sites')
def management_sites(user=Depends(require_role('Management'))):
    site_names=[
        ('Site A','Offshore Platform Alpha'),
        ('Site B','Refinery Complex Beta'),
        ('Site C','Pipeline Sector 4'),
        ('Site D','Depot Terminal C'),
    ]
    rows=[]
    for sid,name in site_names:
        live=[r for r in submitted_reports if r.get('site')==name]
        source_rows=live if live else management_demo_rows(name)
        total=len(source_rows); sif=sum(bool(r.get('is_sif')) for r in source_rows)
        density=sif/total*100 if total else 0.0
        level='High' if density>=20 else 'Moderate' if density>=8 else 'Low' if total else 'No data'
        rows.append({'id':sid,'name':name,'risk_level':level,'sif_reports':sif,'total_reports':total,
                     'density_pct':round(density,1),'source':'live' if live else 'demo'})
    return {'sites':rows,'note':'Live facility submissions are used when available. Empty facilities use deterministic demonstration records because the historical master data has no facility identifier.'}

@app.get('/api/management/drilldown')
def management_drilldown(site:str='',activity:str='',hazard:str='',barrier:str='',user=Depends(require_role('Management'))):
    raw_rows=management_source_rows(site) if site else list(submitted_reports)
    rows=[operational_row(r) for r in raw_rows]
    demo=not any(r.get('site')==site for r in submitted_reports) if site else False
    if activity: rows=[r for r in rows if str(r.get('activity_group',''))==activity]
    if hazard: rows=[r for r in rows if str(r.get('precursor',''))==hazard]
    if barrier: rows=[r for r in rows if str(r.get('barrier',''))==barrier]
    sif=[r for r in rows if str(r.get('sif_prediction','')).strip().lower() == 'sif potential']
    def counts(key):
        d={}
        for r in sif:
            name=str(r.get(key) or 'Not recorded');d[name]=d.get(name,0)+1
        return [{'name':k,'count':v} for k,v in sorted(d.items(),key=lambda x:x[1],reverse=True)]
    return {'site':site,'activity':activity,'hazard':hazard,'barrier':barrier,'demo':demo,
            'activities':counts('activity_group'),'hazards':counts('precursor'),'barriers':counts('barrier'),'reports':sif[:100]}

# Historical OSHA dataset used by management's location heatmap. The raw dataset
# contains State/City/Employer plus incident event fields, but not an explicit
# normalized operational activity field. We therefore derive a small set of
# operational activity groups from the incident event/narrative fields rather
# than inventing site identifiers.
_LOCATION_DATA_FILE = APP_CORE / 'January2015toNovember2025.csv'
_LOCATION_HEATMAP_CACHE = None
_LOCATION_HEATMAP_LOCK = threading.RLock()

def _activity_group_from_incident(event_title='', source_title='', narrative=''):
    text = ' '.join(str(x or '') for x in (event_title, source_title, narrative)).lower()
    rules = [
        ('Working at height', r'fall to lower level|scaffold|ladder|roof|elevated|height|fall from'),
        ('Lifting & material handling', r'crane|hoist|rigging|suspended load|lifting|pallet jack|forklift|material handling|caught in|compressed by'),
        ('Vehicle & transport', r'truck|tractor|trailer|forklift|vehicle|motor vehicle|roadway|driving|tanker|semi-'),
        ('Machinery & equipment', r'machin|conveyor|press|saw|lathe|mill|equipment|caught in running|powered'),
        ('Hot work', r'weld|torch|cutting|hot work|ignition|flame|fire|explosion'),
        ('Electrical work', r'electrical|electric|energized|arc flash|shock'),
        ('Excavation & ground work', r'excavat|trench|earth|ground collapse|digging'),
        ('Chemical & process', r'chemical|gas|vapou?r|solvent|toxic|corrosive|release|leak|pressure'),
        ('Manual handling & ergonomics', r'lifted|lifting|overexert|strain|ergonomic|repetitive|manual'),
        ('Slips, trips & access', r'slip|trip|stumble|walkway|floor|stairs|same level'),
    ]
    for name, pat in rules:
        import re
        if re.search(pat, text):
            return name
    return 'Other / general operations'

def _load_location_heatmap():
    global _LOCATION_HEATMAP_CACHE
    if _LOCATION_HEATMAP_CACHE is not None:
        return _LOCATION_HEATMAP_CACHE
    with _LOCATION_HEATMAP_LOCK:
        if _LOCATION_HEATMAP_CACHE is not None:
            return _LOCATION_HEATMAP_CACHE
        if not _LOCATION_DATA_FILE.exists():
            _LOCATION_HEATMAP_CACHE = {'locations': [], 'activities': [], 'cells': [], 'total_reports': 0, 'note': 'Location dataset is not available.'}
            return _LOCATION_HEATMAP_CACHE
        try:
            raw = pd.read_csv(_LOCATION_DATA_FILE, low_memory=False, usecols=['State','EventTitle','SourceTitle','Final Narrative'])
            raw['location'] = raw['State'].fillna('Unknown').astype(str).str.strip().str.title()
            raw.loc[raw['location'].isin(['','Nan','None']), 'location'] = 'Unknown'
            raw['activity'] = [
                _activity_group_from_incident(e, s, n)
                for e, s, n in zip(raw['EventTitle'], raw['SourceTitle'], raw['Final Narrative'])
            ]
            # Keep the most informative locations and activities visible without
            # making the management view unreadably wide.
            top_locations = raw.groupby('location').size().nlargest(10).index.tolist()
            top_activities = raw.groupby('activity').size().nlargest(10).index.tolist()
            scoped = raw[raw.location.isin(top_locations) & raw.activity.isin(top_activities)]
            cells=[]
            max_count=max(1, int(scoped.groupby(['activity','location']).size().max() or 1))
            for a in top_activities:
                for loc in top_locations:
                    count=int(((scoped['activity']==a)&(scoped['location']==loc)).sum())
                    cells.append({'activity':a,'location':loc,'count':count,'intensity':round(count/max_count,3)})
            _LOCATION_HEATMAP_CACHE={'locations':top_locations,'activities':top_activities,'cells':cells,'total_reports':int(len(raw)),
                'note':'Location is State from the January 2015–November 2025 OSHA dataset. Activity groups are derived from incident event/source descriptions; heat intensity represents report density, not a site-specific SIF probability.'}
        except Exception as exc:
            print(f'[OIL-SIF] Location heatmap could not be built: {exc}')
            _LOCATION_HEATMAP_CACHE={'locations': [], 'activities': [], 'cells': [], 'total_reports': 0, 'note': 'Location heatmap data could not be loaded.'}
    return _LOCATION_HEATMAP_CACHE


# Rich geographic management view built from the supplied January 2015–November 2025 dataset.
# The source contains U.S. State and FederalState fields, but no Country field. Country scope
# is therefore explicitly derived as United States rather than fabricating country-level data.
_GEO_HEATMAP_CACHE = None
_GEO_HEATMAP_LOCK = threading.RLock()
_GEO_CACHE_PATH = APP_CORE / 'geography_cache.json'

def _load_geographic_management_data():
    global _GEO_HEATMAP_CACHE
    if _GEO_HEATMAP_CACHE is not None:
        return _GEO_HEATMAP_CACHE
    with _GEO_HEATMAP_LOCK:
        if _GEO_HEATMAP_CACHE is not None:
            return _GEO_HEATMAP_CACHE
        # Use the compact persistent cache first so the Management dashboard does
        # not have to parse and aggregate the full historical CSV after login.
        if _GEO_CACHE_PATH.exists():
            try:
                _GEO_HEATMAP_CACHE = json.loads(_GEO_CACHE_PATH.read_text(encoding='utf-8'))
                return _GEO_HEATMAP_CACHE
            except Exception as exc:
                print(f'[OIL-SIF] Geographic cache could not be read; rebuilding: {exc}')
        if not _LOCATION_DATA_FILE.exists():
            return {'country': {'name':'United States','total_reports':0,'states':0},
                    'states': [], 'activities': [], 'activity_states': {}, 'years': [], 'note':'Location dataset is not available.'}
        try:
            raw = pd.read_csv(
                _LOCATION_DATA_FILE,
                low_memory=False,
                usecols=['State','Latitude','Longitude','EventDate','EventTitle','SourceTitle','Final Narrative','FederalState']
            )
            raw['state'] = raw['State'].fillna('Unknown').astype(str).str.strip().str.title()
            raw.loc[raw['state'].isin(['','Nan','None']), 'state'] = 'Unknown'
            raw['activity'] = [
                _activity_group_from_incident(e, s, n)
                for e, s, n in zip(raw['EventTitle'], raw['SourceTitle'], raw['Final Narrative'])
            ]
            raw['date'] = pd.to_datetime(raw['EventDate'], errors='coerce')
            raw['year'] = raw['date'].dt.year
            raw['federal'] = pd.to_numeric(raw['FederalState'], errors='coerce').fillna(1).eq(1)

            state_counts = raw.groupby('state').size().sort_values(ascending=False)
            max_count = max(1, int(state_counts.max() if len(state_counts) else 1))
            states = []
            for state, group in raw.groupby('state', sort=False):
                if state == 'Unknown':
                    continue
                lat = pd.to_numeric(group['Latitude'], errors='coerce').mean()
                lon = pd.to_numeric(group['Longitude'], errors='coerce').mean()
                top = group['activity'].value_counts().head(4)
                activities = [{'name':str(k), 'count':int(v)} for k,v in top.items()]
                years = group['year'].dropna().astype(int)
                states.append({
                    'name': state,
                    'count': int(len(group)),
                    'intensity': round(len(group) / max_count, 4),
                    'share': round(len(group) / max(1, len(raw)) * 100, 3),
                    'latitude': None if pd.isna(lat) else round(float(lat), 4),
                    'longitude': None if pd.isna(lon) else round(float(lon), 4),
                    'federal_reports': int(group['federal'].sum()),
                    'state_reports': int((~group['federal']).sum()),
                    'top_activities': activities,
                    'first_year': int(years.min()) if len(years) else None,
                    'last_year': int(years.max()) if len(years) else None,
                })
            states.sort(key=lambda x:x['count'], reverse=True)

            activity_counts = raw['activity'].value_counts()
            activities = [{'name':str(k), 'count':int(v)} for k,v in activity_counts.items()]
            activity_states = {}
            for activity_name, ag in raw.groupby('activity'):
                counts = ag.groupby('state').size().to_dict()
                activity_states[str(activity_name)] = {str(k): int(v) for k,v in counts.items()}

            # Keep the full 2015–2025 timeline compact: one state/activity-aware
            # aggregate per year, used by the animated timeline on the frontend.
            yearly = []
            for year, yg in raw.dropna(subset=['year']).groupby('year'):
                year_states = yg.groupby('state').size().to_dict()
                yearly.append({
                    'year': int(year),
                    'total': int(len(yg)),
                    'states': {str(k): int(v) for k,v in year_states.items()}
                })
            yearly.sort(key=lambda x:x['year'])

            federal_count = int(raw['federal'].sum())
            country = {
                'name': 'United States',
                'total_reports': int(len(raw)),
                'states': int(raw['state'].nunique()),
                'federal_reports': federal_count,
                'state_reports': int(len(raw) - federal_count),
                'start_date': raw['date'].min().strftime('%Y-%m-%d') if raw['date'].notna().any() else None,
                'end_date': raw['date'].max().strftime('%Y-%m-%d') if raw['date'].notna().any() else None,
            }
            _GEO_HEATMAP_CACHE = {
                'country': country,
                'states': states,
                'activities': activities,
                'activity_states': activity_states,
                'years': yearly,
                'note': 'State-level report density from the supplied January 2015–November 2025 dataset. The source does not contain a Country field; all records are treated as United States scope. Intensity represents report volume, not SIF probability.',
                'source': 'January 2015–November 2025 dataset',
            }
            try:
                _GEO_CACHE_PATH.write_text(json.dumps(_GEO_HEATMAP_CACHE, separators=(',', ':')), encoding='utf-8')
            except Exception as exc:
                print(f'[OIL-SIF] Could not persist geographic cache: {exc}')
        except Exception as exc:
            print(f'[OIL-SIF] Geographic management data could not be built: {exc}')
            _GEO_HEATMAP_CACHE = {
                'country': {'name':'United States','total_reports':0,'states':0},
                'states': [], 'activities': [], 'activity_states': {}, 'years': [],
                'note': 'Geographic management data could not be loaded.'
            }
    return _GEO_HEATMAP_CACHE

@app.get('/api/management/geography')
def management_geography(user=Depends(require_role('Management'))):
    return _load_geographic_management_data()

@app.get('/api/management/heatmap')
def management_heatmap(user=Depends(require_role('Management'))):
    return _load_location_heatmap()

@app.get('/api/hse/density')
def hse_density(user=Depends(require_role('HSE Officer'))):
    """Return a compact activity x Life-Saving Rule density matrix for the HSE dashboard.

    The matrix is calculated from the supplied HSE review queue. A row may be associated
    with more than one Life-Saving Rule, so each explicit rule association is counted.
    Density is the share of those associations marked SIF Potential; it is not a model
    probability and should be read as a review-queue concentration signal.
    """
    if queue_df.empty:
        return {'activities': [], 'rules': [], 'cells': [], 'total_associations': 0,
                'note': 'HSE review queue data is not available.'}
    work = queue_df.copy()
    work['activity'] = work.get('activity_group', pd.Series('', index=work.index)).fillna('Unknown activity').astype(str).str.strip()
    work['rules_raw'] = work.get('life_saving_rule', pd.Series('', index=work.index)).fillna('Not mapped').astype(str)
    work['sif'] = work.get('sif_prediction', pd.Series('', index=work.index)).fillna('').astype(str).str.lower().str.contains('sif potential')
    rows=[]
    for _, r in work.iterrows():
        rules=[x.strip() for x in str(r['rules_raw']).split(';') if x.strip()]
        if not rules: rules=['Not mapped']
        for rule in rules:
            rows.append({'activity':r['activity'] or 'Unknown activity','rule':rule,'sif':bool(r['sif'])})
    pairs=pd.DataFrame(rows)
    if pairs.empty:
        return {'activities': [], 'rules': [], 'cells': [], 'total_associations': 0,
                'note': 'No activity / Life-Saving Rule associations were available.'}
    top_activities=pairs['activity'].value_counts().head(8).index.tolist()
    top_rules=pairs['rule'].value_counts().head(8).index.tolist()
    scoped=pairs[pairs.activity.isin(top_activities) & pairs.rule.isin(top_rules)]
    cells=[]
    for activity in top_activities:
        for rule in top_rules:
            cell=scoped[(scoped.activity==activity)&(scoped.rule==rule)]
            total=int(len(cell)); sif=int(cell['sif'].sum()) if total else 0
            cells.append({'activity':activity,'rule':rule,'total':total,'sif':sif,
                          'density':round((sif/total*100) if total else 0,1)})
    return {
        'activities':[{'name':x,'total':int((scoped.activity==x).sum())} for x in top_activities],
        'rules':[{'name':x,'total':int((scoped.rule==x).sum())} for x in top_rules],
        'cells':cells,
        'total_associations':int(len(scoped)),
        'note':'HSE review-queue concentration matrix. SIF density is the share of queue associations marked SIF Potential; it is not a model probability.'
    }

@app.get('/api/intelligence/drilldown')
def intelligence_drilldown(kind:str='activity',value:str='',days:int=3650,user=Depends(require_role('HSE Officer','Management'))):
    rows=[]
    for r in submitted_reports:
        key={'activity':'activity','lsr':'life_saving_rule','barrier':'barrier','precursor':'hazard','site':'site'}.get(kind,'activity')
        if value and str(r.get(key,'' )).lower()!=value.lower(): continue
        rows.append(operational_row(r))
    if kind in {'activity','lsr','barrier','precursor','site'} and value and not rows and user['role']=='HSE Officer':
        mdf = get_master_df()
        col={'activity':'activity_group','lsr':'life_saving_rule','barrier':'critical_barrier','precursor':'precursor','site':'site'}.get(kind,'activity_group')
        if col in mdf.columns:
            m=mdf[mdf[col].astype(str).str.lower().eq(value.lower())]
            rows=compact_records(m.head(200))
    return {'kind':kind,'value':value,'total':len(rows),'sif_count':sum(str(r.get('sif_prediction','')).lower().find('sif')>=0 for r in rows),'rows':rows[:200]}

@app.get('/api/export/reports')
def export_reports(search:str='',status:str='all',review:str='all',activity:str='all',date_from:str='',date_to:str='',site:str='',user=Depends(require_role('HSE Officer','Management'))):
    # Reuse the report explorer logic over both submitted and master data.
    base=[operational_row(r) for r in submitted_reports if not site or r.get('site')==site] + compact_records(get_master_df())
    def yes(r):
        q=search.lower().strip()
        if q and q not in json.dumps(r,ensure_ascii=False).lower(): return False
        pred=str(r.get('sif_prediction','')).lower()
        if status=='sif' and 'sif potential' not in pred:return False
        if status=='non-sif' and 'sif potential' in pred:return False
        rs=str(r.get('hse_review_status','')).lower()
        if review=='pending' and 'pending' not in rs:return False
        if review=='reviewed' and 'pending' in rs:return False
        if activity!='all' and str(r.get('activity_group',r.get('activity',''))) != activity:return False
        if date_from and str(r.get('date_of_incident','')) < date_from:return False
        if date_to and str(r.get('date_of_incident','')) > date_to:return False
        return True
    filtered=[r for r in base if yes(r)]
    df=pd.DataFrame(filtered)
    buf=StringIO(); df.to_csv(buf,index=False)
    return StreamingResponse(iter([buf.getvalue()]),media_type='text/csv',headers={'Content-Disposition':'attachment; filename="oil-sif-reports.csv"'})

def dynamic_overview(site=''):
    out=json.loads(json.dumps(OVERVIEW_CACHE))
    scoped=[r for r in submitted_reports if not site or r.get('site')==site]
    pending_submitted=sum(r.get('review_status')=='Pending HSE review' for r in scoped)
    out['kpis']['awaiting_review']=int(OVERVIEW_CACHE['kpis']['awaiting_review'])+pending_submitted
    out['kpis']['submitted_reports']=len(scoped)
    out['kpis']['site_submitted_reports']=len(scoped)
    out['site_scope']=site or 'All facilities'
    return out

@app.get('/api/data/bootstrap')
def bootstrap(site:str='',user=Depends(current_user)):
    role = user.get('role')
    # Employees receive only field-safe, aggregate information. HSE receives
    # operational review/analytics data. Management receives aggregate data.
    payload = {'overview': None, 'barriers': None, 'activities': None, 'lsr': None, 'precursor': None, 'queue': None}
    if role == 'Employee':
        site_rows=[r for r in submitted_reports if not site or r.get('site')==site]
        payload['overview'] = {
            'kpis': {'total_reports': OVERVIEW_CACHE['kpis']['total_reports'], 'site_submitted_reports': len(site_rows)},
            'precursors': OVERVIEW_CACHE.get('precursors', [])[:5],
            'recent_high_risk': OVERVIEW_CACHE.get('recent_high_risk', [])[:5],
        }
        payload['lsr'] = {'columns': list(lsr_df.columns), 'rows': compact_records(lsr_df.head(8))}
        return payload
    if role == 'Management':
        payload['overview'] = dynamic_overview(site)
        payload['overview']['site_submitted_reports'] = len([r for r in submitted_reports if not site or r.get('site')==site])
        payload['precursor'] = {'columns': list(precursor_df.columns), 'rows': compact_records(precursor_df.head(8))}
        payload['activities'] = {'columns': list(activity_df.columns), 'rows': compact_records(activity_df.head(10))}
        return payload
    payload['overview'] = dynamic_overview(site)
    payload['overview']['site_submitted_reports'] = len([r for r in submitted_reports if not site or r.get('site')==site])
    payload['barriers'] = {'columns': list(barrier_df.columns), 'rows': compact_records(barrier_df)}
    payload['activities'] = {'columns': list(activity_df.columns), 'rows': compact_records(activity_df)}
    payload['lsr'] = {'columns': list(lsr_df.columns), 'rows': compact_records(lsr_df)}
    payload['precursor'] = {'columns': list(precursor_df.columns), 'rows': compact_records(precursor_df)}
    live_queue=[r for r in all_operational_rows() if not site or r.get('site')==site]
    combined_queue = live_queue + compact_records(queue_df.head(100))
    payload['queue'] = {'columns': ['report_id','date_of_incident','activity_group','precursor','life_saving_rule','sif_probability','sif_prediction','confidence_band','hse_review_status','report_text'], 'rows': combined_queue[:200], 'site_scope': site or 'All facilities', 'live_queue_count': len(live_queue)}
    return payload

@app.get('/api/data/overview')
def get_overview(site:str='',user=Depends(require_role('HSE Officer', 'Management'))):
    return dynamic_overview(site)

@app.get('/api/data/barriers')
def get_barriers(user=Depends(require_role('HSE Officer'))):
    return {'columns': list(barrier_df.columns), 'rows': compact_records(barrier_df)}

@app.get('/api/data/activities')
def get_activities(user=Depends(require_role('HSE Officer'))):
    return {'columns': list(activity_df.columns), 'rows': compact_records(activity_df)}

@app.get('/api/data/queue')
def get_queue(limit: int = 100, user=Depends(require_role('HSE Officer'))):
    limit = max(1, min(limit, 200))
    return {'columns': list(queue_df.columns), 'rows': compact_records(queue_df, limit)}

@app.get('/api/data/reports')
def get_reports(search: str = '', status: str = 'all', review: str = 'all', activity: str = 'all', date_from: str = '', date_to: str = '', site: str = '', limit: int = 60, user=Depends(require_role('HSE Officer'))):
    """Filtered report explorer over the master dataset plus live submitted reports."""
    work = get_master_df().copy()
    if work.empty:
        master_rows=[]
    else:
        mask = pd.Series(True, index=work.index)
        q = str(search).strip().lower()
        if q:
            searchable = pd.DataFrame({c: work[c].astype(str) for c in work.columns if c in ['report_id','activity_group','precursor','life_saving_rule','report_text']}).fillna('').agg(' '.join,axis=1).str.lower()
            mask &= searchable.str.contains(q,regex=False,na=False)
        pred=work.get('sif_prediction',pd.Series('',index=work.index)).astype(str).str.lower()
        if status.lower()=='sif': mask &= pred.eq('sif potential')
        elif status.lower()=='non-sif': mask &= ~pred.eq('sif potential')
        rs=work.get('hse_review_status',pd.Series('',index=work.index)).astype(str).str.lower()
        if review.lower()=='pending': mask &= rs.str.contains('pending',na=False)
        elif review.lower()=='reviewed': mask &= ~rs.str.contains('pending',na=False)
        if activity.lower()!='all': mask &= work.get('activity_group',pd.Series('',index=work.index)).astype(str).eq(activity)
        if date_from or date_to:
            dates=pd.to_datetime(work.get('date_of_incident',pd.Series('',index=work.index)),errors='coerce')
            if date_from: mask &= dates >= pd.to_datetime(date_from,errors='coerce')
            if date_to: mask &= dates <= pd.to_datetime(date_to,errors='coerce')
        filtered=work.loc[mask]
        if 'sif_probability' in filtered.columns: filtered=filtered.sort_values('sif_probability',ascending=False,na_position='last')
        view_cols=[c for c in ['report_id','date_of_incident','activity_group','precursor','life_saving_rule','sif_probability','sif_prediction','confidence_band','hse_review_status','report_text'] if c in filtered.columns]
        master_rows=compact_records(filtered[view_cols])
        for row in master_rows:
            saved = hse_reviews.get(str(row.get('report_id')), {})
            if saved:
                row['hse_review_status'] = 'Needs more information' if saved.get('decision') == 'Needs More Information' else 'Reviewed'
                row['hse_decision'] = saved.get('decision')
                row['hse_reason'] = saved.get('reason')
                row['corrective_action'] = saved.get('action')
    submitted=[r for r in all_operational_rows() if not site or r.get('site')==site]
    q=str(search).strip().lower()
    def keep(r):
        text=json.dumps(r,ensure_ascii=False).lower()
        if q and q not in text:return False
        pred=str(r.get('sif_prediction','')).lower()
        if status=='sif' and 'sif potential' not in pred:return False
        if status=='non-sif' and 'sif potential' in pred:return False
        rs=str(r.get('hse_review_status','')).lower()
        if review=='pending' and 'pending' not in rs:return False
        if review=='reviewed' and 'pending' in rs:return False
        if activity!='all' and str(r.get('activity_group',r.get('activity',''))) != activity:return False
        if date_from and str(r.get('date_of_incident','')) < date_from:return False
        if date_to and str(r.get('date_of_incident','')) > date_to:return False
        return True
    submitted=[r for r in submitted if keep(r)]
    combined=submitted+master_rows
    combined.sort(key=lambda r: float(r.get('sif_probability') or 0), reverse=True)
    limit=max(1,min(int(limit),200))
    cols=['report_id','date_of_incident','activity_group','precursor','life_saving_rule','sif_probability','sif_prediction','confidence_band','hse_review_status','report_text']
    return {'columns':cols,'rows':combined[:limit],'total':len(combined)}

@app.get('/api/data/lsr')
def get_lsr(user=Depends(require_role('HSE Officer', 'Employee'))):
    return {'columns': list(lsr_df.columns), 'rows': compact_records(lsr_df)}

@app.get('/api/data/precursor')
def get_precursor(user=Depends(require_role('HSE Officer', 'Management'))):
    return {'columns': list(precursor_df.columns), 'rows': compact_records(precursor_df)}

@app.get('/api/health')
def health():
    return {'ok': True, 'sif_model_loaded': _sif_model is not None, 'lsr_model_loaded': _lsr_model is not None, 'submitted_reports': len(submitted_reports), 'pending_hse_reviews': sum(r.get('review_status')=='Pending HSE review' for r in submitted_reports), 'timestamp': datetime.now(timezone.utc).isoformat()}
