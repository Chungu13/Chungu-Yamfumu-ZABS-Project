# ZABS Certification and Verification System

Developed during my internship at Yamfumu Technologies
**My Role:** Backend Developer (Django/Python)
**Project Type:** Internship Project | Team Collaboration

## Overview

The ZABS Certification and Verification System facilitates manufacturers in performing the certification process online and enables consumers to verify product certifications using their mobile devices through a web app or a dedicated mobile app. The system automatically generates QR codes upon certification issuance for easy verification.

## Key Features

- **Manufacturer Portal:**
  - Registration and Authentication: Secure sign-up and login for manufacturers.
  - Certification Application: Apply for product certifications online.
  - Application Tracking: Real-time status tracking of certification applications.
  - Document Management: Upload, store, and manage certification-related documents.
  - Communication: Messaging system for communication between manufacturers and ZABS officials.
  - QR Code Generation: Automatic generation of QR codes upon successful certification issuance.
- **ZABS Admin Portal:**
  - User Management: Manage manufacturers' accounts and roles.
  - Certification Management: Review and process certification applications.
  - Document Review: Access and review submitted documents.
  - Approval and Issuance: Approve certifications and issue digital certificates with QR codes.
  - Reporting and Analytics: Generate reports on certification activities and statistics.
- **Consumer Verification Portal:**
  - QR Code Scanning: Mobile app and web app for consumers to scan QR codes.
  - Product Verification: Display certification details and product information upon scanning.
  - Search Functionality: Allow consumers to search for products and verify their certifications manually.
  - Feedback and Reporting: Consumers can report issues or provide feedback on product certifications.

## Installation

Follow the steps below to set up the project on your local machine.

### 1. Pull the Code

Clone the repository to your local path:

```sh
git clone https://github.com/Chungu13/Chungu-Yamfumu-ZABS-Project.git
cd Chungu-Yamfumu-ZABS-Project

## 2. Activate Virtual Environment
Create and activate a virtual environment:

python -m venv venv
source venv\Scripts\activate

## 3. Start Docker
Make sure Docker Desktop is installed and running. After the Docker engine is running, proceed with the following steps.


## 4. Run Docker Compose
Navigate to your project directory and open a terminal. Run:


docker-compose up --build

## 5. Run Migrations
After the Docker containers are up and running, apply the migrations:


docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate

##6. Create a Superuser (Optional)
If you need admin access, create a superuser: 


docker-compose exec web python manage.py createsuperuser  


## 7. Access the Application
Admin Portal: http://localhost:8000/admin

Manufacturer Portal: http://localhost:8000

Consumer Verification Portal: http://localhost:8000/verify


### Tech Stack
## Backend:
Python Django: Core framework for backend development.
PostgreSQL: Database management system for storing application data.
GraphQL: API framework for efficient data querying and manipulation.
Docker: Containerization for consistent deployment environments.

## Frontend:
React.js (Next.js): Frontend framework for building responsive web applications.
Dart (Flutter): Framework for developing cross-platform mobile applications.



