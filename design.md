# Design Document: Lead Management Application

## Overview

This document summarizes the design choices for a FastAPI-based lead management application using SQLite, supporting public lead submissions and internal lead management with email notifications.

## Functional Requirements

- **Public**: Prospects submit leads (`first_name`, `last_name`, `email`, `resume`). Emails sent to prospect and attorney.
- **Internal**: Authenticated attorneys view leads, update state (`PENDING` to `REACHED_OUT`).
- **Tech**: Use FastAPI, SQLite, implement APIs (no UI).

## Architecture

- **Public API**: `POST /leads` for submissions.
- **Internal API**: `GET /leads`, `PATCH /leads/{id}` (w/ auth).
- **Storage**: SQLite (`leads` table), resumes in `uploads/`.
- **Emails**: Simulated via console.

## Design Choices

1. **FastAPI**:

   - **Why**: Required, fast, type-safe with Pydantic, auto-generates OpenAPI docs.
   - **How**: Defined endpoints in `main.py`, used `Form`/`File` for uploads.
   - **Trade-off**: Async complexity minimal for this scope.

2. **SQLite**:

   - **Why**: Required, serverless, simple for low traffic.
   - **How**: Single `leads` table via SQLAlchemy ORM, auto-created.
   - **Trade-off**: Limited scalability, sufficient for scope.

3. **Single Table**:

   - **Why**: Minimal model (`id`, `first_name`, `last_name`, `email`, `resume_path`, `state`).
   - **How**: SQLAlchemy model in `models.py`, CRUD in `crud.py`.
   - **Trade-off**: Simple but less extensible.

4. **Local File Storage**:

   - **Why**: Easy for resumes, avoids database bloat.
   - **How**: `uploads/` with UUID filenames.
   - **Trade-off**: Not scalable, fine for development.

5. **Simulated Emails**:

   - **Why**: Meets requirement without external service.
   - **How**: Console output in `emails.py`.
   - **Trade-off**: Not production-ready, easy to swap.

6. **Basic Auth**:

   - **Why**: Simple protection for internal endpoints.
   - **How**: Hardcoded `admin:password` in `main.py`.
   - **Trade-off**: Insecure for production, fits exercise.

7. **Pydantic**:

   - **Why**: Validates inputs, serializes responses.
   - **How**: Schemas in `schemas.py` with `LeadState` enum.
   - **Trade-off**: Minor overhead, ensures correctness.

8. **SQLAlchemy ORM**:

   - **Why**: Simplifies database operations.
   - **How**: Session injection via `Depends(get_db)`.
   - **Trade-off**: Slight overhead vs. raw SQL.


## Assumptions

- Single attorney (hardcoded email).
- Local development, no production needs.
- Basic validation (e.g., email format).
- Two states (`PENDING`, `REACHED_OUT`).

## Future Improvements

- Real email service (e.g., Mailgun).
- Secure auth (JWT, user database).
- Cloud storage for resumes (e.g., S3).
- Migrations with Alembic.
- Enhanced validation.
