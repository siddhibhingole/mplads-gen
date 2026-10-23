# MPLADS Sentinel

**A Civic-Tech Platform for Monitoring and Understanding Public Development Works**

MPLADS Sentinel is a web application prototype designed to make information about development works funded through the Members of Parliament Local Area Development Scheme (MPLADS) easier to explore and understand.

The project combines a modern web frontend with a Python API backend, providing a foundation for development-work tracking, data exploration, and optional AI-assisted insights.

> **Project status:** Prototype / MVP. Demo data, AI integrations, authentication, and deployment configuration should be verified before real-world use. Demo data must not be presented as official government data.

## Features

- **Development-work exploration:** A foundation for searching and viewing development-work records.
- **Project status tracking:** Designed to present available project and progress information.
- **AI-assisted insights:** Optional AI integration when the required provider and credentials are configured.
- **API-driven architecture:** Separates the frontend interface from backend processing.
- **Extensible data layer:** Can be extended to use verified datasets and a persistent cloud database.
- **Cloud deployment:** Designed for a frontend and backend deployment workflow.

Only features implemented and connected in the current version should be considered operational.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI |
| API communication | HTTP / JSON |
| Local data | SQLite or mock data, depending on configuration |
| AI integration
