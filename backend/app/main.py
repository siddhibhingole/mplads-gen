import csv,io,json
from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Query
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .repository import Repository
from .agents import Orchestrator
from .models import IngestRequest,ReviewRequest
from .security import current_user,require_roles,audit,RateLimitMiddleware
app=FastAPI(title="MPLADS Sentinel API",version="0.1.0")
app.add_middleware(RateLimitMiddleware,limit=settings.rate_limit_per_minute)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_credentials=True,allow_methods=["GET","POST","OPTIONS"],allow_headers=["Authorization","Content-Type","X-Demo-Role"])
repo=Repository(); orchestrator=Orchestrator(repo)
@app.get("/healthz")
def healthz():return {"status":"ok","environment":settings.app_env,"auth_mode":settings.auth_mode}
@app.post("/api/v1/ingest")
def ingest(body:IngestRequest,user=Depends(require_roles("admin"))):
    r=orchestrator.ingestion.ingest(repo,body.source,body.records); created=orchestrator.scan_all()
    audit({"action":"ingest","actor":user.uid,"accepted":r["accepted"],"rejected":len(r["rejected"])})
    return {**r,"alerts_created":len(created)}
@app.post("/api/v1/ingest/file")
async def ingest_file(file:UploadFile=File(...),user=Depends(require_roles("admin"))):
    if not file.filename or not file.filename.lower().endswith((".csv",".json")):raise HTTPException(400,"Only CSV and JSON supported")
    data=await file.read(settings.max_upload_bytes+1)
    if len(data)>settings.max_upload_bytes:raise HTTPException(413,"File too large")
    try:
        records=json.loads(data) if file.filename.lower().endswith(".json") else list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
        if isinstance(records,dict):records=records.get("records",[])
        if not records or len(records)>settings.max_ingest_rows:raise ValueError("row count")
    except Exception as exc:raise HTTPException(400,"Invalid file content or row count") from exc
    r=orchestrator.ingestion.ingest(repo,file.filename,records);created=orchestrator.scan_all()
    audit({"action":"file_ingest","actor":user.uid,"accepted":r["accepted"]});return {**r,"alerts_created":len(created)}
@app.get("/api/v1/works")
def works(limit:int=Query(100,ge=1,le=500),offset:int=Query(0,ge=0),user=Depends(current_user)):return {"items":repo.list_works(limit,offset),"total":repo.count_works()}
@app.get("/api/v1/works/{work_id}")
def work_detail(work_id:str,user=Depends(current_user)):
    w=repo.get_work(work_id)
    if not w:raise HTTPException(404,"Work not found")
    return w
@app.get("/api/v1/alerts")
def alerts(status:str|None=None,limit:int=Query(100,ge=1,le=500),user=Depends(current_user)):return {"items":repo.list_alerts(status,limit)}
@app.get("/api/v1/alerts/{alert_id}")
def alert_detail(alert_id:str,user=Depends(current_user)):
    a=repo.get_alert(alert_id)
    if not a:raise HTTPException(404,"Alert not found")
    return a
@app.post("/api/v1/alerts/{alert_id}/explain")
def explain(alert_id:str,audience:str="officer",user=Depends(current_user)):
    if audience not in {"citizen","officer","admin"}:raise HTTPException(422,"Invalid audience")
    a=repo.get_alert(alert_id)
    if not a:raise HTTPException(404,"Alert not found")
    try:r=orchestrator.explain(a,audience)
    except ValueError as exc:raise HTTPException(422,str(exc)) from exc
    audit({"action":"explain","actor":user.uid,"alert_id":alert_id});return r
@app.post("/api/v1/alerts/{alert_id}/review")
def review(alert_id:str,body:ReviewRequest,user=Depends(require_roles("officer","admin"))):
    if not repo.get_alert(alert_id):raise HTTPException(404,"Alert not found")
    task=orchestrator.action.create_review_task(repo,alert_id,user.role,body.decision,body.note)
    audit({"action":"review","actor":user.uid,"alert_id":alert_id,"decision":body.decision});return {"task":task,"message":"Review decision recorded"}
@app.get("/api/v1/analytics/summary")
def analytics(user=Depends(current_user)):return repo.summary()
