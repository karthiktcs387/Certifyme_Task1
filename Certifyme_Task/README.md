Qatar Foundation — Admin Portal
A full-stack web application built for the CertifyMe intern assessment. The project provides a backend for the existing Admin UI to manage admin authentication and opportunity management.

Tech Stack

Frontend: HTML, CSS, JavaScript (provided — no changes made)
Backend: Python, Flask
Database: SQLite (via Flask-SQLAlchemy)


Project Structure
Test1/
├── backend/
│   ├── app.py               # Flask app, routes, DB setup
│   ├── auth.py              # Authentication routes
│   ├── opportunities.py     # Opportunity management routes
│   ├── models.py            # Database models
│   └── extensions.py        # SQLAlchemy instance
└── sky/
    ├── admin.html           # Frontend UI (provided, unchanged)
    ├── admin.css            # Styles (provided, unchanged)
    └── admin.js             # Frontend logic (API calls added)

How to Run
1. Go into the backend folder
bashcd Test1/backend
2. Install dependencies
bashpip install flask flask-sqlalchemy flask-cors werkzeug
3. Start the server
bashpython app.py
4. Open in browser
http://127.0.0.1:5000

Features Implemented
Task 1 — Login & Signup (Day 1)
US-1.1 — Admin Sign Up

Form fields: full name, email, password, confirm password
All fields required with validation
Email format validation
Password minimum 8 characters
Password and confirm password must match
Duplicate email check with error message
On success, account saved to database and redirected to login

US-1.2 — Admin Login

Form fields: email, password, Remember Me checkbox
Generic error message for wrong credentials
Remember Me checked → session stays active for 30 days
Remember Me unchecked → session ends when browser closes
On success, redirected to dashboard

US-1.3 — Forgot Password

Always shows same success message regardless of email existence (privacy protection)
If email is registered, generates a reset token and logs the link in the terminal
Reset link expires after 1 hour
Using an expired link shows a clear error message
No actual email sending (as per task requirement)


Task 2 — Opportunity Management (Day 2)
US-2.1 — View All Opportunities

Loads all opportunities for the logged-in admin on page open
Each card shows: name, category, duration, start date, description
All data from database — nothing hardcoded
Empty state message shown when no opportunities exist

US-2.2 — Add a New Opportunity

Modal form with required fields: Opportunity Name, Duration, Start Date, Description, Skills to Gain, Category, Future Opportunities
Maximum Applicants is optional
Category options: Technology, Business, Design, Marketing, Data Science, Other
All required fields validated before submission
On success, saved to database and card appears immediately without page refresh

US-2.3 — Opportunities Persist After Login

Opportunities stored in database
Loads correctly after logout and login
No browser memory or local storage used
One admin cannot see another admin's opportunities

US-2.4 — View Opportunity Details

View Details button on each card opens a details modal
Shows all fields: name, duration, start date, description, skills, category, future opportunities, maximum applicants
Close button to dismiss modal

US-2.5 — Edit an Opportunity

Edit button on each card
Opens the same form modal with all fields pre-filled
Same validations as create
On success, updates database and card refreshes immediately without page refresh
Only updates that specific opportunity

US-2.6 — Delete an Opportunity

Delete button on each card
Confirmation prompt before deleting
On confirm, permanently deleted from database and removed from UI immediately
On cancel, nothing changes
Only the admin who created the opportunity can delete it


API Endpoints
Auth
MethodEndpointDescriptionPOST/api/auth/signupRegister new adminPOST/api/auth/loginLogin adminPOST/api/auth/logoutLogout adminPOST/api/auth/forgot-passwordRequest password resetGET/POST/api/auth/reset-password/<token>Validate and reset password
Opportunities
MethodEndpointDescriptionGET/api/opportunities/Get all opportunities for logged-in adminPOST/api/opportunities/Create new opportunityGET/api/opportunities/<id>Get single opportunity detailsPUT/api/opportunities/<id>Update opportunityDELETE/api/opportunities/<id>Delete opportunity

Notes

Frontend UI was provided and has not been modified (HTML and CSS unchanged)
All opportunity data is tied to the logged-in admin account
Admins can only view, edit, and delete their own opportunities
Passwords are hashed using Werkzeug's security module
Sessions use Flask's built-in session management
