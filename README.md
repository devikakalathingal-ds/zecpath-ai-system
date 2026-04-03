# Zecpath AI Project

## Project Overview
This project is an AI-powered hiring system designed to automate the recruitment process. It covers multiple stages including resume parsing, candidate screening, interview processing, and final scoring.

---

## Project Structure

The project follows a modular architecture to ensure scalability, maintainability, and clear separation of responsibilities.

```
project-root/
│
├── data/
├── parsers/
├── ats_engine/
├── screening_ai/
├── interview_ai/
├── scoring/
├── utils/
├── tests/
├── logs/
├── main.py
└── requirements.txt
```

---

## Module Description

### data/
Stores datasets such as resumes, job descriptions, and processed data used in the system.

---

### parsers/
Responsible for data extraction and preprocessing. This includes converting resumes (PDF/DOCX) into structured text format.

---

### ats_engine/
Implements Applicant Tracking System (ATS) functionality:
- Resume filtering
- Keyword matching
- Candidate ranking

---

### screening_ai/
Handles AI-based candidate screening:
- Skill analysis
- Experience evaluation
- Initial filtering

---

### interview_ai/
Manages AI-driven interview processes:
- Question generation
- Response analysis
- Interview flow management

---

### scoring/
Calculates final candidate scores by combining:
- ATS score
- Screening results
- Interview performance

---

### utils/
Contains reusable helper functions such as logging, file handling, and common utilities.

---

### tests/
Includes test scripts for validating different modules and ensuring system reliability.

---

### logs/
Stores system logs for monitoring, debugging, and tracking AI activities.

---

### main.py
Serves as the entry point of the application, integrating all modules and executing the workflow.

---

### requirements.txt
Lists all Python dependencies required to run the project.

---

## Summary

This project is designed using a modular and scalable architecture where each component operates independently while contributing to an integrated AI-based hiring system.