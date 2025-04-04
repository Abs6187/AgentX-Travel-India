import streamlit as st
import os
import json
from datetime import datetime, timedelta
import base64
import pandas as pd
import pydeck as pdk
from travel import (
    destination_research_task, accommodation_task, transportation_task,
    activities_task, dining_task, itinerary_task, chatbot_task,
    run_task
)

# st.set_page_config() must be called before any other Streamlit functions
st.set_page_config(
    page_title="Your AI Agent for Travelling",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# Translation dictionary and helper functions
# ------------------------------------------
translations = {
    "en": {
         "page_title": "Your AI Agent for Travelling",
         "header": "Your AI Agent for Travelling",
         "create_itinerary": "Create Your Itinerary",
         "trip_details": "Trip Details",
         "origin": "Origin",
         "destination": "Destination",
         "travel_dates": "Travel Dates",
         "duration": "Duration (days)",
         "preferences": "Preferences",
         "additional_preferences": "Additional Preferences",
         "interests": "Interests",
         "special_requirements": "Special Requirements",
         "submit": "🚀 Create My Personal Travel Itinerary",
         "request_details": "Your Travel Request",
         "from": "From",
         "when": "When",
         "budget": "Budget",
         "travel_style": "Travel Style",
         "live_agent_outputs": "Live Agent Outputs",
         "full_itinerary": "Full Itinerary",
         "details": "Details",
         "download_share": "Download & Share",
         "save_itinerary": "Save Your Itinerary",
         "plan_another_trip": "🔄 Plan Another Trip",
         "about": "About",
         "how_it_works": "How it works",
         "travel_agents": "Travel Agents",
         "share_itinerary": "Share Your Itinerary",
         "save_for_mobile": "Save for Mobile",
         "built_with": "Built with ❤️ for you",
         # Additional text related to output
         "itinerary_ready": "Your Travel Itinerary is Ready! 🎉",
         "personalized_experience": "We've created a personalized travel experience just for you. Explore your itinerary below.",
         "agent_activity": "Agent Activity",
         "error_origin_destination": "Please enter both origin and destination.",
         "your_itinerary_file": "Your Itinerary File",
         "text_format": "Text format - Can be opened in any text editor"
    },
    "ko": {
         "page_title": "당신의 여행을 위한 AI 에이전트",
         "header": "당신의 여행을 위한 AI 에이전트",
         "create_itinerary": "여행 일정 생성",
         "trip_details": "여행 세부 정보",
         "origin": "출발지",
         "destination": "목적지",
         "travel_dates": "여행 날짜",
         "duration": "기간 (일수)",
         "preferences": "선호사항",
         "additional_preferences": "추가 선호사항",
         "interests": "관심사",
         "special_requirements": "특별 요구사항",
         "submit": "🚀 나만의 여행 일정 생성",
         "request_details": "여행 요청 정보",
         "from": "출발지",
         "when": "여행 기간",
         "budget": "예산",
         "travel_style": "여행 스타일",
         "live_agent_outputs": "실시간 에이전트 결과",
         "full_itinerary": "전체 일정",
         "details": "세부사항",
         "download_share": "다운로드 및 공유",
         "save_itinerary": "일정 저장",
         "plan_another_trip": "🔄 다른 여행 계획",
         "about": "소개",
         "how_it_works": "작동 방식",
         "travel_agents": "여행 에이전트",
         "share_itinerary": "일정 공유",
         "save_for_mobile": "모바일 저장",
         "built_with": "당신을 위해 ❤️ 만들어졌습니다",
         # Additional text related to output
         "itinerary_ready": "여행 일정이 준비되었습니다! 🎉",
         "personalized_experience": "당신만을 위한 맞춤형 여행 경험이 만들어졌습니다. 아래에서 일정을 확인하세요.",
         "agent_activity": "에이전트 활동",
         "error_origin_destination": "출발지와 목적지를 모두 입력하세요.",
         "your_itinerary_file": "당신의 여행 일정 파일",
         "text_format": "텍스트 형식 - 모든 텍스트 편집기에서 열 수 있습니다."
    },
    "ja": {
         "page_title": "あなたの旅行のためのAIエージェント",
         "header": "あなたの旅行のためのAIエージェント",
         "create_itinerary": "旅行プラン作成",
         "trip_details": "旅行詳細",
         "origin": "出発地",
         "destination": "目的地",
         "travel_dates": "旅行日程",
         "duration": "期間（日数）",
         "preferences": "好み",
         "additional_preferences": "追加の好み",
         "interests": "興味",
         "special_requirements": "特別な要件",
         "submit": "🚀 私のための旅行プラン作成",
         "request_details": "旅行リクエスト",
         "from": "出発地",
         "when": "旅行期間",
         "budget": "予算",
         "travel_style": "旅行スタイル",
         "live_agent_outputs": "リアルタイムエージェント出力",
         "full_itinerary": "全行程",
         "details": "詳細",
         "download_share": "ダウンロードと共有",
         "save_itinerary": "旅行プランを保存",
         "plan_another_trip": "🔄 他の旅行を計画",
         "about": "概要",
         "how_it_works": "使い方",
         "travel_agents": "旅行エージェント",
         "share_itinerary": "旅行プランを共有",
         "save_for_mobile": "モバイル保存",
         "built_with": "愛を込めて作られました",
         # Additional text related to output
         "itinerary_ready": "旅行プランの準備ができました！ 🎉",
         "personalized_experience": "あなたのためにパーソナライズされた旅行体験を作成しました。下のプランをご覧ください。",
         "agent_activity": "エージェントアクティビティ",
         "error_origin_destination": "出発地と目的地の両方を入力してください。",
         "your_itinerary_file": "あなたの旅行プランファイル",
         "text_format": "テキスト形式 - 任意のテキストエディタで開けます。"
    },
    "zh": {
         "page_title": "您的旅行 AI 代理",
         "header": "您的旅行 AI 代理",
         "create_itinerary": "创建您的行程",
         "trip_details": "旅行详情",
         "origin": "出发地",
         "destination": "目的地",
         "travel_dates": "旅行日期",
         "duration": "天数",
         "preferences": "偏好",
         "additional_preferences": "其他偏好",
         "interests": "兴趣",
         "special_requirements": "特殊需求",
         "submit": "🚀 创建我的个性化行程",
         "request_details": "您的旅行请求",
         "from": "出发地",
         "when": "旅行时间",
         "budget": "预算",
         "travel_style": "旅行风格",
         "live_agent_outputs": "实时代理输出",
         "full_itinerary": "完整行程",
         "details": "详情",
         "download_share": "下载与分享",
         "save_itinerary": "保存行程",
         "plan_another_trip": "🔄 计划另一趟旅行",
         "about": "关于",
         "how_it_works": "工作原理",
         "travel_agents": "旅行代理",
         "share_itinerary": "分享行程",
         "save_for_mobile": "保存到手机",
         "built_with": "用❤️为您制作",
         # Additional text related to output
         "itinerary_ready": "您的旅行行程已准备就绪！ 🎉",
         "personalized_experience": "我们已为您创建了个性化的旅行体验，请在下方查看您的行程。",
         "agent_activity": "代理活动",
         "error_origin_destination": "请输入出发地和目的地。",
         "your_itinerary_file": "您的行程文件",
         "text_format": "文本格式 - 可在任何文本编辑器中打开。"
    },
    "es": {
         "page_title": " Tu Agente de IA para Viajar",
         "header": " Tu Agente de IA para Viajar",
         "create_itinerary": "Crea Tu Itinerario",
         "trip_details": "Detalles del Viaje",
         "origin": "Origen",
         "destination": "Destino",
         "travel_dates": "Fechas del Viaje",
         "duration": "Duración (días)",
         "preferences": "Preferencias",
         "additional_preferences": "Preferencias Adicionales",
         "interests": "Intereses",
         "special_requirements": "Requisitos Especiales",
         "submit": "🚀 Crea Mi Itinerario Personalizado",
         "request_details": "Tu Solicitud de Viaje",
         "from": "Desde",
         "when": "Cuándo",
         "budget": "Presupuesto",
         "travel_style": "Estilo de Viaje",
         "live_agent_outputs": "Salidas en Vivo del Agente",
         "full_itinerary": "Itinerario Completo",
         "details": "Detalles",
         "download_share": "Descargar y Compartir",
         "save_itinerary": "Guardar Itinerario",
         "plan_another_trip": "🔄 Planear Otro Viaje",
         "about": "Acerca de",
         "how_it_works": "Cómo Funciona",
         "travel_agents": "Agentes de Viaje",
         "share_itinerary": "Compartir Itinerario",
         "save_for_mobile": "Guardar para Móvil",
         "built_with": "Hecho con ❤️ para ti",
         # Additional text related to output
         "itinerary_ready": "¡Tu itinerario de viaje está listo! 🎉",
         "personalized_experience": "Hemos creado una experiencia de viaje personalizada solo para ti. Explora tu itinerario a continuación.",
         "agent_activity": "Actividad del Agente",
         "error_origin_destination": "Por favor, ingresa tanto el origen como el destino.",
         "your_itinerary_file": "Tu Archivo de Itinerario",
         "text_format": "Formato de texto - Se puede abrir en cualquier editor de texto."
    },
    "fr": {
         "page_title": " Votre Agent IA pour Voyager",
         "header": " Votre Agent IA pour Voyager",
         "create_itinerary": "Créez Votre Itinéraire",
         "trip_details": "Détails du Voyage",
         "origin": "Origine",
         "destination": "Destination",
         "travel_dates": "Dates du Voyage",
         "duration": "Durée (jours)",
         "preferences": "Préférences",
         "additional_preferences": "Préférences Supplémentaires",
         "interests": "Centres d'intérêt",
         "special_requirements": "Exigences Spéciales",
         "submit": "🚀 Créez Mon Itinéraire Personnalisé",
         "request_details": "Votre Demande de Voyage",
         "from": "De",
         "when": "Quand",
         "budget": "Budget",
         "travel_style": "Style de Voyage",
         "live_agent_outputs": "Résultats en Direct de l'Agent",
         "full_itinerary": "Itinéraire Complet",
         "details": "Détails",
         "download_share": "Télécharger et Partager",
         "save_itinerary": "Enregistrer l'Itinéraire",
         "plan_another_trip": "🔄 Planifier un Autre Voyage",
         "about": "À Propos",
         "how_it_works": "Fonctionnement",
         "travel_agents": "Agents de Voyage",
         "share_itinerary": "Partager l'Itinéraire",
         "save_for_mobile": "Enregistrer pour Mobile",
         "built_with": "Conçu avec ❤️ pour vous",
         # Additional text related to output
         "itinerary_ready": "Votre itinéraire de voyage est prêt ! 🎉",
         "personalized_experience": "Nous avons créé une expérience de voyage personnalisée rien que pour vous. Découvrez votre itinéraire ci-dessous.",
         "agent_activity": "Activité de l'Agent",
         "error_origin_destination": "Veuillez saisir à la fois le lieu de départ et la destination.",
         "your_itinerary_file": "Votre Fichier d'Itinéraire",
         "text_format": "Format texte - Peut être ouvert dans n'importe quel éditeur de texte."
    },
    "de": {
         "page_title": "Ihr KI-Reiseassistent",
         "header": " Ihr KI-Reiseassistent",
         "create_itinerary": "Erstellen Sie Ihre Reiseroute",
         "trip_details": "Reisedetails",
         "origin": "Abfahrtsort",
         "destination": "Zielort",
         "travel_dates": "Reisedaten",
         "duration": "Dauer (Tage)",
         "preferences": "Vorlieben",
         "additional_preferences": "Zusätzliche Vorlieben",
         "interests": "Interessen",
         "special_requirements": "Besondere Anforderungen",
         "submit": "🚀 Erstellen Sie meine personalisierte Reiseroute",
         "request_details": "Ihre Reiseanfrage",
         "from": "Von",
         "when": "Wann",
         "budget": "Budget",
         "travel_style": "Reisestil",
         "live_agent_outputs": "Live Agent Ausgaben",
         "full_itinerary": "Komplette Reiseroute",
         "details": "Details",
         "download_share": "Herunterladen & Teilen",
         "save_itinerary": "Reiseroute speichern",
         "plan_another_trip": "🔄 Plane eine weitere Reise",
         "about": "Über",
         "how_it_works": "Wie es funktioniert",
         "travel_agents": "Reiseassistenten",
         "share_itinerary": "Reiseroute teilen",
         "save_for_mobile": "Für Mobilgeräte speichern",
         "built_with": "Mit ❤️ für Sie gebaut",
         # Additional text related to output
         "itinerary_ready": "Ihre Reiseroute ist fertig! 🎉",
         "personalized_experience": "Wir haben eine personalisierte Reiseerfahrung nur für Sie erstellt. Entdecken Sie Ihre Reiseroute unten.",
         "agent_activity": "Agentenaktivität",
         "error_origin_destination": "Bitte geben Sie sowohl den Abfahrtsort als auch das Ziel ein.",
         "your_itinerary_file": "Ihre Reise-Datei",
         "text_format": "Textformat – Kann in jedem Texteditor geöffnet werden."
    },
    "ar": {
         "page_title": " وكيل السفر الذكي الخاص بك",
         "header": " وكيل السفر الذكي الخاص بك",
         "create_itinerary": "إنشاء خط سير الرحلة",
         "trip_details": "تفاصيل الرحلة",
         "origin": "المغادرة من",
         "destination": "الوجهة",
         "travel_dates": "تواريخ السفر",
         "duration": "المدة (بالأيام)",
         "preferences": "التفضيلات",
         "additional_preferences": "تفضيلات إضافية",
         "interests": "الاهتمامات",
         "special_requirements": "المتطلبات الخاصة",
         "submit": "🚀 إنشاء خط سير الرحلة الشخصي",
         "request_details": "طلب السفر الخاص بك",
         "from": "من",
         "when": "متى",
         "budget": "الميزانية",
         "travel_style": "أسلوب السفر",
         "live_agent_outputs": "مخرجات الوكيل المباشرة",
         "full_itinerary": "خط سير الرحلة الكامل",
         "details": "التفاصيل",
         "download_share": "تنزيل ومشاركة",
         "save_itinerary": "حفظ خط سير الرحلة",
         "plan_another_trip": "🔄 خطط لرحلة أخرى",
         "about": "حول",
         "how_it_works": "كيف يعمل",
         "travel_agents": "وكلاء السفر",
         "share_itinerary": "شارك خط سير الرحلة",
         "save_for_mobile": "حفظ للهاتف المحمول",
         "built_with": "مصنوع بحب من أجلك",
         # Additional text related to output
         "itinerary_ready": "تم تجهيز خط سير رحلتك! 🎉",
         "personalized_experience": "لقد أنشأنا تجربة سفر مخصصة لك. استعرض خط سير رحلتك أدناه.",
         "agent_activity": "نشاط الوكيل",
         "error_origin_destination": "يرجى إدخال نقطة الانطلاق والوجهة.",
         "your_itinerary_file": "ملف خط سير رحلتك",
         "text_format": "تنسيق نصي - يمكن فتحه في أي محرر نصوص."
    }
}

def t(key):
    lang = st.session_state.get("selected_language", "en")
    return translations[lang].get(key, key)

# ------------------------------------------
# Session initialization
# ------------------------------------------
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "en"  # Default is English

# ------------------------------------------
# Add language selection widget to sidebar
# ------------------------------------------
with st.sidebar:
    language = st.selectbox(
        "Language / 언어 / 言語 / 语言 / Idioma / Langue / Sprache / اللغة",
        ["English", "한국어", "日本語", "中文", "Español", "Français", "Deutsch", "العربية"]
    )
    lang_map = {
        "English": "en",
        "한국어": "ko",
        "日本語": "ja",
        "中文": "zh",
        "Español": "es",
        "Français": "fr",
        "Deutsch": "de",
        "العربية": "ar"
    }
    st.session_state.selected_language = lang_map.get(language, "en")

# ------------------------------------------
# Start of Streamlit UI code
# ------------------------------------------

# Modern CSS with refined color scheme and sleek animations
st.markdown("""
<style>
    /* Sleek Color Palette */
    :root {
        --primary: #3a86ff;
        --primary-light: #4895ef;
        --primary-dark: #2667ff;
        --secondary: #4cc9f0;
        --accent: #4361ee;
        --background: #f8f9fa;
        --card-bg: #ffffff;
        --text: #212529;
        --text-light: #6c757d;
        --text-muted: #adb5bd;
        --border: #e9ecef;
        --success: #2ecc71;
        --warning: #f39c12;
        --info: #3498db;
    }
    
    /* Refined Animations */
    @keyframes smoothFadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .animate-in {
        animation: smoothFadeIn 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    
    .slide-in {
        animation: slideInRight 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    
    /* Sleek Header Styles */
    .main-header {
        font-size: 2.5rem;
        color: var(--primary-dark);
        text-align: center;
        margin-bottom: 0.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.4rem;
        color: var(--accent);
        font-weight: 600;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.4rem;
    }
    
    /* Sleek Card Styles */
    .modern-card {
        background-color: var(--card-bg);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        transition: all 0.25s ease;
        border: 1px solid var(--border);
    }
    
    .modern-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* Refined Form Styles */
    .stTextInput > div > div > input, 
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid var(--border);
        padding: 10px 12px;
        font-size: 14px;
        transition: all 0.2s ease;
        box-shadow: none;
    }
    
    .stTextInput > div > div > input:focus, 
    .stDateInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 1px solid var(--primary);
        box-shadow: 0 0 0 1px rgba(58, 134, 255, 0.15);
    }
    
    /* Sleek Button Styles */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        font-weight: 500;
        padding: 0.5rem 1.2rem;
        border-radius: 6px;
        border: none;
        transition: all 0.2s ease;
        font-size: 14px;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: 0 3px 8px rgba(58, 134, 255, 0.25);
    }
    
    /* Sleek Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--background);
        border-radius: 8px;
        padding: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: white !important;
    }
    
    /* Progress Bar Styles */
    .stProgress > div > div > div > div {
        background-color: var(--primary);
    }
    
    /* Progress Styles */
    .progress-container {
        margin: 1.2rem 0;
        background-color: var(--background);
        border-radius: 8px;
        padding: 0.8rem;
        border: 1px solid var(--border);
    }
    
    .step-complete {
        color: #4CAF50;
        font-weight: 600;
    }
    
    .step-pending {
        color: #9E9E9E;
    }
    
    .step-active {
        color: var(--primary);
        font-weight: 600;
    }
    
    /* Agent Output */
    .agent-output {
        background-color: #f8f9fa;
        border-left: 5px solid var(--primary);
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 10px;
        max-height: 400px;
        overflow-y: auto;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: var(--text-light);
        font-size: 0.9rem;
        padding: 1rem;
        border-top: 1px solid #eaeaea;
    }
    
    /* Agent Log */
    .agent-log {
        background-color: #F5F5F5;
        border-left: 3px solid var(--primary);
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        font-family: monospace;
        border-radius: 4px;
    }
    
    /* Info and Success Boxes */
    .info-box {
        background-color: var(--primary-light);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to download HTML file
def get_download_link(text_content, filename):
    b64 = base64.b64encode(text_content.encode()).decode()
    href = f'<a class="download-link" href="data:text/plain;base64,{b64}" download="{filename}"><i>📥</i> {t("save_itinerary")}</a>'
    return href

# Updated helper function to display modern progress with a single UI element
def display_modern_progress(current_step, total_steps=6):
    if 'progress_steps' not in st.session_state:
        st.session_state.progress_steps = {
            0: {'status': 'pending', 'name': t("trip_details")},
            1: {'status': 'pending', 'name': t("about")},
            2: {'status': 'pending', 'name': t("travel_style")},
            3: {'status': 'pending', 'name': t("live_agent_outputs")},
            4: {'status': 'pending', 'name': t("download_share")},
            5: {'status': 'pending', 'name': t("full_itinerary")}
        }
    
    for i in range(total_steps):
        if i < current_step:
            st.session_state.progress_steps[i]['status'] = 'complete'
        elif i == current_step:
            st.session_state.progress_steps[i]['status'] = 'active'
        else:
            st.session_state.progress_steps[i]['status'] = 'pending'
    
    progress_percentage = (current_step / total_steps) * 100
    st.progress(progress_percentage / 100)
    
    st.markdown("""
    <style>
    .compact-progress {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .progress-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #333;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }
    .step-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    .step-item {
        display: flex;
        align-items: center;
        padding: 8px 10px;
        border-radius: 6px;
        background: #f8f9fa;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .step-item.complete {
        border-left: 3px solid #4CAF50;
        background: #f1f8e9;
    }
    .step-item.active {
        border-left: 3px solid #2196F3;
        background: #e3f2fd;
        font-weight: bold;
    }
    .step-item.pending {
        border-left: 3px solid #9e9e9e;
        opacity: 0.7;
    }
    .step-icon {
        margin-right: 8px;
        font-size: 14px;
    }
    .step-text {
        font-size: 13px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    </style>
    <div class="compact-progress">
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="step-grid">', unsafe_allow_html=True)
    for i, step_info in st.session_state.progress_steps.items():
        status = step_info['status']
        name = step_info['name']
        if status == 'complete':
            icon = "✅"
            status_class = "complete"
        elif status == 'active':
            icon = "🔄"
            status_class = "active"
        else:
            icon = "⭕"
            status_class = "pending"
        
        st.markdown(f"""
        <div class="step-item {status_class}">
            <span class="step-icon">{icon}</span>
            <span class="step-text">{name}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    return progress_percentage

def update_step_status(step_index, status):
    if 'progress_steps' in st.session_state and step_index in st.session_state.progress_steps:
        st.session_state.progress_steps[step_index]['status'] = status

def run_task_with_logs(task, input_text, log_container, output_container, results_key=None):
    log_message = f"🤖 Starting {task.agent.role}..."
    st.session_state.log_messages.append(log_message)
    
    with log_container:
        st.markdown("### " + t("agent_activity"))
        for msg in st.session_state.log_messages:
            st.markdown(msg)
    
    result = run_task(task, input_text)
    
    if results_key:
        st.session_state.results[results_key] = result
    
    log_message = f"✅ {task.agent.role} completed!"
    st.session_state.log_messages.append(log_message)
    
    with log_container:
        st.markdown("### " + t("agent_activity"))
        for msg in st.session_state.log_messages:
            st.markdown(msg)
    
    with output_container:
        st.markdown(f"### {task.agent.role} Output")
        st.markdown("<div class='agent-output'>" + result + "</div>", unsafe_allow_html=True)
    
    return result

# ------------------------------------------
# Session state 초기화
# ------------------------------------------
if 'generated_itinerary' not in st.session_state:
    st.session_state.generated_itinerary = None
if 'generation_complete' not in st.session_state:
    st.session_state.generation_complete = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'results' not in st.session_state:
    st.session_state.results = {
        "destination_info": "",
        "accommodation_info": "",
        "transportation_info": "",
        "activities_info": "",
        "dining_info": "",
        "itinerary": "",
        "final_itinerary": ""
    }
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []
if 'current_output' not in st.session_state:
    st.session_state.current_output = None
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Modern animated header
st.markdown(f"""
<div class="animate-in" style="text-align: center;">
    <div style="margin-bottom: 20px;">
        <img src="https://img.icons8.com/fluency/96/travel-card.png" width="90" style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));">
    </div>
    <h1 class="main-header">{t("header")}</h1>
    <p style="font-size: 1.2rem; color: #6c757d; margin-bottom: 25px;">
        ✨ Create your personalized AI-powered travel itinerary in minutes! ✨
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr style="height:3px;border:none;background-color:#f0f0f0;margin-bottom:25px;">', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; margin-bottom: 20px; border-bottom: 1px solid #eaeaea;">
        <img src="https://img.icons8.com/fluency/96/travel-card.png" width="80" style="margin-bottom: 15px;">
        <h3 style="margin-bottom: 5px; color: #4361ee;">Your AI Agent for Travelling</h3>
        <p style="color: #6c757d; font-size: 0.9rem;">AI-Powered Travel Planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### 🌟 " + t("about"))
    st.info("This AI-powered tool creates a personalized travel itinerary based on your preferences. Fill in the form and let our specialized travel agents plan your perfect trip!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 " + t("how_it_works"))
    st.markdown("""
    <ol style="padding-left: 25px;">
        <li><b>🖊️ Enter</b> your travel details</li>
        <li><b>🧠 AI analysis</b> of your preferences</li>
        <li><b>📋 Generate</b> comprehensive itinerary</li>
        <li><b>📥 Download</b> and enjoy your trip!</li>
    </ol>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Travel Agents")
    agents = [
        ("🔭 Research Specialist", "Finds the best destinations based on your preferences"),
        ("🏨 Accommodation Expert", "Suggests suitable hotels and stays"),
        ("🚆 Transportation Planner", "Plans efficient travel routes"),
        ("🎯 Activities Curator", "Recommends activities tailored to your interests"),
        ("🍽️ Dining Connoisseur", "Finds the best dining experiences"),
        ("📅 Itinerary Creator", "Puts everything together in a daily plan")
    ]
    for name, desc in agents:
        st.markdown("**" + name + "**")
        st.markdown("<small>" + desc + "</small>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.generation_complete:
    st.markdown('<div class="modern-card animate-in">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: 600; color: var(--primary-dark); display: flex; align-items: center; gap: 10px;'><span style='font-size: 20px;'>✈️</span> " + t("create_itinerary") + "</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color: var(--text-light); margin-bottom: 16px; font-size: 14px; font-weight: 400;">Complete the form below for a personalized travel plan.</p>
    """, unsafe_allow_html=True)
    
    with st.form("travel_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p style="font-weight: 500; color: var(--primary); font-size: 14px; margin-bottom: 12px;">Trip Details</p>', unsafe_allow_html=True)
            origin = st.text_input(t("origin"), placeholder="e.g., New York, USA")
            destination = st.text_input(t("destination"), placeholder="e.g., Paris, France")
            st.markdown('<p style="margin-bottom: 5px; font-size: 14px;">Travel Dates</p>', unsafe_allow_html=True)
            start_date = st.date_input("Start Date", min_value=datetime.now(), label_visibility="collapsed")
            duration = st.slider(t("duration"), min_value=1, max_value=30, value=7)
            end_date = start_date + timedelta(days=duration-1)
            st.markdown('<p style="font-size: 13px; color: var(--text-muted); margin-top: 5px;">' + start_date.strftime("%b %d") + " - " + end_date.strftime("%b %d, %Y") + '</p>', unsafe_allow_html=True)
        with col2:
            st.markdown('<p style="font-weight: 500; color: var(--primary); font-size: 14px; margin-bottom: 12px;">Preferences</p>', unsafe_allow_html=True)
            travelers = st.number_input("Travelers", min_value=1, max_value=15, value=2)
            budget_options = ["Budget", "Moderate", "Luxury"]
            budget = st.selectbox("Budget", budget_options, help="Budget: Economy options | Moderate: Mid-range | Luxury: High-end experiences")
            travel_style = st.multiselect("🌈 Travel Style", options=["Culture", "Adventure", "Relaxation", "Food & Dining", "Nature", "Shopping", "Nightlife", "Family-friendly"], default=["Culture", "Food & Dining"])
        with st.expander("Additional Preferences", expanded=False):
            preferences = st.text_area("Interests", placeholder="History museums, local cuisine, hiking, art...")
            special_requirements = st.text_area("Special Requirements", placeholder="Dietary restrictions, accessibility needs...")
        submit_button = st.form_submit_button(t("submit"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submit_button:
        if not origin or not destination:
            st.error(t("error_origin_destination"))
        else:
            st.session_state.form_submitted = True
            user_input = {
                "origin": origin,
                "destination": destination,
                "duration": str(duration),
                "travel_dates": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                "travelers": str(travelers),
                "budget": budget.lower(),
                "travel_style": ", ".join(travel_style),
                "preferences": preferences,
                "special_requirements": special_requirements
            }
            # 기존의 여행 요청 프롬프트
            input_context = f"""Travel Request Details:
Origin: {user_input['origin']}
Destination: {user_input['destination']}
Duration: {user_input['duration']} days
Travel Dates: {user_input['travel_dates']}
Travelers: {user_input['travelers']}
Budget Level: {user_input['budget']}
Travel Style: {user_input['travel_style']}
Preferences/Interests: {user_input['preferences']}
Special Requirements: {user_input['special_requirements']}
"""
            
            llm_language_instructions = {
                "en": "Please output the response in English.",
                "ko": "한국어로 출력해 주세요.",
                "ja": "日本語で出力してください。",
                "zh": "请用中文输出。",
                "es": "Por favor, responda en español.",
                "fr": "Veuillez répondre en français.",
                "de": "Bitte antworten Sie auf Deutsch.",
                "ar": "يرجى الرد باللغة العربية."
            }
            selected_lang = st.session_state.get("selected_language", "en")
            language_instruction = llm_language_instructions.get(selected_lang, "Please output the response in English.")
            modified_input_context = language_instruction + "\n" + input_context
            
            st.markdown("""
            <div class="sleek-processing-container">
              <div class="pulse-container">
                <div class="pulse-ring"></div>
                <div class="pulse-core"></div>
              </div>
            </div>
            <style>
            .sleek-processing-container {
              display: flex;
              justify-content: center;
              align-items: center;
              padding: 20px 0;
            }
            .pulse-container {
              position: relative;
              width: 50px;
              height: 50px;
            }
            .pulse-core {
              position: absolute;
              left: 50%;
              top: 50%;
              transform: translate(-50%, -50%);
              width: 12px;
              height: 12px;
              background-color: #4361ee;
              border-radius: 50%;
              box-shadow: 0 0 8px rgba(67, 97, 238, 0.6);
            }
            .pulse-ring {
              position: absolute;
              left: 0;
              top: 0;
              width: 100%;
              height: 100%;
              border: 2px solid #4361ee;
              border-radius: 50%;
              animation: pulse 1.5s ease-out infinite;
              opacity: 0;
            }
            @keyframes pulse {
              0% { transform: scale(0.1); opacity: 0; }
              50% { opacity: 0.5; }
              100% { transform: scale(1); opacity: 0; }
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            progress_tab, logs_tab, details_tab = st.tabs(["📊 Progress", "🔄 Live Activity", "📋 " + t("request_details")])
            with details_tab:
                st.markdown("#### " + t("request_details"))
                st.markdown("**" + t("destination") + ":** " + user_input['destination'])
                st.markdown("**" + t("from") + ":** " + user_input['origin'])
                st.markdown("**" + t("when") + ":** " + user_input['travel_dates'] + " (" + user_input['duration'] + " days)")
                st.markdown("**" + t("budget") + ":** " + user_input['budget'].title())
                st.markdown("**" + t("travel_style") + ":** " + user_input['travel_style'])
                if user_input['preferences']:
                    st.markdown("**Interests:** " + user_input['preferences'])
                if user_input['special_requirements']:
                    st.markdown("**Special Requirements:** " + user_input['special_requirements'])
            with progress_tab:
                if 'progress_placeholder' not in st.session_state:
                    st.session_state.progress_placeholder = st.empty()
                with st.session_state.progress_placeholder.container():
                    display_modern_progress(0)
            with logs_tab:
                log_container = st.container()
                st.session_state.log_messages = []
            st.markdown('</div>', unsafe_allow_html=True)
            output_container = st.container()
            with output_container:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("### 🌟 " + t("live_agent_outputs"))
                st.info("Our AI agents will show their work here as they create your itinerary")
                st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.current_step = 0
            
            update_step_status(0, 'active')
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            destination_info = run_task_with_logs(
                destination_research_task, 
                modified_input_context.format(destination=user_input['destination'], preferences=user_input['preferences']),
                log_container,
                output_container,
                "destination_info"
            )
            update_step_status(0, 'complete')
            st.session_state.current_step = 1
            update_step_status(1, 'active')
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            accommodation_info = run_task_with_logs(
                accommodation_task, 
                modified_input_context.format(destination=user_input['destination'], budget=user_input['budget'], preferences=user_input['preferences']),
                log_container,
                output_container,
                "accommodation_info"
            )
            update_step_status(1, 'complete')
            st.session_state.current_step = 2
            update_step_status(2, 'active')
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            transportation_info = run_task_with_logs(
                transportation_task, 
                modified_input_context.format(origin=user_input['origin'], destination=user_input['destination']),
                log_container,
                output_container,
                "transportation_info"
            )
            update_step_status(2, 'complete')
            st.session_state.current_step = 3
            update_step_status(3, 'active')
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            activities_info = run_task_with_logs(
                activities_task, 
                modified_input_context.format(destination=user_input['destination'], preferences=user_input['preferences']),
                log_container,
                output_container,
                "activities_info"
            )
            update_step_status(3, 'complete')
            st.session_state.current_step = 4
            update_step_status(4, 'active')
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            dining_info = run_task_with_logs(
                dining_task, 
                modified_input_context.format(destination=user_input['destination'], preferences=user_input['preferences']),
                log_container,
                output_container,
                "dining_info"
            )
            update_step_status(4, 'complete')
            st.session_state.current_step = 5
            update_step_status(5, 'active')
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            combined_info = f"""{input_context}

Destination Information:
{destination_info}

Accommodation Options:
{accommodation_info}

Transportation Plan:
{transportation_info}

Recommended Activities:
{activities_info}

Dining Recommendations:
{dining_info}
"""
            itinerary = run_task_with_logs(
                itinerary_task, 
                combined_info.format(duration=user_input['duration'], origin=user_input['origin'], destination=user_input['destination']),
                log_container,
                output_container,
                "itinerary"
            )
            update_step_status(5, 'complete')
            st.session_state.current_step = 6
            with st.session_state.progress_placeholder.container():
                display_modern_progress(st.session_state.current_step)
            st.session_state.generated_itinerary = itinerary
            st.session_state.generation_complete = True
            date_str = datetime.now().strftime("%Y-%m-%d")
            st.session_state.filename = f"{user_input['destination'].replace(' ', '_')}_{date_str}_itinerary.txt"

if st.session_state.generation_complete:
    st.markdown("""
    <div class="modern-card animate-in">
      <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div class="success-animation">
          <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
            <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" />
            <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" />
          </svg>
        </div>
      </div>
      <h2 style="text-align: center; color: #4361ee;">""" + t("itinerary_ready") + """</h2>
      <p style="text-align: center; color: #6c757d; margin-bottom: 20px;">""" + t("personalized_experience") + """</p>
    </div>
    
    <style>
    .success-animation {
      width: 100px;
      height: 100px;
      position: relative;
    }
    .checkmark {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      display: block;
      stroke-width: 2;
      stroke: #4361ee;
      stroke-miterlimit: 10;
      box-shadow: 0 0 20px rgba(67, 97, 238, 0.3);
      animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
    }
    .checkmark__circle {
      stroke-dasharray: 166;
      stroke-dashoffset: 166;
      stroke-width: 2;
      stroke-miterlimit: 10;
      stroke: #4361ee;
      fill: none;
      animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
    }
    .checkmark__check {
      transform-origin: 50% 50%;
      stroke-dasharray: 48;
      stroke-dashoffset: 48;
      animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
    }
    @keyframes stroke {
      100% { stroke-dashoffset: 0; }
    }
    @keyframes scale {
      0%, 100% { transform: none; }
      50% { transform: scale3d(1.1, 1.1, 1); }
    }
    @keyframes fill {
      100% { box-shadow: 0 0 20px rgba(67, 97, 238, 0.3); }
    }
    </style>
    """, unsafe_allow_html=True)
    
  
    itinerary_tab, details_tab, download_tab, map_tab, chatbot_tab = st.tabs([
        "🗒️ " + t("full_itinerary"), 
        "💼 " + t("details"), 
        "💾 " + t("download_share"),
        "🗺️ 지도 및 시각화",
        "🤖 챗봇 인터페이스"
    ])
    
   
    with itinerary_tab:
        st.text_area("Your Itinerary", st.session_state.generated_itinerary, height=600)

    with details_tab:
        agent_tabs = st.tabs(["🌎 Destination", "🏨 Accommodation", "🚗 Transportation", "🎭 Activities", "🍽️ Dining"])
        with agent_tabs[0]:
            st.markdown("### 🌎 Destination Research")
            st.markdown(st.session_state.results["destination_info"])
        with agent_tabs[1]:
            st.markdown("### 🏨 Accommodation Options")
            st.markdown(st.session_state.results["accommodation_info"])
        with agent_tabs[2]:
            st.markdown("### 🚗 Transportation Plan")
            st.markdown(st.session_state.results["transportation_info"])
        with agent_tabs[3]:
            st.markdown("### 🎭 Recommended Activities")
            st.markdown(st.session_state.results["activities_info"])
        with agent_tabs[4]:
            st.markdown("### 🍽️ Dining Recommendations")
            st.markdown(st.session_state.results["dining_info"])
    
    
    with download_tab:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### " + t("save_itinerary"))
            st.markdown("Download your personalized travel plan to access it offline or share with your travel companions.")
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 20px;">
                <h4 style="margin-top: 0;">""" + t("your_itinerary_file") + """</h4>
                <p style="font-size: 0.9rem; color: #6c757d;">""" + t("text_format") + """</p>
            """, unsafe_allow_html=True)
            st.markdown("<div style='margin: 10px 0;'>" + get_download_link(st.session_state.generated_itinerary, st.session_state.filename) + "</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("### " + t("share_itinerary"))
            st.markdown("*Coming soon: Email your itinerary or share via social media.*")
        with col2:
            st.markdown("### " + t("save_for_mobile"))
            st.markdown("*Coming soon: QR code for easy access on your phone*")
    
 
    with map_tab:
        st.markdown("### Destination Map")
        # Example: Coordinate data for major attractions near destination (can be dynamically fetched via API or DB)
        map_data = pd.DataFrame({
            "lat": [48.8584, 48.8606, 48.8529],
            "lon": [2.2945, 2.3376, 2.3500],
            "name": ["Eiffel Tower", "Louvre Museum", "Notre Dame"]
        })
        # Default map output (st.map)
        st.map(map_data)
        
        st.markdown("#### Interactive Map with Pydeck")
        view_state = pdk.ViewState(
            latitude=48.8584,
            longitude=2.2945,
            zoom=12,
            pitch=50
        )
        
        # AI Chatbot interface tab (using Gemini)
        with chatbot_tab:
            st.markdown("### AI Chatbot Interface")
            # Store conversation history in session state (message, sender, timestamp)
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # User input field and send button
            user_question = st.text_input("Ask me about your travel plans:", key="chat_input")
            
            # Gemini-based chatbot response: use run_task() to query chatbot_task
            if user_question and st.button("Ask", key="ask_button"):
                response = run_task(chatbot_task, user_question)
                st.session_state.messages.append({
                    "speaker": "User",
                    "message": user_question,
                    "time": datetime.now()
                })
                st.session_state.messages.append({
                    "speaker": "AI",
                    "message": response,
                    "time": datetime.now()
                })
            
            # Conversation history output (including timestamp, scrollable area)
            st.markdown("<div style='max-height:400px; overflow-y:auto; padding:10px; border:1px solid #eaeaea; border-radius:6px;'>", unsafe_allow_html=True)
            for chat in st.session_state.messages:
                time_str = chat["time"].strftime("%H:%M:%S")
                st.markdown(f"**{chat['speaker']}** ({time_str}): {chat['message']}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 50px; text-align: center; padding: 20px; color: #6c757d; font-size: 0.8rem;">
        <p>""" + t("built_with") + """</p>
    </div>
    """, unsafe_allow_html=True)
