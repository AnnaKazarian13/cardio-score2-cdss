import math
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="CardioScore2 | Экспертная система ССЗ",
    page_icon="❤️",
    layout="wide",
)


def calculate_score2_risk(age, sex, sbp, total_chol, hdl_chol, is_smoking):
    c_age = (age - 60) / 5
    c_sbp = (sbp - 120) / 20
    c_tchol = total_chol - 6
    c_hdl = (hdl_chol - 1.3) / 0.5
    smoke = 1 if is_smoking else 0

    if sex == "Женский":
        l_pred = (
            (0.3742 * c_age)
            + (0.6012 * smoke)
            + (0.2777 * c_sbp)
            + (0.1458 * c_tchol)
            + (-0.2698 * c_hdl)
        )
        l_pred += (
            (-0.0755 * c_age * smoke)
            + (-0.0255 * c_age * c_sbp)
            + (-0.0281 * c_age * c_tchol)
        )
        scale1, scale2 = 0.5836, 0.8294
    else:
        l_pred = (
            (0.4648 * c_age)
            + (0.7744 * smoke)
            + (0.3131 * c_sbp)
            + (0.1002 * c_tchol)
            + (-0.2606 * c_hdl)
        )
        l_pred += (
            (-0.1088 * c_age * smoke)
            + (-0.0277 * c_age * c_sbp)
            + (-0.0226 * c_age * c_tchol)
        )
        scale1, scale2 = 0.9412, 0.8329

    uncalibrated_risk = 1 - math.exp(-math.exp(l_pred))
    uncalibrated_risk = max(0.00001, min(0.99999, uncalibrated_risk))

    final_score = 1 - math.exp(
        -math.exp(scale1 + scale2 * math.log(-math.log(1 - uncalibrated_risk)))
    )
    return final_score * 100


def get_risk_info(risk, age):
    if age < 50:
        low_bound, high_bound = 2.5, 7.5
    elif 50 <= age < 70:
        low_bound, high_bound = 5.0, 10.0
    else:
        low_bound, high_bound = 7.5, 15.0

    if risk < low_bound:
        return "Низкий / Умеренный", "#2ecc71"
    elif risk < high_bound:
        return "ВЫСОКИЙ", "#f39c12"
    else:
        return "ОЧЕНЬ ВЫСОКИЙ", "#e74c3c"


