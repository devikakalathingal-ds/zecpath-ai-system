# AI Data Entity Design Document  
Project: Zecpath – AI Hiring System  
Day 4 – Data Understanding & Structuring  

---

## 1. Objective

The objective of this document is to convert unstructured resume and job description data into structured, AI-ready JSON formats.

Resumes and job descriptions are usually available in PDF, DOC, or text formats. These formats are unstructured and cannot be directly processed by AI systems.

By defining standardized data entities, we enable:

- AI-based resume parsing
- Automated ATS scoring
- Skill matching
- Interview evaluation
- Final hiring decision automation

---

## 2. Resume & Job Description Analysis Findings

After reviewing multiple sample resumes, the following common patterns were identified:

- Personal details are always present (name, email, phone, location).
- Skills are listed as bullet points (technical and soft skills).
- Work experience includes company name, designation, and duration.
- Education includes degree, institution, and graduation year.
- Certifications include issuing authority and year.
- Technical resumes often include project details.

After studying job descriptions, the following patterns were observed:

- Job title and department are clearly mentioned.
- Required experience range is specified (e.g., 2–5 years).
- Mandatory and preferred skills are listed.
- Educational qualifications are mentioned.
- Responsibilities are described in bullet points.
- Salary range may be included.

These observations were used to design standardized JSON schemas for AI-based automation.

---

## 3. Core Data Entities Defined

### 3.1 Resume Entity

The Resume Entity standardizes candidate information into structured fields.

It includes:

- Candidate Profile
- Education Structure
- Experience Patterns
- Skill Object
- Certifications
- Experience Summary

This allows AI models to extract and compare structured attributes easily.

---

### 3.2 Job Description Entity

The Job Description Entity structures hiring requirements into fixed attributes.

It includes:

- Job Profile
- Required Experience
- Required and Preferred Skills
- Education Requirements
- Responsibilities
- Salary Range
- Notice Period Limits

This enables automated candidate-to-job matching.

---

### 3.3 Skill Object

The Skill Object separates skills into categories:

- Technical Skills
- Soft Skills

This improves matching accuracy and reduces ambiguity in skill evaluation.

---

### 3.4 Experience Object

The Experience Object standardizes:

- Designation
- Company
- Duration
- Responsibilities

This helps the AI engine identify experience patterns across candidates.

---

## 4. Design Logic & Technical Decisions

### 4.1 Why JSON Format?

JSON was chosen because:

- It is lightweight and structured.
- It is compatible with AI models and APIs.
- It can be easily stored in databases.
- It is both human-readable and machine-readable.

---

### 4.2 Use of Arrays (Lists)

Arrays are used for:

- Skills
- Responsibilities
- Certifications
- Experience records

This allows AI systems to process multiple data points efficiently.

---

### 4.3 Standardization Approach

Resumes vary in format and writing style. To reduce inconsistency, the following fields were standardized:

- Degree → string
- Institution → string
- Graduation Year → integer
- Experience Duration → number
- Skills → string array

This reduces data noise and improves scoring accuracy.

---

## 5. How This Supports the Zecpath AI System

The structured entities support:

- Phase 2 – ATS Resume Parsing
- AI-based skill matching
- HR and technical round scoring
- Cross-round score aggregation
- Final hiring decision automation

Without structured entities, automation across the Zecpath hiring lifecycle would not be possible.

---

## 6. Conclusion

The defined data entities form the foundation of the Zecpath AI Hiring System.

By converting unstructured resumes and job descriptions into structured JSON entities, the system enables intelligent automation, accurate candidate scoring, and efficient hiring decisions.

This structured design ensures scalability, consistency, and AI-readiness across the entire hiring lifecycle.