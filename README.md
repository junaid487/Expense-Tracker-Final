# Expense Tracker | Streamlit & MySQL App

A full-stack expense tracking web application built with **Streamlit**, **Pandas**, and **Plotly**, featuring persistent storage using a **MySQL** database.

This project focuses on modular architecture, clean data handling, and interactive visualizations.

## Live Demo
[Check out the App](https://junaidexp.streamlit.app/)

> Note:
> This demo uses a shared public database without authentication.
> Any data added, edited, or deleted is visible to all users.
> To Do: add authentication.

## Features
- **Full CRUD**: Add, delete, and clear expenses with instant database synchronization.
- **Advanced Filtering**: Filter by category, date range presets, and amount sliders.
- **Real-time Search**: Quick search across expense names and notes.
- **Data Visualizations**: Interactive Plotly Bar, Pie, and Area charts for spending analysis.
- **Data Portability**: Export filtered data directly to CSV or Excel.
- **Modular Architecture**: Clean separation of concerns (Database, UI, Utilities).
- **Responsive Design**: Custom CSS and a Floating Action Button (FAB) for user-friendly use.
- **Cloud Deployment**: Streamlit Community Cloud

## Tech Stack
- **Frontend/Framework**: Streamlit
- **Data Handling**: Pandas, NumPy
- **Visualization**: Plotly
- **Backend Database**: MySQL
- **Environment Management**: Python-dotenv
- **Connectivity**: mysql-connector-python

## Architecture
The project is organized into logical modules to ensure maintainability:
- `app.py`: Main entry point and UI layout.
- `database.py`: Handles all MySQL CRUD operations and connection management.
- `ui_components.py`: Encapsulates complex UI elements like Dialogs and FAB.
- `utils.py`: Shared helper functions for charting, formatting, and exports.

## Local Development

To run this project locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/junaid487/Expense-Tracker-Final.git
cd Expense-Tracker-Final
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
1. Create a MySQL database named `expense_tracker`.
2. Create the `expenses` table using the following schema:
```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    time TIME,
    name VARCHAR(255),
    amount INT,
    category VARCHAR(100),
    notes TEXT
);
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your MySQL credentials:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=expense_tracker
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## Design Philosophy
- **Separation of Concerns**: Decoupled the database logic from the UI layer.
- **User-Centric Design**: Focused on a premium feel with glassmorphism and smooth animations.
- **Data Integrity**: Used proper SQL types and Pandas for robust data validation.

---
Built by **Junaid Alam**.