def analyze_pathologies(sbp, total_chol, hdl, is_smoking, current_risk, sex):
    pathologies = []

    if sbp >= 140:
        if sbp >= 160:
            pathologies.append(
                {
                    "title": "Артериальная гипертензия II-III степени",
                    "source": "Протокол ESC/ESH 2024",
                    "status": "critical",
                    "desc": "Стойкое опасное повышение систолического давления.",
                    "actions": [
                        "Немедленное обращение к терапевту или кардиологу для подбора комбинированной антигипертензивной терапии.",
                        "Заведение дневника давления: замеры утром и вечером ежедневно.",
                        "Ограничение потребления поваренной соли до уровня менее 5 г/сутки (1 чайная ложка без верха).",
                        "Исключение скрытой соли: полуфабрикаты, колбасы, фастфуд.",
                    ],
                }
            )
        else:
            pathologies.append(
                {
                    "title": "Артериальная гипертензия I степени",
                    "source": "Протокол ESC/ESH 2024",
                    "status": "warning",
                    "desc": "Начальная стадия гипертонической болезни.",
                    "actions": [
                        "Консультация врача. Оценка поражения органов-мишеней (ЭхоКГ, почки).",
                        """Модификация образа жизни на 3-6 месяцев (аэробные нагрузки по 30 минут 5 раз в неделю).""",
                        "Если через 6 месяцев давление не нормализуется — начало медикаментозной терапии.",
                    ],
                }
            )

    remnant_chol = total_chol - hdl
    if total_chol > 4.9 or remnant_chol > 3.4:
        if total_chol >= 7.5:
            pathologies.append(
                {
                    "title": "Выраженная гиперхолестеринемия (Подозрение на СГХС)",
                    "source": "Рекомендации ЕОК/ЕОА по дислипидемиям",
                    "status": "critical",
                    "desc": "Экстремально высокий уровень общего холестерина. Требуется исключить семейную гиперхолестеринемию.",
                    "actions": [
                        "Срочно сдать развернутый липидный профиль (ЛПНП, ЛПВП, Триглицериды, АпоВ).",
                        "Сделать УЗИ сонных артерий (УЗДГ БЦА) для выявления скрытых атеросклеротических бляшек.",
                        "Обратиться к липидологу/кардиологу. В 95% случаев требуется немедленный старт высокоинтенсивных статинов (Аторвастатин/Розувастатин).",
                    ],
                }
            )
        else:
            pathologies.append(
                {
                    "title": "Дислипидемия (Нарушение липидного обмена)",
                    "source": "Рекомендации ЕОК/ЕОА по дислипидемиям",
                    "status": "warning",
                    "desc": "Повышен атерогенный потенциал крови.",
                    "actions": [
                        "Переход на Средиземноморскую диету: минимизация трансжиров, увеличение в рационе жирной рыбы, оливкового масла и клетчатки.",
                        "Целевой уровень ЛПНП зависит от вашего SCORE2. При высоком риске цель — ЛПНП < 1.8 ммоль/л, при очень высоком — < 1.4 ммоль/л.",
                        "Контрольный анализ крови через 8-12 недель диеты.",
                    ],
                }
            )

    if hdl < 1.0 and sex == "Мужской":
        pathologies.append(
            {
                "title": "Гипоальфахолестеринемия",
                "source": "Протокол АСС/AHA 2023",
                "status": "warning",
                "desc": "Критически низкий уровень антиатерогенного ('хорошего') холестерина.",
                "actions": [
                    "Полный отказ от курения (это главный фактор снижения ЛПВП).",
                    "Добавление регулярных кардионагрузок высокой интенсивности.",
                    "Включение в рацион продуктов, богатых Омега-3 полиненасыщенными жирными кислотами.",
                ],
            }
        )
    elif hdl < 1.2 and sex == "Женский":
        pathologies.append(
            {
                "title": "Гипоальфахолестеринемия (Женский профиль)",
                "source": "Протокол АСС/AHA 2023",
                "status": "warning",
                "desc": "Дефицит 'хорошего' холестерина у женщин повышает риски быстрее, чем у мужчин.",
                "actions": [
                    "Оценка метаболического профиля (сдать индекс HOMA-IR, глюкозу натощак).",
                    "Отказ от простых углеводов и сахаров, снижающих фракцию ЛПВП.",
                    "Увеличение физической активности.",
                ],
            }
        )

    if is_smoking:
        pathologies.append(
            {
                "title": "Табачная зависимость как критический фактор риска",
                "source": "ESC Prevention Guidelines",
                "status": "critical",
                "desc": "Курение удваивает скорость развития атеросклеротических бляшек.",
                "actions": [
                    "Рассмотреть никотинзаместительную терапию (пластыри, жевательные резинки) или консультацию терапевта для назначения препаратов (варениклин/цитизин).",
                    "Отказ от курения снижает риск инфаркта в два раза уже через 1 год.",
                ],
            }
        )

    return pathologies


st.title("❤️ Экспертный Кардио-Скрининг & Мониторинг: SCORE2 + Симуляция")
st.markdown(
    """
    **Достоверная клиническая база:** Модель построена на базе актуальных руководств **Европейского общества кардиологов (ESC)** и **ACC/AHA**.  
    Калькулятор адаптирован для регионов **очень высокого базового риска** ССЗ.
    """
)
st.write("---")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📋 Профиль пациента")

    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        age = st.slider("Возраст (лет)", min_value=40, max_value=69, value=55, step=1)
    with sub_col2:
        sex = st.radio("Биологический пол", ["Мужской", "Женский"], horizontal=True)

    st.write("---")

    sbp = st.slider(
        "Систолическое АД (верхнее, мм рт. ст.)",
        min_value=100,
        max_value=180,
        value=150,
        step=5,
    )

    sub_col3, sub_col4 = st.columns(2)
    with sub_col3:
        t_chol = st.number_input(
            "Общий холестерин (ммоль/л)",
            min_value=2.0,
            max_value=9.0,
            value=6.2,
            step=0.1,
            format="%.1f",
        )
    with sub_col4:
        hdl = st.number_input(
            "Холестерин ЛПВП (ммоль/л)",
            min_value=0.5,
            max_value=3.0,
            value=1.1,
            step=0.1,
            format="%.1f",
        )

    st.write("---")

    is_smoking = st.checkbox(
        "Пациент курит в настоящее время",
        value=True,
        help="Факт курения в течение последнего года.",
    )

