# Food Waste Management System

A Django web application that connects food donors with NGOs, with volunteers handling pickup and delivery. Built as an academic project.

## Features

**Donors**
- Sign up, log in, and post food donations
- View donation history and claims on their donations
- Make payments linked to claims
- Raise and track complaints

**NGOs**
- Sign up, log in, and use a dashboard
- Browse available donations and claim them
- View claimed donations and notices

**Volunteers**
- Log in and use a dashboard
- Mark donations as picked up and delivered

**General**
- About and contact pages
- Django admin panel

## Tech Stack
- Python, Django
- MySQL
- HTML/CSS templates
- django-widget-tweaks, python-dotenv, Pillow

## Data Model
NGOExtra, DonarExtra, Volunteer (user profiles), Donation (with status), Claim, Payment, Notice, Complaint.

## Setup
1. Clone the repository and open the project folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a MySQL database named `food_donation_db`.
4. Copy `.env.example` to `.env` and fill in your own values.
5. Run `python manage.py migrate`
6. Run `python manage.py runserver` and open http://127.0.0.1:8000/

## Configuration
Secrets are read from environment variables (see `.env.example`) and are never committed to the repository.
