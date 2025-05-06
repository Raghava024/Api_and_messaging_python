# API and Messaging Projects in Python

This repository contains a set of Python mini-projects that use APIs, messaging services, and automation to solve real-world problems. Each project demonstrates how to work with external APIs, manage data, and send messages or alerts.

---

## 📁 Projects Overview

### 🎂 Birthday Wisher
Sends birthday wishes via email using pre-written letter templates and contact data from a CSV file.

- Uses `smtplib` for email.
- Reads birthdays from `birthdays.csv`.
- Randomly selects a letter template from `letter_templates/`.

### ✈️ Flight Tracker
Notifies users when there’s a price drop in flights for tracked destinations.

- Integrates with Sheety API and Tequila Kiwi API.
- Sends alerts using email or SMS.
- Environment variables stored in `.env`.

### 🧠 Kanye Quotes API
Displays random quotes from Kanye West over a background image.

- Fetches quotes using the Kanye Rest API.
- GUI display using `tkinter`.

### 🌧️ Rain Alert
Sends an SMS alert if rain is predicted in the next 12 hours.

- Uses OpenWeatherMap API.
- Sends messages via Twilio.

---

## 🛠 Technologies Used

- Python
- REST APIs
- `smtplib`, `requests`, `dotenv`, `tkinter`
- Twilio API
- Sheety & Tequila Kiwi APIs
- Email and CSV handling

---

## 🔒 Note

Remember to store your API keys and sensitive information securely in the `.env` file (excluded using `.gitignore`).

---

## 📬 Author

Developed by [Your Name]

---

## 📌 License

This project is open-source and available under the [MIT License](LICENSE).
