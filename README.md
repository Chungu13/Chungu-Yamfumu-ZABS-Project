# ZABS Certification and Verification System

> A full-stack certification management platform built for the Zambia Bureau of Standards (ZABS). Manufacturers apply for product certifications online, ZABS officials review and approve applications, and consumers verify certified products by scanning a QR code.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?logo=django)](https://www.djangoproject.com/)
[![GraphQL](https://img.shields.io/badge/GraphQL-API-E10098?logo=graphql)](https://graphql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![React](https://img.shields.io/badge/React-Next.js-61DAFB?logo=react)](https://react.dev/)
[![Flutter](https://img.shields.io/badge/Flutter-Mobile-02569B?logo=flutter)](https://flutter.dev/)

---

## 🎥 Demo

[(https://www.loom.com/share/2fa204abf864485cb815e60f5c6f4e89)]

> Covers the full certification flow — ZABS admin issues a certification, QR code is automatically generated, consumer scans the QR code and retrieves full product and certification details.

---

## 🔗 Live Demo

| Portal | URL |
|---|---|
| Admin Portal | https://chungu-yamfumu-zabs-project.onrender.com/myadmin/login/?next=/myadmin/ |
| GraphQL API | https://chungu-yamfumu-zabs-project.onrender.com/graphql/ |

**Admin credentials (read-only demo access)**
- Username: `admin`
- Password: `admin@1234`

---

## Problem & Solution

Product certification in Zambia has traditionally been a manual, paper-based process. Manufacturers had no way to apply online, ZABS officials had no central system to manage applications, and consumers had no reliable way to verify whether a product was genuinely certified.

The ZABS Certification and Verification System solves this end to end. Manufacturers apply online, ZABS officials review and approve applications through an admin portal, and upon approval the system automatically generates a QR code. Consumers can then scan the QR code on any mobile device to instantly verify a product's certification status.

---

## My Role

**Backend Developer (Django/Python) — Internship at Yamfumu Technologies, 2024**

I was responsible for the entire backend of the system. This included designing the database schema, building the GraphQL API, implementing authentication and role-based access control, automating QR code generation on certification issuance, and setting up the email notification system. The frontend (React/Next.js and Flutter) was developed by a separate team.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| API | GraphQL (Graphene-Django) |
| Database | PostgreSQL |
| Authentication | Django Auth, JWT, Role-Based Access Control |
| QR Code Generation | Automated on certification issuance |
| Email Notifications | Django Email with HTML templates |
| Containerization | Docker, docker-compose |
| Frontend | React.js (Next.js) *(separate team)* |
| Mobile | Dart (Flutter) *(separate team)* |

---

## Key Engineering Decisions

- **GraphQL API** — Used Graphene-Django to expose a single flexible API endpoint. Mutations handle all create/update/delete operations while queries power the consumer verification flow when a QR code is scanned.

- **Automated QR code generation** — QR codes are generated server-side automatically when a certification is issued. Each QR code is tied to a unique certification ID, ensuring the verification query always returns accurate product and certification details.

- **Role-based access control** — Three distinct user types: `manufacturer`, `admin`, and `consumer`. Each role has access only to the operations relevant to their function. For example only consumers can trigger verifications, and only admins can issue certifications.

- **Email notification pipeline** — Status changes on certification applications automatically trigger HTML email notifications to the manufacturer. Each status (`submitted`, `reviewing`, `approved`, `rejected`) maps to a dedicated email template.

- **Docker-first setup** — Full backend containerised via docker-compose for consistent local development and deployment environments.

---

## Features

### 🏭 Manufacturer Portal
- Register and authenticate securely
- Submit certification applications online
- Track real-time status of applications (`Submitted → Reviewing → Approved/Rejected`)
- Upload and manage certification-related documents
- Receive email notifications on every status change
- Message ZABS officials directly through the platform

### 🏛️ ZABS Admin Portal
- Manage manufacturer accounts and roles
- Review and process certification applications
- Access and review submitted documents
- Issue digital certificates with automatically generated QR codes
- Generate reports on certification activities and statistics

### 📱 Consumer Verification Portal
- Scan QR codes via mobile app or web app
- Instantly retrieve product and certification details
- Search for products and verify certifications manually
- Submit feedback or report issues on product certifications

---

## Architecture

```
.
├── apps/
│   ├── certifications/     # Certification applications, product details, documents
│   ├── users/              # Custom user model, user profiles
│   ├── communication/      # Messaging between manufacturers and ZABS
│   └── verifications/      # Consumer verification and feedback
├── utils/
│   └── send_email.py       # Email notification utility
├── schema.py               # GraphQL schema (queries + mutations)
├── docker-compose.yml      # Full stack orchestration
└── manage.py
```

---

## Local Setup

### Prerequisites
- Docker Desktop

### 1. Clone the Repository
```bash
git clone https://github.com/Chungu13/Chungu-Yamfumu-ZABS-Project.git
cd Chungu-Yamfumu-ZABS-Project
```

### 2. Start Docker
```bash
docker-compose up --build
```

### 3. Run Migrations
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 4. Create a Superuser (Optional)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application

| Portal | URL |
|---|---|
| Admin Portal | http://localhost:8000/myadmin/ |
| GraphQL API | http://localhost:8000/graphql/ |

---

## About

Built during my internship at Yamfumu Technologies to digitise the product certification process for the Zambia Bureau of Standards. The project gave me hands-on experience designing GraphQL APIs, implementing role-based access control, automating background processes like QR code generation and email notifications, and containerising a Django application with Docker.
