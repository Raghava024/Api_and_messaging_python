Sure! Here's a **detailed `README.md`** for your `API_AND_MESSAGING_PYTHON` project, all in one code block:

```markdown
# API_AND_MESSAGING_PYTHON

This repository is a collection of Python mini-projects focused on using APIs and messaging services to automate real-world tasks. These projects demonstrate the power of APIs, environment configuration, external libraries, and basic automation techniques in Python.

---

## 📁 Project Structure



API\_AND\_MESSAGING\_PYTHON/
│
├── Birthday\_wisher/
│   ├── letter\_templates/
│   │   ├── letter\_1.txt
│   │   ├── letter\_2.txt
│   │   └── letter\_3.txt
│   ├── birthdays.csv
│   └── main.py
│
├── Flight\_tracker/
│   ├── .env
│   ├── data\_manager.py
│   ├── flight\_data.py
│   ├── flight\_search.py
│   ├── main.py
│   └── notification\_manager.py
│
├── Kanye\_api/
│   ├── background.png
│   ├── kanye.png
│   └── main.py
│
└── Rain\_alert/
└── main.py



---

## 🚀 Projects Overview

### 🎂 Birthday Wisher
Automates the process of sending birthday emails using pre-written letters.

- Reads birthday data from `birthdays.csv`.
- Picks a random letter template.
- Sends an email using `smtplib`.

📌 **Libraries Used**: `pandas`, `datetime`, `smtplib`, `random`

---

### ✈️ Flight Tracker
Tracks flight prices and notifies the user when a flight deal is found.

- Integrates with the Kiwi Tequila API for flight data.
- Uses the Sheety API to manage Google Sheet data.
- Sends notifications via email or other messaging services.

📌 **Libraries Used**: `requests`, `smtplib`, `os`, `dotenv`

💡 **Files Description**:
- `data_manager.py`: Handles data operations with Sheety.
- `flight_search.py`: Searches flights via the Kiwi API.
- `flight_data.py`: Formats and holds flight data.
- `notification_manager.py`: Sends email or SMS alerts.

---

### 🧠 Kanye Quotes API
Displays random quotes by Kanye West in a GUI.

- Uses the Kanye REST API.
- GUI created with `tkinter`.

📌 **Libraries Used**: `requests`, `tkinter`

---

### 🌧️ Rain Alert
Sends SMS alerts if rain is forecasted in the next 12 hours.

- Uses the OpenWeatherMap API.
- Sends SMS using Twilio API.

📌 **Libraries Used**: `requests`, `os`, `dotenv`, `twilio`

---

## 🔧 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/API_AND_MESSAGING_PYTHON.git
   cd API_AND_MESSAGING_PYTHON
````

2. **Create and Activate Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**
   Add your API keys, email credentials, and other sensitive data:

   ```
   EMAIL=your_email@example.com
   PASSWORD=your_password
   SHEETY_ENDPOINT=https://api.sheety.co/...
   TEQUILA_API_KEY=your_key
   TWILIO_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   ```

5. **Run Any Project**

   ```bash
   python Birthday_wisher/main.py
   python Flight_tracker/main.py
   python Kanye_api/main.py
   python Rain_alert/main.py
   ```

---

## 🛠 Technologies Used

* Python
* REST APIs (Kiwi, Sheety, Kanye REST, OpenWeatherMap, Twilio)
* Email and SMS Automation
* File I/O and CSV Handling
* GUI with `tkinter`
* `.env` for config and security

---

## 🔒 Security Notice

Make sure to never expose your `.env` file or sensitive credentials publicly. This project uses a `.gitignore` file to exclude `.env` from version control.

---

