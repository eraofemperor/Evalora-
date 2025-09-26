# Evalora-
to solve all the evaluation problems related to exams 
Evalora – Handwritten Answer Script Digitization & Evaluation System

Evalora is a smart evaluation platform designed to help educators efficiently digitize, evaluate, and manage student answer scripts. It leverages OCR (Optical Character Recognition) and machine learning to convert handwritten scripts into digital documents, simplifying grading and record-keeping.

Table of Contents

Features

Technology Stack

Architecture

Modules

Installation

Usage

Future Enhancements

Features

Handwriting Recognition: Convert scanned answer sheets into editable digital text using ML models.

Evaluation Management: Teachers can input marks, add comments, and save evaluations.

Digital Report Generation: Export converted scripts and evaluations to Word or PDF formats.

Student Records: Maintain organized records of student submissions and evaluations.

Admin Dashboard: Track all submitted answer sheets, evaluations, and reports in one place.

Technology Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript (optionally Tailwind CSS)

Database: SQLite / PostgreSQL

Machine Learning: CRNN for handwriting recognition, DBNet for text detection

File Management: Word/PDF export functionality using Python libraries

Architecture

The system is built using a modular approach:

User Interface: Students upload handwritten answer scripts.

OCR & ML Module: Detects text and converts handwriting into editable digital format.

Evaluation Module: Teachers assign marks and provide feedback.

Export Module: Generate final evaluated documents in Word or PDF.

Database: Stores student data, scripts, and evaluation records securely.
