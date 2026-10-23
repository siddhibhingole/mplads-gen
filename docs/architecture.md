# Architecture
React/TypeScript/Vite/Tailwind → FastAPI auth/RBAC/rate limit → Orchestrator → IngestionAgent, ValidationAgent, ContextAgent, deterministic RiskAgent, EvidenceAgent, ExplainerAgent (mock or Vertex Gemini), GuardrailAgent, ActionAgent.
Local repository is SQLite; BigQuery is an adapter boundary. Cloud Run hosts API, Firebase Hosting hosts frontend, Firebase Auth verifies identity, Secret Manager stores secrets. Browser never calls Vertex AI.
Trust boundaries: only server-side evidence IDs can be cited; external content is untrusted; LLM receives minimal structured context and cannot set scores. Production requires a managed rate limit, durable append-only audit sink, least-privilege IAM, and formal privacy/security review.
