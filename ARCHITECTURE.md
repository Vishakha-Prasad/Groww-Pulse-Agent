# System Architecture: Groww Review Pulse

This document outlines the high-level architecture of the Groww Review Pulse pipeline.

## System Overview
The pipeline is designed as a **Phase-Wise Modular Architecture**. Each phase is independent, allowing for easy updates (e.g., swapping the scraper or the LLM) without breaking the entire system.

```mermaid
graph TD
    A[Play Store reviews] -->|Phase 1: Ingestion| B(ingestion.py)
    B -->|Raw JSON/CSV| C{Phase 2: Analysis}
    C -->|LLM / Gemini| D(analysis.py)
    D -->|Structured Themes| E[Phase 3: Outputs]
    E -->|reporting.py| F[Weekly_Pulse.md]
    F -->|Phase 4: Email| G(mailing.py)
    G -->|SMTP| H[vishakhaprasad985@gmail.com]
    
    subgraph Configuration
    I[.env File] -.-> D
    I -.-> G
    end
```

## Modular Breakdown

### 📂 Phase 1: Ingestion
- **Source**: `Phase_1_Ingestion/ingestion.py`
- **Responsibility**: Fetches the last 4 weeks of public reviews using `google-play-scraper`.
- **Privacy**: Strips all PII (User IDs, Names) at the source.
- **Persistence**: Saves raw data to `sample_reviews.csv` for audit trails.

### 📂 Phase 2: Analysis (The Brain)
- **Source**: `Phase_2_Analysis/analysis.py`
- **Responsibility**: Processes review text through Google Gemini 1.5 Flash.
- **Logic**: 
    - Groups reviews into max 5 themes.
    - Extracts 3 verbatim user quotes per theme.
    - Generates 3 tactical action items per theme.
- **Fallback**: Contains a high-fidelity mock dataset to ensure the pipeline runs even without an API key.

### 📂 Phase 3: Outputs
- **Source**: `Phase_3_Outputs/reporting.py`
- **Responsibility**: Formats analyzed data into `Weekly_Pulse.md` and `Email_Draft.txt`.

### 📂 Phase 4: Email Automation
- **Source**: `Phase_4_Email/mailing.py`
- **Responsibility**: Automatically dispatches the generated report via SMTP.
- **Recipient**: `vishakhaprasad985@gmail.com`
- **Security**: Requires a Gmail App Password in `.env`.

## Configuration & Security
- **API Management**: API keys are stored in a root `.env` file (not checked into version control).
- **Environment**: Managed via `requirements.txt`.
