import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app); h={'X-Demo-Role':'admin'}
assert c.get('/healthz').status_code==200
p={'source':'smoke','records':[{'work_id':'SMOKE-001','district':'Pune','category':'Road','sanction_date':'2025-01-01','status':'in_progress','amount_sanctioned':100000,'amount_paid':0,'last_progress_date':'2025-01-01'}]}
assert c.post('/api/v1/ingest',json=p,headers=h).status_code==200
a=next(x for x in c.get('/api/v1/alerts').json()['items'] if x['work_id']=='SMOKE-001')
e=c.post(f"/api/v1/alerts/{a['alert_id']}/explain?audience=officer").json()
assert all('[EVIDENCE:' in claim for claim in [e['summary'],*e['claims']])
assert c.get('/api/v1/works/SMOKE-001').status_code==200
print('SMOKE PASS: ingest -> risk scan -> alert -> cited explanation -> API fetch')
