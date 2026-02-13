# Expense Tracker | Streamlit App



A personal expense tracking web application built with **Streamlit**, **pandas**, and **Plotly**, featuring persistent storage using **Google Sheets** as a lightweight backend.



This project focuses on **clean data handling, UI responsiveness, and practical tradeoffs**.



---



## Features



- Add, delete, and clear expenses

- Category, date, and amount-based filtering

- Interactive visualizations (Bar, Pie, Line charts)

- CSV and Excel export

- Persistent storage across sessions

- Clean, minimal UI with floating action controls


---

## Limitations

-This application uses a single shared Google Sheet as its data store.

-User authentication and data isolation are not implemented.

-As a result, the app is intended for single-user usage in its current state.

---


## Tech Stack



- **Frontend / App Framework**: Streamlit  

- **Data Handling**: pandas, NumPy  

- **Visualization**: Plotly  

- **Persistence Layer**: Google Sheets API  

- **Auth**: Google Service Account  

- **Deployment**: Streamlit Cloud



---



## Why Google Sheets as a Backend?



This project intentionally uses **Google Sheets** as a persistence layer instead of a traditional database.



### Advantages

- Completely free

- Serverless and easy to manage

- Secure via service-account–only access



### Tradeoffs

- Not designed for high concurrency

- Higher latency compared to databases

- Write operations are slower due to network calls



This choice was made deliberately to balance **simplicity, security, and zero cost** for a single-user application.



> For production or multi-user scenarios, this backend can be replaced with SQLite, Supabase, or PostgreSQL with minimal changes to the app logic.



---



## Performance Considerations



- Google Sheets access is cached using Streamlit’s caching primitives to reduce latency on reruns.

- Cache invalidation is handled explicitly after write operations to ensure data consistency.

- UI feedback (toasts) is used to improve perceived responsiveness.



---



## Security Model



- Google Sheet is **not public**

- Access is restricted to a **single service account**

- Credentials are stored securely using **Streamlit Secrets**

- No user authentication data is stored



---



## Design Philosophy



- Prefer clarity over premature optimization

- Treat data mutations as validated operations

- Make calculated tradeoffs

- Build portfolio projects as **real systems**



---



## Local Development



```bash

pip install -r requirements.txt

streamlit run app.py



