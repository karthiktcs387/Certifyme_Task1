# Qatar Foundation — Admin Portal

A full-stack web application built for the CertifyMe intern assessment.  
The project provides a backend for the existing Admin UI to manage admin authentication and opportunity management.

---

##  Tech Stack

- **Frontend:** HTML, CSS, JavaScript (provided — no changes made)  
- **Backend:** Python, Flask  
- **Database:** SQLite (Flask-SQLAlchemy)  

---

##  Project Structure


Test1/
├── backend/
│ ├── app.py # Flask app, routes, DB setup
│ ├── auth.py # Authentication routes
│ ├── opportunities.py # Opportunity management routes
│ ├── models.py # Database models
│ └── extensions.py # SQLAlchemy instance
└── sky/
├── admin.html # Frontend UI (provided, unchanged)
├── admin.css # Styles (provided, unchanged)
└── admin.js # Frontend logic (API calls added)


---

##  How to Run

### 1. Navigate to backend folder
```bash
cd Test1/backend
2. Install dependencies
pip install flask flask-sqlalchemy flask-cors werkzeug
3. Run the server
python app.py
4. Open in browser
http://127.0.0.1:5000
 Features Implemented
 Task 1 — Login & Signup (Day 1)
US-1.1 — Admin Sign Up
Required fields: full name, email, password, confirm password
Email format validation
Password minimum 8 characters
Password match validation
Duplicate email check
On success → saved to DB + redirect to login
US-1.2 — Admin Login
Fields: email, password, Remember Me
Generic error for invalid credentials
Remember Me:
 Checked → session 30 days
 Unchecked → session ends on browser close
On success → redirect to dashboard
US-1.3 — Forgot Password
Same response for all emails (security)
Generates reset token if email exists
Reset link logged in terminal
Token expires in 1 hour
Expired link → error message
No email sending (as per requirement)
 Task 2 — Opportunity Management (Day 2)
US-2.1 — View Opportunities
Loads all opportunities on login
Displays:
Name, category, duration, start date, description
Shows empty state if none exist
US-2.2 — Add Opportunity
Modal form with required fields
Category options:
Technology, Business, Design, Marketing, Data Science, Other
Max applicants optional
Validations applied
Instant UI update (no refresh)
US-2.3 — Data Persistence
Stored in database
Survives logout/login
No local storage used
Admin-specific data isolation
US-2.4 — View Details
"View Details" modal
Displays full information
Close button included
US-2.5 — Edit Opportunity
Pre-filled modal form
Same validation rules
Updates instantly without refresh
Only affects selected record
US-2.6 — Delete Opportunity
Confirmation prompt
Permanent deletion
UI updates instantly
Only creator can delete
 API Endpoints
Auth
Method	Endpoint	Description
POST	/api/auth/signup	Register admin
POST	/api/auth/login	Login admin
POST	/api/auth/logout	Logout admin
POST	/api/auth/forgot-password	Request reset
GET/POST	/api/auth/reset-password/<token>	Reset password
Opportunities
Method	Endpoint	Description
GET	/api/opportunities/	Get all opportunities
POST	/api/opportunities/	Create opportunity
GET	/api/opportunities/<id>	Get single
PUT	/api/opportunities/<id>	Update
DELETE	/api/opportunities/<id>	Delete
 Notes
Frontend UI is unchanged (provided)
Opportunities are user-specific
Admins can only manage their own data
Passwords are securely hashed using Werkzeug
Session handled using Flask session management
 Author

Karthik
GitHub: https://github.com/karthiktcs387
