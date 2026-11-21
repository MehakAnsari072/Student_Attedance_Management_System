STUDENT ATTENDANCE MANAGEMENT SYSTEM
====================================

Technology:
- Python
- Django
- SQLite
- HTML and CSS

SETUP (Windows)
---------------
1. Extract this ZIP file.
2. Open the extracted folder in VS Code.
3. Open Terminal in VS Code.
4. Create a virtual environment:

   python -m venv env

5. Activate it:

   env\Scripts\activate

6. Install Django:

   pip install -r requirements.txt

7. Create database tables:

   python manage.py makemigrations
   python manage.py migrate

8. Create admin/teacher login:

   python manage.py createsuperuser

   Enter username, email (optional), and password.

9. Start the project:

   python manage.py runserver

10. Open this address in your browser:

    http://127.0.0.1:8000/

LOGIN
-----
Use the username and password created with createsuperuser.

FEATURES
--------
- Secure teacher/admin login and logout
- Dashboard with student and attendance statistics
- Add, edit and delete students
- Mark attendance as Present or Absent for a selected date
- Prevent duplicate attendance for the same student and date
- View attendance records
- Calculate attendance percentage for each student

NOTE
----
The database file is created automatically after running migrations.
Do not copy an old virtual environment into this project. Create a fresh
environment using the steps above.