with col2:
    st.subheader("📊 Расчет 10-летнего риска ССЗ")

    current_risk = calculate_score2_risk(age, sex, sbp, t_chol, hdl, is_smoking)
    category, color = get_risk_info(current_risk, age)

    st.markdown(
        f"""
        <div style="background-color: {color}15; border-left: 5px solid {color}; padding: 20px; border-radius: 5px;">
            <h4 style="color: {color}; margin: 0;">Категория: {category} РИСК</h4>
            <p style="font-size: 36px; font-weight: bold; margin: 10px 0 0 0; color: #111;">{current_risk:.2f}%</p>
            <p style="font-size: 13px; color: #666; margin-top: 5px;">Риск получить инфаркт, инсульт или умереть от патологии ССЗ в ближайшие 10 лет.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")
    st.subheader("🔮 Динамика снижения рисков при терапии")

    scenarios = ["Текущий риск"]
    values = [current_risk]
    colors_map = [color]

    if is_smoking:
        scenarios.append("Отказ от табака")
        r_smoke = calculate_score2_risk(age, sex, sbp, t_chol, hdl, False)
        values.append(r_smoke)
        colors_map.append("#3498db")

    if sbp > 120:
        scenarios.append("Контроль АД до 120")
        r_sbp = calculate_score2_risk(age, sex, 120, t_chol, hdl, is_smoking)
        values.append(r_sbp)
        colors_map.append("#9b59b6")

    if is_smoking or sbp > 120:
        scenarios.append("Целевой профиль (АД 120 + не курит)")
        r_ideal = calculate_score2_risk(age, sex, 120, t_chol, hdl, False)
        values.append(r_ideal)
        colors_map.append("#2ecc71")

    fig = go.Figure(
        data=[
            go.Bar(
                x=scenarios,
                y=values,
                marker_color=colors_map,
                text=[f"{v:.1f}%" for v in values],
                textposition="auto",
            )
        ]
    )
    fig.update_layout(
        yaxis_title="Процент риска (%)",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, width="stretch")

st.write("---")
st.subheader("🩺 Выявленные синдромы и патологии (Клинический разбор)")

detected_issues = analyze_pathologies(
    sbp, t_chol, hdl, is_smoking, current_risk, sex
)

if not detected_issues:
    st.success(
        "Критических патологий и явных маркеров ССЗ на основе введенных параметров не обнаружено. Профиль соответствует норме."
    )
else:
    for issue in detected_issues:
        border_color = "#e74c3c" if issue["status"] == "critical" else "#f39c12"
        badge_text = "КРИТИЧЕСКИ" if issue["status"] == "critical" else "ВНИМАНИЕ"

        with st.container():
            st.markdown(
                f"""
                <div style="border: 1px solid {border_color}30; border-left: 4px solid {border_color}; padding: 15px; border-radius: 4px; margin-bottom: 15px; background-color: #fafafa;">
                    <span style="background-color: {border_color}; color: white; padding: 2px 6px; font-size: 10px; font-weight: bold; border-radius: 3px;">{badge_text}</span>
                    <h5 style="margin: 5px 0 2px 0; color: #333;">{issue['title']}</h5>
                    <p style="font-size: 11px; color: #777; margin-bottom: 8px;"><b>Источник протокола:</b> {issue['source']}</p>
                    <p style="font-size: 13px; color: #444; margin-bottom: 10px;"><b>Описание:</b> {issue['desc']}</p>
                    <p style="font-size: 13px; font-weight: bold; margin-bottom: 5px; color: #222;">📋 Пошаговый протокол действий для пациента:</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for step in issue["actions"]:
                st.markdown(f"- {step}")

st.write("---")
st.caption(
    "**⚠️ Важный дисклеймер:** Данное программное обеспечение является демонстрационной математической моделью скрининга ССЗ. Программа не ставит окончательный диагноз и не назначает терапию. Все медицинские решения должны приниматься строго совместно с лечащим врачом."
)