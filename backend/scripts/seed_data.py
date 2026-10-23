import json,random,sys
from datetime import date,timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.repository import Repository
from app.agents import Orchestrator
here=Path(__file__).resolve(); root=next((parent for parent in here.parents if (parent/'data'/'works.json').exists()), here.parents[2]); data=root/'data'
records=json.loads((data/'works.json').read_text()); evidence=json.loads((data/'evidence.json').read_text())
repo=Repository('sqlite:///./mplads_sentinel.db')
repo.conn.execute('DELETE FROM works');repo.conn.execute('DELETE FROM alerts');repo.conn.execute('DELETE FROM evidence');repo.conn.commit()
o=Orchestrator(repo);result=o.ingestion.ingest(repo,'synthetic-seed',records)
for e in evidence:repo.add_evidence(e)
alerts=o.scan_all()
print(f"Seeded {result['accepted']} synthetic works, {len(evidence)} evidence records, {len(alerts)} alerts")
