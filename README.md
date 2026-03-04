# Clara Answers – Zero-Cost Automation Pipeline

## Overview

This project implements a zero-cost automation pipeline that converts client conversations (demo calls and onboarding calls) into structured, version-controlled Retell agent configurations.

It simulates Clara’s real-world onboarding workflow:

Human Conversation  
→ Structured Operational Rules  
→ AI Agent Configuration  
→ Versioned Artifacts  

The system processes:

- 5 Demo Call Transcripts → Generates v1 Agent
- 5 Onboarding Transcripts → Updates to v2 Agent
- Structured Account Memo JSON
- Retell Agent Draft Spec
- Detailed Version Changelog

The entire solution runs locally with **zero paid APIs** and is fully reproducible.



# Architecture

## Pipeline A – Demo → v1

Demo Transcript  
↓  
Extractor (Rule-Based)  
↓  
Account Memo JSON (v1)  
↓  
Retell Agent Draft Spec (v1)  
↓  
Stored under `/outputs/accounts/<account_id>/v1`



## Pipeline B – Onboarding → v2

Onboarding Transcript  
↓  
Update Extraction  
↓  
Patch Engine  
↓  
Account Memo JSON (v2)  
↓  
Retell Agent Draft Spec (v2)  
↓  
Detailed Changelog  

# How to Run

## 1. Add Transcripts

Place demo transcripts in:


dataset/demo/


Place onboarding transcripts in:


dataset/onboarding/


Files must be `.txt`.

The filename (without extension) becomes the `account_id`.

Example:


dataset/demo/client1.txt


→ account_id = `client1`



## 2. Run Full Pipeline


python scripts/run_pipeline.py


This will:

- Generate v1 memos
- Generate v1 agent specs
- Apply onboarding updates
- Generate v2 memos
- Generate v2 agent specs
- Create detailed changelogs

The system is idempotent — running it multiple times does not create duplicate structures.



# Account Memo Schema

Each account generates a structured JSON including:

- account_id
- company_name
- business_hours
- office_address
- services_supported
- emergency_definition
- emergency_routing_rules
- non_emergency_routing_rules
- call_transfer_rules
- integration_constraints
- after_hours_flow_summary
- office_hours_flow_summary
- questions_or_unknowns
- notes

If information is missing in transcripts, it is:

- Left blank, OR
- Explicitly listed under `questions_or_unknowns`

No hallucinated data is introduced.



# Retell Agent Draft Spec

Each version (v1 and v2) generates:

- agent_name
- voice_style
- system_prompt
- key_variables
- call_transfer_protocol
- fallback_protocol
- version

The generated system prompt includes:

## Business Hours Flow
- Greeting
- Ask purpose
- Collect name and number
- Transfer or route
- Fallback if transfer fails
- Confirm next steps
- Ask if anything else
- Close call

## After Hours Flow
- Greeting
- Confirm emergency
- If emergency:
  - Immediately collect name, number, address
  - Attempt transfer
  - Fallback handling if transfer fails
- If non-emergency:
  - Collect details
  - Confirm follow-up during business hours
- Close call

The agent never mentions internal tools or function calls.



# Versioning Strategy

The system maintains:

- v1 → Based only on demo transcript
- v2 → Updated using onboarding transcript

The v2 generation:

- Preserves unrelated fields
- Updates only confirmed changes
- Avoids silent overwrites
- Produces a detailed changelog

Example changelog format:


### business_hours
- Old: {...}
- New: {...}
- Reason: Confirmed during onboarding call


This ensures operational transparency and auditability

# Design Decisions

## Rule-Based Extraction

Chosen because:

- Zero-cost requirement
- Fully offline
- Deterministic behavior
- No hallucination risk
- Reproducible by reviewers

## JSON-Based Storage

Benefits:

- Clean versioning
- Easy diff comparison
- Future database migration ready
- Clear schema control

## Version Separation (v1 vs v2)

Demo conversations are exploratory and incomplete.  
Onboarding confirms operational details.

Separating versions prevents corruption of assumptions and ensures safe updates.



# Idempotency

The pipeline:

- Can be run multiple times safely
- Rewrites versioned outputs cleanly
- Does not duplicate accounts
- Maintains consistent folder structure



# Limitations

- Rule-based extraction (limited NLP flexibility)
- Basic keyword detection
- No speech-to-text included (expects transcripts)
- Retell API not directly integrated (spec JSON generated instead)



# Production Improvements

If extended for production:

- Integrate local LLM for structured extraction
- Add schema validation layer
- Use Supabase/Postgres for storage
- Implement full Retell API automation
- Add UI diff viewer
- Add timezone normalization
- Add error logging + retry handling



# What This Demonstrates

- Systems thinking
- Schema design for operational logic
- Handling ambiguity safely
- Version-controlled AI configuration
- Automation design under zero-cost constraint
- Clean separation of exploratory vs confirmed data

## n8n Orchestration

The pipeline can also be triggered using n8n.

Workflow:

Manual Trigger
↓
HTTP Request
↓
Flask Server (/run-pipeline)
↓
run_pipeline.py

The workflow export is available at:

workflows/n8n_pipeline.json

# Summary

This project simulates Clara’s onboarding automation layer:

Messy real-world conversations  
→ Structured operational configuration  
→ Versioned AI voice agent  
→ Reproducible artifacts  

It is designed as a small internal product rather than a one-off script.

for run:
1.  python scripts/run_pipeline.py
2.  python scripts/pipeline_server.py


Author: Priyanshu Gautam
