# Hiretica

Hiretica is an AI-powered Candidate Intelligence and Ranking Platform designed for the Data & AI Challenge Hackathon. It evaluates and ranks candidates using a pragmatic, production-ready ML architecture under strict performance and compute limits.

## Project Structure
- `backend/`: Python backend containing the FastAPI server and ML ranking pipeline.
- `frontend/`: Next.js web application for interactive candidate evaluation.
- `dataset/`: Storage for the `candidates.jsonl` and precomputed embeddings/indexes.
- `docs/`: Extensive documentation including Dataset, JD, and Behavioral Signal analysis.
- `scripts/`: Offline data ingestion, embedding generation, and FAISS indexing scripts.
- `models/`: Local storage for downloaded ONNX models and checkpoints.
- `tests/`: Automated unit and integration tests.
- `artifacts/`: Project artifacts and intermediate files.

## Getting Started

### Local Development (Backend)
1. Navigate to `backend/`
2. Run `python -m venv venv` and activate it.
3. Install dependencies: `pip install -r requirements.txt` (or rely on `pip install fastapi pydantic polars duckdb sentence-transformers faiss-cpu onnxruntime numpy scikit-learn`)
4. Run the API: `uvicorn main:app --reload`

### Local Development (Frontend)
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

### Docker (Production / Sandbox Simulation)
Run `make run` to build and spin up the complete environment via Docker Compose.
