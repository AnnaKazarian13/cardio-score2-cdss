# CardioScore2: CDSS для оценки кардиоваскулярного риска

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**English summary:** Interactive Streamlit CDSS that estimates 10-year CVD risk using the **SCORE2** model (ESC), calibrated for very-high-risk regions (Eastern Europe / CIS). Includes syndrome flags, what-if simulation (Plotly), and patient-oriented guidance based on ESC/ESH and ACC/AHA context.

Интерактивное веб-приложение (клиническая система поддержки принятия решений — **CDSS**) для оценки **10-летнего риска** фатальных и нефатальных сердечно-сосудистых заболеваний (ССЗ).

В основе калькулятора — прогностическая модель **SCORE2 (European Society of Cardiology)**, откалиброванная под регионы с *очень высоким* базовым кардиориском (страны СНГ и Восточной Европы).

---

## Ключевой функционал

* **Расчёт риска SCORE2** по базовым параметрам пациента
* **Синдромальный анализ:** подсказки по сочетаниям вроде артериальной гипертензии, дислипидемии, подозрения на СГХС, гипоальфахолестеринемии
* **What-If симулятор (Plotly):** как меняется риск при отказе от курения / нормализации давления
* **Гайдлайны для пациента:** персонализированные рекомендации в духе ESC/ESH и ACC/AHA

---

## Стек

* **Python 3.11+** (`math` + логика SCORE2)
* **Streamlit** — UI
* **Plotly** — интерактивные графики

---

## Локальный запуск

### 1. Клонирование

```bash
git clone https://github.com/AnnaKazarian13/cardio-score2-cdss.git
cd cardio-score2-cdss
```

### 2. Окружение и зависимости

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Запуск приложения

```bash
streamlit run main.py
```

Откройте адрес из терминала (обычно `http://localhost:8501`).

---

## Структура репозитория

```
cardio-score2-cdss/
├── main.py              # Streamlit-приложение + SCORE2
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Автор

[AnnaKazarian13](https://github.com/AnnaKazarian13)
