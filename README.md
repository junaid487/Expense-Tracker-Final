# Expense Tracker | Streamlit App

A personal expense tracking web application built with **Streamlit**, **pandas**, and **Plotly**, featuring persistent storage using **Google Sheets** as a lightweight backend.



This project focuses on clean data handling, UI responsiveness, and practical engineering tradeoffs.

## Expense Tracker Demo

![Expense Tracker Demo](expense%20tracker.gif)

## Live Demo
[Check out the App](https://junaidexp.streamlit.app/)

## Features
* Full CRUD: Add, delete, and clear expenses.
* Smart Filtering: Category, date range presets, and amount-based filtering.
* Search: Real-time search across Name and Notes fields.
* Visualizations: Interactive Plotly Bar, Pie, and Area charts.
* Data Portability: Export filtered data to CSV or Excel.
* Persistent Storage: Data remains safe across sessions via Google Sheets API.
* Mobile-Friendly: Custom CSS and Floating Action Button for quick entry.

## Tech Stack
* Frontend/Framework: Streamlit
* Data Handling: pandas, NumPy
* Visualization: Plotly
* Persistence Layer: Google Sheets API
* Auth: Google Service Account (OAuth2)
* Deployment: Streamlit Cloud

## Architecture and Decisions

### Why Google Sheets as a Backend?
This project uses Google Sheets as a persistence layer instead of a traditional SQL database.

* Advantages: Completely free and serverless.
* Security: Access is restricted via a Google Service Account. Only the app (authenticated via a private key) can read or write data.
* Tradeoffs: Designed for single-user scenarios. **Not** intended for high-traffic production environments due to API rate limits.

### Design Philosophy
* Clarity over Premature Optimization: Prioritized a clean user experience and robust error handling.
* Data Integrity: Implemented duplicate detection and type validation before pushing to the cloud.
* Performance: Utilized Streamlit’s caching to minimize network latency during data retrieval.

## Local Development

To run this project locally, follow these steps:

* Clone the repository:
   git clone https://github.com/junaid487/Expense-Tracker-Final.git<br>
   cd Expense-Tracker-Final

* Install the required dependencies:
   pip install -r requirements.txt

---

Configure Streamlit Secrets:
- The application requires a connection to Google Sheets via a Service Account. You must create a folder named .streamlit in the root directory and a file named secrets.toml inside it. Use the following structure:

[connections.gsheets]<br>
spreadsheet = "[https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit](https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit)"<br>
type = "service_account"<br>
project_id = "your-project-id"<br>
private_key_id = "your-private-key-id"<br>
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Key-Here\n-----END PRIVATE KEY-----\n"<br>
client_email = "your-service-account-email"<br>
client_id = "your-client-id"<br>
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"<br>
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"<br>
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"<br>
client_x509_cert_url = "your-cert-url"<br>

* Run the application:
   streamlit run app.py

---

## Limitations

* This application uses a single shared Google Sheet as its dataBase.

* User authentication and data isolation are not implemented.

* As a result, the app is intended for single-user usage only.

---
Built with Python by **Junaid Alam**.
