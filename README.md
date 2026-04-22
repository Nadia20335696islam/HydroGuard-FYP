💧 HydroGuard

A Smart Water Conservation Web Application

📌 Overview

HydroGuard is a full-stack web application developed using Django that promotes responsible water usage through tracking, feedback, and behavioural engagement. The system enables users to monitor their daily water consumption, receive insights, and stay motivated through gamification features such as points, badges, and challenges.

The application is designed to support sustainability awareness and aligns with global initiatives such as UN Sustainable Development Goal 6: Clean Water and Sanitation.

🚀 Features
👤 User Management
User registration and login (custom authentication system)
Secure password hashing using PBKDF2-HMAC-SHA256
Session-based access control
Guest mode with limited access
💧 Water Usage Tracking
Add and manage daily water usage records
Track activities (e.g., shower, dishwashing, laundry)
Store usage data with timestamps and details
View usage history and summaries
📊 Data Processing & Insights
Calculate total and average water usage
Display latest activity and trends
Visualise data using charts
🎮 Gamification System
Earn eco points for water-saving actions
Level progression and daily streak tracking
Unlock badges based on milestones
Daily missions to encourage engagement
Interactive mini-game (“Water Rescue Challenge”)
🌍 Community Feature
View shared water-saving tips
Submit community contributions (authenticated users only)
Guest users can view but not interact
🏗️ System Architecture

HydroGuard follows Django’s Model-View-Template (MVT) architecture and is organised into modular applications:

accounts → User authentication and session handling
usage → Water usage tracking and data processing
core → Dashboard, navigation, and overall integration
🛠️ Technologies Used
Backend
Python
Django
Frontend
HTML
CSS (Bootstrap)
JavaScript
Database
SQLite (default Django database)
Tools
Visual Studio Code
Git & GitHub
Figma (UI design)
🔐 Security Features
Password hashing with salt (PBKDF2)
CSRF protection for secure requests
Session-based authentication
Access control for protected features
📂 Project Structure
HydroGuard/
│
├── accounts/        # User authentication logic
├── usage/           # Water usage tracking
├── core/            # Dashboard and main views
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── manage.py
└── db.sqlite3
⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/HydroGuard-FYP.git
cd HydroGuard-FYP
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install django
4. Run migrations
python manage.py migrate
5. Start the server
python manage.py runserver
6. Open in browser
http://127.0.0.1:8000/
🧪 Testing
Manual testing was performed across:
User authentication
Water usage input
Dashboard navigation
Gamification features
Guest vs authenticated access
⚠️ Limitations
Gamification system is partially template-driven (not fully database-based)
No external API integration for real-time water data
Community feature does not include moderation
Limited advanced analytics (e.g., prediction models)
🔮 Future Improvements
Fully dynamic gamification system (database-driven)
Integration with real-world water usage APIs
Advanced analytics and AI-based recommendations
Mobile app version
Community moderation and ranking system
🎓 Academic Context

This project was developed as a Final Year Project (FYP) for a BSc Computer Science degree at the University of Westminster.

👤 Author

Honey (Nadia Islam)
Computer Science Student
University of Westminster

📜 License

This project is for academic purposes.
Feel free to explore and learn from the code.

⭐ Acknowledgements
Django Documentation
Bootstrap Framework
Open-source learning resources
