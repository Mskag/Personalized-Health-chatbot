from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Personalized Health Recommendations</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #f0f4f8;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 2rem 1rem;
    }
    .container {
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.10);
      padding: 2.5rem 2rem;
      width: 100%;
      max-width: 620px;
    }
    h1 { font-size: 1.5rem; font-weight: 700; color: #1a202c; margin-bottom: 0.25rem; }
    .subtitle { font-size: 0.92rem; color: #718096; margin-bottom: 2rem; }
    .section {
      background: #f7fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 1.25rem 1.25rem 1rem;
      margin-bottom: 1.25rem;
    }
    .section-title {
      font-size: 0.75rem; font-weight: 600; color: #718096;
      text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 1rem;
    }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .field { margin-bottom: 0.85rem; }
    .field:last-child { margin-bottom: 0; }
    label { display: block; font-size: 0.85rem; font-weight: 500; color: #4a5568; margin-bottom: 5px; }
    input[type="number"] {
      width: 100%; padding: 9px 12px;
      border: 1.5px solid #e2e8f0; border-radius: 8px;
      font-size: 0.95rem; color: #2d3748; background: #fff; outline: none;
      transition: border 0.15s;
    }
    input[type="number"]:focus { border-color: #4299e1; }
    .toggle-group {
      display: flex; border: 1.5px solid #e2e8f0;
      border-radius: 8px; overflow: hidden; width: fit-content;
    }
    .toggle-group button {
      padding: 8px 18px; border: none; background: #fff;
      font-size: 0.85rem; color: #718096; cursor: pointer;
      transition: all 0.15s; border-right: 1px solid #e2e8f0;
    }
    .toggle-group button:last-child { border-right: none; }
    .toggle-group button.active { background: #ebf8ff; color: #2b6cb0; font-weight: 600; }
    .bmi-badge { display: inline-flex; align-items: baseline; gap: 8px; margin-top: 10px; }
    .bmi-value { font-size: 1.6rem; font-weight: 700; color: #2d3748; }
    .bmi-cat { font-size: 0.8rem; font-weight: 600; padding: 3px 10px; border-radius: 999px; }
    .chip-group { display: flex; flex-wrap: wrap; gap: 8px; }
    .chip {
      padding: 6px 14px; border-radius: 999px;
      border: 1.5px solid #e2e8f0; background: #fff;
      font-size: 0.83rem; color: #4a5568; cursor: pointer; transition: all 0.15s;
    }
    .chip.selected { background: #ebf8ff; color: #2b6cb0; border-color: #bee3f8; font-weight: 600; }
    .chip:hover:not(.selected) { background: #f0f4f8; }
    .error { font-size: 0.78rem; color: #e53e3e; margin-top: 4px; display: none; }
    .submit-btn {
      width: 100%; padding: 13px; background: #3182ce; color: #fff;
      border: none; border-radius: 10px; font-size: 1rem; font-weight: 600;
      cursor: pointer; margin-top: 0.5rem; transition: background 0.15s;
    }
    .submit-btn:hover { background: #2b6cb0; }
    .results {
      background: #f0fff4; border: 1.5px solid #c6f6d5;
      border-radius: 12px; padding: 1.25rem; margin-top: 1.25rem; display: none;
    }
    .results-heading {
      font-size: 1rem; font-weight: 700; color: #276749;
      margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;
    }
    .results-heading::before {
      content: ''; display: inline-block; width: 10px; height: 10px;
      border-radius: 50%; background: #38a169;
    }
    .rec-item {
      display: flex; gap: 12px; padding: 10px 0;
      border-bottom: 1px solid #c6f6d5;
      font-size: 0.9rem; color: #2d3748; line-height: 1.6;
    }
    .rec-item:last-child { border-bottom: none; padding-bottom: 0; }
    .rec-num {
      min-width: 26px; height: 26px; border-radius: 50%;
      background: #c6f6d5; display: flex; align-items: center;
      justify-content: center; font-size: 0.75rem; font-weight: 700;
      color: #276749; flex-shrink: 0;
    }
    @media (max-width: 480px) { .row { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<div class="container">
  <h1>🩺 Health Recommendations</h1>
  <p class="subtitle">Fill in your details below to get personalized health advice.</p>

  <div class="section">
    <div class="section-title">Basic Information</div>
    <div class="row">
      <div class="field">
        <label for="age">Age</label>
        <input type="number" id="age" min="1" max="120" placeholder="e.g. 35" />
        <div class="error" id="err-age">Please enter a valid age (1–120).</div>
      </div>
      <div class="field">
        <label>Sex</label>
        <div class="toggle-group" id="sex-toggle">
          <button class="active" onclick="setSex('male', this)">Male</button>
          <button onclick="setSex('female', this)">Female</button>
          <button onclick="setSex('other', this)">Other</button>
        </div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Body Metrics</div>
    <div class="row">
      <div class="field">
        <label for="weight">Weight (kg)</label>
        <input type="number" id="weight" min="20" max="300" placeholder="e.g. 70" oninput="calcBMI()" />
      </div>
      <div class="field">
        <label for="height">Height (cm)</label>
        <input type="number" id="height" min="100" max="250" placeholder="e.g. 170" oninput="calcBMI()" />
      </div>
    </div>
    <div class="bmi-badge" id="bmi-display" style="display:none;">
      <span class="bmi-value" id="bmi-val"></span>
      <span class="bmi-cat" id="bmi-cat"></span>
    </div>
    <div class="error" id="err-bmi">Please enter valid weight and height.</div>
  </div>

  <div class="section">
    <div class="section-title">Lifestyle</div>
    <div class="field">
      <label>Activity Level</label>
      <div class="toggle-group" id="act-toggle">
        <button class="active" onclick="setActivity('sedentary', this)">Sedentary</button>
        <button onclick="setActivity('moderate', this)">Moderate</button>
        <button onclick="setActivity('active', this)">Active</button>
      </div>
    </div>
    <div class="field" style="margin-top:1rem;">
      <label>Do you smoke?</label>
      <div class="toggle-group" id="smoke-toggle">
        <button class="active" onclick="setSmoker(false, this)">No</button>
        <button onclick="setSmoker(true, this)">Yes</button>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Medical Conditions (select all that apply)</div>
    <div class="chip-group" id="conditions">
      <div class="chip" onclick="toggleChip(this)" data-val="hypertension">Hypertension</div>
      <div class="chip" onclick="toggleChip(this)" data-val="diabetes">Diabetes</div>
      <div class="chip" onclick="toggleChip(this)" data-val="asthma">Asthma</div>
      <div class="chip" onclick="toggleChip(this)" data-val="heart disease">Heart Disease</div>
      <div class="chip" onclick="toggleChip(this)" data-val="arthritis">Arthritis</div>
      <div class="chip" onclick="toggleChip(this)" data-val="none">None</div>
    </div>
  </div>

  <button class="submit-btn" onclick="submitForm()">Get My Recommendations</button>

  <div class="results" id="results">
    <div class="results-heading">Your Personalized Recommendations</div>
    <div id="rec-list"></div>
  </div>
</div>

<script>
  let sex = 'male', activity = 'sedentary', smoker = false, bmi = null;

  function setSex(val, btn) {
    sex = val;
    document.querySelectorAll('#sex-toggle button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  function setActivity(val, btn) {
    activity = val;
    document.querySelectorAll('#act-toggle button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  function setSmoker(val, btn) {
    smoker = val;
    document.querySelectorAll('#smoke-toggle button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  function toggleChip(el) {
    const isNone = el.dataset.val === 'none';
    if (isNone) {
      document.querySelectorAll('#conditions .chip').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
    } else {
      document.querySelector('[data-val="none"]').classList.remove('selected');
      el.classList.toggle('selected');
    }
  }
  function calcBMI() {
    const w = parseFloat(document.getElementById('weight').value);
    const h = parseFloat(document.getElementById('height').value) / 100;
    const disp = document.getElementById('bmi-display');
    const err = document.getElementById('err-bmi');
    if (w > 0 && h > 0.5 && h < 3) {
      bmi = +(w / (h * h)).toFixed(1);
      document.getElementById('bmi-val').textContent = bmi;
      const cat = document.getElementById('bmi-cat');
      if (bmi < 18.5) { cat.textContent = 'Underweight'; cat.style.background = '#fefcbf'; cat.style.color = '#744210'; }
      else if (bmi < 25) { cat.textContent = 'Normal'; cat.style.background = '#c6f6d5'; cat.style.color = '#276749'; }
      else if (bmi < 30) { cat.textContent = 'Overweight'; cat.style.background = '#feebc8'; cat.style.color = '#7b341e'; }
      else { cat.textContent = 'Obese'; cat.style.background = '#fed7d7'; cat.style.color = '#822727'; }
      disp.style.display = 'flex';
      err.style.display = 'none';
    } else {
      bmi = null;
      disp.style.display = 'none';
    }
  }
  async function submitForm() {
    const age = parseInt(document.getElementById('age').value);
    const errAge = document.getElementById('err-age');
    const errBmi = document.getElementById('err-bmi');
    let valid = true;
    if (!age || age < 1 || age > 120) { errAge.style.display = 'block'; valid = false; } else { errAge.style.display = 'none'; }
    if (!bmi) { errBmi.style.display = 'block'; valid = false; } else { errBmi.style.display = 'none'; }
    if (!valid) return;

    const conditions = [...document.querySelectorAll('#conditions .chip.selected')]
      .map(c => c.dataset.val).filter(v => v !== 'none');

    const payload = { age, sex, bmi, activity_level: activity, smoker, medical_conditions: conditions };

    const resp = await fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();

    const list = document.getElementById('rec-list');
    list.innerHTML = data.recommendations.map((r, i) =>
      `<div class="rec-item"><div class="rec-num">${i + 1}</div><div>${r}</div></div>`
    ).join('');
    const res = document.getElementById('results');
    res.style.display = 'block';
    res.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
</script>
</body>
</html>
"""


def get_health_recommendations(user_profile):
    age = user_profile.get('age')
    sex = user_profile.get('sex')
    bmi = user_profile.get('bmi')
    activity_level = user_profile.get('activity_level')
    smoker = user_profile.get('smoker')
    conditions = user_profile.get('medical_conditions', [])

    recommendations = []

    # BMI Advice
    if bmi < 18.5:
        recommendations.append("Your BMI indicates you're underweight. Consider a nutrient-dense, higher-calorie diet.")
    elif 18.5 <= bmi < 25:
        recommendations.append("Your BMI is in the normal range. Maintain your current lifestyle with balanced nutrition and regular activity.")
    elif 25 <= bmi < 30:
        recommendations.append("You are overweight. Try to increase physical activity and monitor portion sizes.")
    else:
        recommendations.append("You are in the obese range. It's advisable to consult a healthcare provider for a weight loss plan.")

    # Age-Based Screening
    if age >= 45:
        recommendations.append("Consider regular screening for diabetes, cholesterol, and blood pressure.")
    if sex == 'female' and age >= 50:
        recommendations.append("Schedule regular bone density scans to check for osteoporosis.")

    # Activity Level
    if activity_level == 'sedentary':
        recommendations.append("Try to include at least 30 minutes of moderate exercise 5 days a week.")
    elif activity_level == 'active':
        recommendations.append("Great! Keep up your physical activity.")

    # Smoking
    if smoker:
        recommendations.append("Quitting smoking greatly reduces your risk for heart disease and cancer.")

    # Chronic Conditions
    for condition in conditions:
        c = condition.lower()
        if c == 'hypertension':
            recommendations.append("Reduce sodium intake and monitor your blood pressure regularly.")
        if c == 'diabetes':
            recommendations.append("Maintain a low-glycemic diet and check blood sugar levels regularly.")
        if c == 'asthma':
            recommendations.append("Avoid known allergens and keep an inhaler accessible.")
        if c == 'heart disease':
            recommendations.append("Follow a heart-healthy diet, limit saturated fats, and attend regular cardiac check-ups.")
        if c == 'arthritis':
            recommendations.append("Engage in low-impact exercises like swimming or yoga to maintain joint mobility.")

    return recommendations


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    recs = get_health_recommendations(data)
    return jsonify({'recommendations': recs})


if __name__ == '__main__':
    print("Starting Health Recommendations app...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True)
