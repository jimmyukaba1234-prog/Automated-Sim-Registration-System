Automated SIM Registration System
Overview

The Automated SIM Registration System is a web-based application designed to streamline and automate SIM card registration for telecommunications organizations. The system replaces slow, error-prone manual registration processes with an efficient, data-driven workflow that supports both single and bulk customer registrations.

By integrating a data cleaning ETL pipeline, cloud-based data storage, and automated validation logic, the application ensures that customer records are accurate, standardized, and ready for immediate registration.


Key Features

* Automatic SIM Registration

* Validates customer data instantly against a clean dataset

* Manual Registration

* Web form for registering individual customers

* Bulk Registration

* Upload CSV files containing multiple customer records

* ETL Data Pipeline

* Cleans, standardizes, and validates raw customer data

* Cloud-Connected Data Source

* Uses a cloud-hosted CSV (Google Drive) as a lightweight database

Performance Comparison

Compares automated vs manual registration time using visual charts

Data Consistency & Validation

Ensures correct formats for names, phone numbers, ID numbers, and dates


System Architecture
High-Level Flow

- Fake customer data is generated to simulate real-world registrations

- An ETL pipeline cleans and standardizes the dataset

- Clean data is stored in a cloud-hosted CSV file

- The web application connects to the cloud dataset via a backend service

Users can:

- Register customers manually

- Upload bulk registration files

- The system validates data automatically and completes registration

- Performance metrics are calculated and visualized



Technical Overview
Data Engineering (ETL)

Extract

Reads raw CSV files containing customer data

Transform

Standardizes column names

Cleans phone numbers, ID numbers, and dates

Handles missing and invalid values

Load

Outputs a clean dataset used by the web application

Backend

- Fetches clean data from a cloud-hosted CSV link

- Validates new customer records against standardized rules

- Handles bulk file uploads and manual submissions

Frontend

- User-friendly interface for:

- Single customer registration

- Bulk registration

- Displays charts comparing:

- Manual registration time

- Automated registration time

Data Simulation
To mimic real-world telecom data:

Synthetic customer data was generated including:

Name, Address, Phone number, ID number, Registration date

This data was processed through the ETL pipeline to test system reliability and accuracy


Impact & Benefits

Reduces SIM registration time significantly

Minimizes human errors in customer data

Enables high-volume registrations without increasing manpower

Demonstrates real-world use of ETL pipelines + web automation
