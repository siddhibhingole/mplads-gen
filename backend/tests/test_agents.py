from datetime import date,timedelta
import pytest
from app.agents import ContextAgent,RiskAgent,GuardrailAgent,MockGeminiClient
def test_no_payment_rule():
 w={"work_id":"T-1","status":"in_progress","sanction_date":(date.today()-timedelta(days=120)).isoformat(),"last_progress_date":date.today().isoformat(),"amount_sanctioned":100000,"amount_paid":0}
 a=RiskAgent().scan(w,ContextAgent().build(w),[])
 assert "NO_PAYMENT_90D" in [x["id"] for x in a["rules"]]
def test_cited_mock_explanation():
 p={"alert":{"alert_id":"ALT-1","score":20,"rules":[{"message":"No payment recorded"}]},"work":{"work_id":"T-1"},"evidence":[{"evidence_id":"EV-1"}],"audience":"officer"}
 x=GuardrailAgent().check(MockGeminiClient().explain(p),p["evidence"])
 assert all("[EVIDENCE:EV-1]" in c for c in [x["summary"],*x["claims"]])
def test_accusatory_language_blocked():
 x={"alert_id":"ALT-1","audience":"officer","summary":"Fraud occurred [EVIDENCE:EV-1]","claims":["Fraud occurred [EVIDENCE:EV-1]"],"evidence_ids":["EV-1"],"limitations":[]}
 with pytest.raises(ValueError):GuardrailAgent().check(x,[{"evidence_id":"EV-1"}])
