from collections import defaultdict,deque
from datetime import datetime,timezone
from pathlib import Path
import json,time
from fastapi import Depends,Header,HTTPException
from .config import settings
class User:
    def __init__(self,uid,role): self.uid,self.role=uid,role
def current_user(authorization: str|None=Header(default=None),x_demo_role: str|None=Header(default=None)):
    if settings.auth_mode=="mock":
        role=x_demo_role or "citizen"
        if role not in {"citizen","officer","admin"}: raise HTTPException(401,"Invalid demo role")
        return User("local-demo",role)
    if not authorization or not authorization.startswith("Bearer "): raise HTTPException(401,"Missing Firebase bearer token")
    try:
        import firebase_admin
        from firebase_admin import auth
        if not firebase_admin._apps: firebase_admin.initialize_app()
        claims=auth.verify_id_token(authorization[7:]); role=claims.get("role","citizen")
        if role not in {"citizen","officer","admin"}: role="citizen"
        return User(str(claims["uid"]),role)
    except Exception as exc: raise HTTPException(401,"Invalid Firebase token") from exc
def require_roles(*roles):
    def dep(user=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403,"Insufficient role")
        return user
    return dep
def audit(event):
    p=Path(settings.audit_log_path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f: f.write(json.dumps({**event,"at":datetime.now(timezone.utc).isoformat()})+"\n")
class RateLimitMiddleware:
    def __init__(self,app,limit): self.app,self.limit,self.events=app,limit,defaultdict(deque)
    async def __call__(self,scope,receive,send):
        if scope["type"]!="http": await self.app(scope,receive,send); return
        ip=(scope.get("client") or ("unknown",0))[0]; now=time.time(); q=self.events[ip]
        while q and now-q[0]>60:q.popleft()
        if len(q)>=self.limit:
            await send({"type":"http.response.start","status":429,"headers":[(b"content-type",b"application/json")]})
            await send({"type":"http.response.body","body":b'{"detail":"Rate limit exceeded"}'}); return
        q.append(now); await self.app(scope,receive,send)
