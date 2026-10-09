TermsGuard is a privacy-first legal analysis tool engineered to demystify complex Terms of Service agreements and consumer contracts without compromising user data. Built on a microservice architecture using FastAPI for document parsing and Streamlit for a responsive user interface, the application leverages locally hosted Large Language Models via Ollama (llama3.2) to evaluate contract text entirely on-device. By dynamically extracting content from raw text inputs and PDF uploads with pdfplumber, TermsGuard scans documents for high-risk clauses—such as aggressive automatic renewals, data monetization, binding arbitration waivers, and unilateral modifications—delivering plain-English summaries, exact verbatim excerpts, and categorized risk assessments in seconds.

Key Features:
On-Device Privacy: Operates entirely local via Ollama (llama3.2), ensuring zero external API calls or third-party data sharing.

Multi-Format Ingestion: Supports direct text entry as well as native PDF parsing powered by pdfplumber.

Automated Risk Screening: Pinpoints common fine-print traps including auto-renewals, data broker sharing, class-action waivers, and sudden policy shifts.

Categorized Output: Summarizes complex legal jargon into clear, high/medium/low risk flags paired with direct text citations.

Tech Stack:
Backend Framework: FastAPI

Frontend UI: Streamlit

Local Inference Engine: Ollama (llama3.2)

Document Processing: pdfplumber & python-multipart
