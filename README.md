# Personalized Health Recommendation Chatbot

##  Overview
This project is a **Flask-based personalized health recommendation web application** that provides customized lifestyle and medical advice based on user inputs. The system collects user data such as age, BMI, activity level, smoking habits, and existing medical conditions, and generates **rule-based health recommendations** in real-time. It demonstrates the integration of **web development, data processing, and healthcare logic** into an interactive application.

Link for the web portal: https://personalized-health-chatbot.onrender.com/
(Released using Render)
---

## Objectives
- Provide **personalized health recommendations**
- Promote **preventive healthcare awareness**
- Build an interactive **chatbot-like web interface**
- Demonstrate **real-world healthcare application development**

---

## Technologies Used

### Backend
- **Python**
- **Flask** → Web framework for handling requests and responses

### Frontend
- HTML, CSS, JavaScript (embedded in Flask using `render_template_string`)
- Responsive UI with interactive components

### Data Handling
- JSON-based communication between frontend and backend

---

## Features

### User Input Collection
- Age
- Sex
- Weight & Height → BMI calculation
- Activity level (Sedentary / Moderate / Active)
- Smoking status
- Medical conditions (Hypertension, Diabetes, etc.)

---

### BMI Calculation
- Automatically calculated from:
  - Weight (kg)
  - Height (cm)

- Categorized into:
  - Underweight
  - Normal
  - Overweight
  - Obese

---

### Recommendation Engine (Core Logic)

The system uses a **rule-based decision system** to generate recommendations:

#### BMI-based advice
- Suggests diet, exercise, or medical consultation

#### Age-based screening
- Preventive health check suggestions

#### Lifestyle recommendations
- Activity improvements
- Smoking cessation advice

#### Disease-specific guidance
- Hypertension → Low sodium diet
- Diabetes → Low glycemic diet
- Asthma → Avoid triggers
- Heart disease → Cardiac care
- Arthritis → Joint-friendly exercises

---

### Chatbot-like Output
- Displays recommendations dynamically
- Clean UI with numbered suggestions
- Smooth scrolling and interactive experience

---

## Workflow

1. User enters health details via UI  
2. BMI is calculated on the frontend  
3. Data is sent to Flask backend via POST request  
4. Backend processes data using rule-based logic  
5. Recommendations are returned as JSON  
6. Results displayed dynamically on the webpage  

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/health-chatbot.git
cd health-chatbot
