import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .config import settings
class Repository:
    def __init__(self, path: str | None = None):
        raw = path or settings.database_url
        if raw.startswith("sqlite:///"): raw = raw[10:]
        self.path = raw
        if raw != ":memory:": Path(raw).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(raw, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript('''
        CREATE TABLE IF NOT EXISTS works(work_id TEXT PRIMARY KEY,payload TEXT NOT NULL,raw_hash TEXT NOT NULL,created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS evidence(evidence_id TEXT PRIMARY KEY,work_id TEXT NOT NULL,title TEXT NOT NULL,snippet TEXT NOT NULL,source_url TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS alerts(alert_id TEXT PRIMARY KEY,work_id TEXT NOT NULL,score INTEGER NOT NULL,severity TEXT NOT NULL,rules TEXT NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS review_tasks(task_id TEXT PRIMARY KEY,alert_id TEXT NOT NULL,role TEXT NOT NULL,decision TEXT NOT NULL,note TEXT NOT NULL,created_at TEXT NOT NULL);
        ''')
        self.conn.commit()
    def upsert_work(self, work: dict[str,Any], raw_hash: str):
        self.conn.execute("INSERT OR REPLACE INTO works VALUES(?,?,?,?)",(work["work_id"],json.dumps(work,default=str),raw_hash,datetime.now(timezone.utc).isoformat())); self.conn.commit()
    def get_work(self, work_id: str):
        row=self.conn.execute("SELECT payload,raw_hash FROM works WHERE work_id=?",(work_id,)).fetchone()
        if not row: return None
        item=json.loads(row["payload"]); item["raw_sha256"]=row["raw_hash"]; return item
    def list_works(self, limit=100, offset=0):
        rows=self.conn.execute("SELECT payload,raw_hash FROM works ORDER BY work_id LIMIT ? OFFSET ?",(limit,offset)).fetchall()
        out=[]
        for row in rows:
            item=json.loads(row["payload"]); item["raw_sha256"]=row["raw_hash"]; out.append(item)
        return out
    def count_works(self): return self.conn.execute("SELECT COUNT(*) FROM works").fetchone()[0]
    def add_evidence(self,e):
        self.conn.execute("INSERT OR REPLACE INTO evidence VALUES(?,?,?,?,?)",(e["evidence_id"],e["work_id"],e["title"],e["snippet"],e["source_url"])); self.conn.commit()
    def evidence_for(self,work_id):
        return [dict(r) for r in self.conn.execute("SELECT * FROM evidence WHERE work_id=? ORDER BY evidence_id",(work_id,)).fetchall()]
    def create_alert(self,a):
        self.conn.execute("INSERT OR REPLACE INTO alerts VALUES(?,?,?,?,?,?,?)",(a["alert_id"],a["work_id"],a["score"],a["severity"],json.dumps(a["rules"]),a.get("status","open"),a["created_at"])); self.conn.commit()
    def get_alert(self,alert_id):
        r=self.conn.execute("SELECT * FROM alerts WHERE alert_id=?",(alert_id,)).fetchone()
        if not r:return None
        x=dict(r); x["rules"]=json.loads(x["rules"]); return x
    def list_alerts(self,status=None,limit=100):
        sql="SELECT * FROM alerts WHERE status=? ORDER BY created_at DESC LIMIT ?" if status else "SELECT * FROM alerts ORDER BY created_at DESC LIMIT ?"
        rows=self.conn.execute(sql,(status,limit) if status else (limit,)).fetchall()
        out=[]
        for r in rows:
            x=dict(r); x["rules"]=json.loads(x["rules"]); out.append(x)
        return out
    def create_task(self,t):
        self.conn.execute("INSERT INTO review_tasks VALUES(?,?,?,?,?,?)",(t["task_id"],t["alert_id"],t["role"],t["decision"],t["note"],t["created_at"])); self.conn.commit()
    def summary(self):
        return {"works":self.count_works(),"open_alerts":self.conn.execute("SELECT COUNT(*) FROM alerts WHERE status='open'").fetchone()[0],"review_tasks":self.conn.execute("SELECT COUNT(*) FROM review_tasks").fetchone()[0],"by_severity":{r["severity"]:r["n"] for r in self.conn.execute("SELECT severity,COUNT(*) n FROM alerts GROUP BY severity").fetchall()}}
