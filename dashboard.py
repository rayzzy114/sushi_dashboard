import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from pathlib import Path

# Настройка страницы
st.set_page_config(
    page_title="Анализ рынка суши-ресторанов в Омске",
    page_icon="🍣",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_font_setup():
    """Определяет какой шрифт использовать"""
    # Проверяем наличие файлов шрифтов
    font_dir = Path("assets/fonts")
    has_custom_fonts = False
    
    if font_dir.exists():
        woff2_files = list(font_dir.glob("*.woff2"))
        if woff2_files:
            has_custom_fonts = True
    
    if has_custom_fonts:
        # Используем кастомный шрифт через статические файлы
        font_css = """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        """
        font_family = "Inter"
        font_status = "Inter (Google Fonts) + статические файлы готовы"
    else:
        # Используем Google Fonts как основной вариант
        font_css = """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        """
        font_family = "Inter"
        font_status = "Inter (Google Fonts)"
    
    return font_css, font_family, font_status

# Получаем настройки шрифта
font_css, font_family, font_status = get_font_setup()

# Цветовая палитра Streamlit
STREAMLIT_COLORS = {
    'primary': '#1E3A8A',      # темно-синий
    'secondary': '#3B82F6',    # синий
    'success': '#10B981',      # зеленый
    'warning': '#F59E0B',      # оранжевый
    'info': '#6366F1',         # индиго
    'purple': '#8B5CF6',       # фиолетовый
    'dark': '#FF7F50',         # темно-серый
    'light': '#F3F4F6',        # светло-серый
    'accent': '#DC2626'        # красный
}

# Стили CSS для красивого дизайна
st.markdown(f"""
{font_css}
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {{
        --primary-color: {STREAMLIT_COLORS['primary']};
        --secondary-color: {STREAMLIT_COLORS['secondary']};
        --text-color: {STREAMLIT_COLORS['dark']};
        --bg-light: {STREAMLIT_COLORS['light']};
    }}
    
    * {{
        font-family: "{font_family}", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif !important;
    }}
    
    .main-header {{
        font-size: 3.5rem;
        background: linear-gradient(45deg, {STREAMLIT_COLORS['primary']}, {STREAMLIT_COLORS['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        font-family: "{font_family}", sans-serif !important;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid var(--primary-color);
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.1);
        font-family: "{font_family}", sans-serif !important;
        transition: transform 0.2s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(30, 58, 138, 0.15);
    }}
    
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
        font-family: "{font_family}", sans-serif !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
        font-family: "{font_family}", sans-serif !important;
        font-weight: 600;
        font-size: 18px;
        color: #FF8A65;
    }}
    
    .stTabs [data-baseweb="tab-list"] button {{
        background-color: transparent;
        border-radius: 10px 10px 0 0;
        border: none;
        padding: 12px 20px;
        margin-right: 4px;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab-list"] button:hover {{
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.1), rgba(59, 130, 246, 0.1));
        transform: translateY(-2px);
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background: linear-gradient(135deg, {STREAMLIT_COLORS['primary']}, {STREAMLIT_COLORS['secondary']});
        color: white !important;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {{
        color: white !important;
        font-weight: 700;
    }}
    
    .stSelectbox label, .stCheckbox label, .stRadio label {{
        font-family: "{font_family}", sans-serif !important;
        font-weight: 500;
        color: #1F2937;
    }}
    
    .stDataFrame, .stTable {{
        font-family: "{font_family}", sans-serif !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: "{font_family}", sans-serif !important;
        font-weight: 600;
        color: #FF8A65;
    }}
    
    .stMetric {{
        font-family: "{font_family}", sans-serif !important;
    }}
    
    .stMetric > div > div > div > div {{
        font-size: 1.2rem;
        font-weight: 600;
    }}
    
    .stInfo, .stSuccess, .stWarning, .stError {{
        font-family: "{font_family}", sans-serif !important;
        border-radius: 10px;
    }}
    
    .element-container {{
        font-family: "{font_family}", sans-serif !important;
    }}
    
    /* Кастомизация графиков */
    .js-plotly-plot .plotly .main-svg {{
        border-radius: 10px;
    }}
    
    /* Анимации */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .element-container {{
        animation: fadeIn 0.5s ease-out;
    }}
</style>
""", unsafe_allow_html=True)

def get_streamlit_layout():
    """Настройки для всех графиков в стиле Streamlit"""
    return {
        'font': dict(size=16, family=f'"{font_family}", Arial, sans-serif'),
        'title_font': dict(size=24, family=f'"{font_family}", Arial, sans-serif', color="#FF8A65"),
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'margin': dict(l=60, r=60, t=100, b=60),
        'hoverlabel': dict(
            bgcolor="white",
            bordercolor=STREAMLIT_COLORS['primary'],
            font_size=14, 
            font_family=f'"{font_family}", Arial, sans-serif',
            font_color="black"
        ),
        'colorway': list(STREAMLIT_COLORS.values())
    }

@st.cache_data
def load_data():
    """Загрузка данных из Excel файлов"""
    try:
        # Основные данные по рынку суши
        df_market = pd.read_excel('данные по рынку суши.xlsx')
        
        # Данные профиля потребителей
        df_profile = pd.read_excel('профиль_потребителя.xlsx')
        
        # Очищаем данные от Excel ошибок
        df_market = clean_excel_errors(df_market)
        df_profile = clean_excel_errors(df_profile)
        
        return df_market, df_profile
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        return None, None

def clean_excel_errors(df):
    """Очищает данные от Excel ошибок типа #REF!, #N/A, #VALUE! и т.д."""
    df_clean = df.copy()
    
    # Список Excel ошибок для удаления
    excel_errors = ['#REF!', '#N/A', '#VALUE!', '#DIV/0!', '#NUM!', '#NAME?', '#NULL!']
    
    for col in df_clean.columns:
        # Заменяем Excel ошибки на NaN
        for error in excel_errors:
            df_clean[col] = df_clean[col].replace(error, np.nan)
            # Также проверяем строковые представления
            mask = df_clean[col].astype(str).str.contains(error, na=False)
            if mask.any():
                df_clean.loc[mask, col] = np.nan
    
    return df_clean

def create_custom_chart(fig, title_color=None):
    """Применяет кастомные настройки к графику"""
    layout_settings = get_streamlit_layout()
    if title_color:
        layout_settings['title_font']['color'] = title_color
    
    fig.update_layout(**layout_settings)
    
    # Добавляем красивые границы и тени
    fig.update_layout(
        showlegend=True,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(family=f'"{font_family}", Arial, sans-serif', size=12)
        )
    )
    
    return fig

def main():
    # Заголовок с анимацией
    st.markdown('<h1 class="main-header">🍣 Анализ рынка суши-ресторанов в Омске</h1>', unsafe_allow_html=True)
    
    # Информация о шрифте
    st.sidebar.markdown(f"**🎨 Шрифт:** {font_status}")
    
    # Загрузка данных
    df_market, df_profile = load_data()
    
    if df_market is None or df_profile is None:
        st.error("Не удалось загрузить данные. Проверьте наличие файлов 'данные по рынку суши.xlsx' и 'профиль_потребителя.xlsx'")
        return
    
    # Боковая панель с фильтрами
    st.sidebar.markdown("## 🎛️ Настройки дашборда")
    
    # Цветовая схема
    color_scheme = st.sidebar.selectbox(
        "🎨 Цветовая схема:",
        ["Яркая (по умолчанию)", "Пастельная", "Монохром", "Морская"],
        index=0
    )
    
    # Обновляем цвета в зависимости от выбора
    if color_scheme == "Пастельная":
        STREAMLIT_COLORS.update({
            'primary': '#FFB5B5', 'secondary': '#B5E7E1', 'success': '#B5D3F0'
        })
    elif color_scheme == "Монохром":
        STREAMLIT_COLORS.update({
            'primary': '#555555', 'secondary': '#777777', 'success': '#999999'
        })
    elif color_scheme == "Морская":
        STREAMLIT_COLORS.update({
            'primary': '#006A6B', 'secondary': '#00A8CC', 'success': '#40E0D0'
        })
    
    # Показать сырые данные
    if st.sidebar.checkbox("📊 Показать исходные данные"):
        with st.expander("📋 Таблица данных - Рынок суши", expanded=False):
            st.dataframe(df_market, use_container_width=True)
        with st.expander("📋 Таблица данных - Профиль потребителей", expanded=False):
            st.dataframe(df_profile, use_container_width=True)
    
    # Отладочная информация
    if st.sidebar.checkbox("🔍 Показать структуру данных"):
        with st.expander("🗂️ Названия колонок - Рынок суши", expanded=False):
            for i, col in enumerate(df_market.columns):
                st.write(f"`{i}:` {col}")
        with st.expander("🗂️ Названия колонок - Профиль потребителей", expanded=False):
            for i, col in enumerate(df_profile.columns):
                st.write(f"`{i}:` {col}")
    
    # Основные метрики с красивыми карточками
    st.markdown("### 🎨 Ключевые показатели рынка")
    
    # Вычисляем реальные показатели из данных
    top_restaurant = ""
    avg_satisfaction = 0
    top_purpose = ""
    
    # Находим самый популярный ресторан
    if 'Какой суши-ресторан  посещают чаще всего' in df_market.columns and 'кол-во.3' in df_market.columns:
        popular_data = df_market[['Какой суши-ресторан  посещают чаще всего', 'кол-во.3']].dropna()
        if not popular_data.empty:
            top_restaurant = popular_data.loc[popular_data['кол-во.3'].idxmax(), 'Какой суши-ресторан  посещают чаще всего']
    
    # Находим среднюю удовлетворенность (исправляем на формат x/5)
    satisfaction_cols = [col for col in df_market.columns if 'балл' in col]
    if satisfaction_cols:
        avg_satisfaction = df_market[satisfaction_cols[0]].mean()
        # Преобразуем из 10-балльной в 5-балльную систему
        if avg_satisfaction > 5:
            avg_satisfaction = avg_satisfaction / 2
    
    # Находим топ цель посещения
    if 'цель посещения' in df_market.columns and 'кол-во' in df_market.columns:
        purpose_data = df_market[['цель посещения', 'кол-во']].dropna()
        if not purpose_data.empty:
            top_purpose = purpose_data.loc[purpose_data['кол-во'].idxmax(), 'цель посещения']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            transform: translateY(0);
            transition: all 0.3s ease;
            border: none;
            position: relative;
            overflow: hidden;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏆</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem;">Лидер рынка</div>
            <div style="font-size: 1.2rem; opacity: 0.9; font-weight: 500;">{top_restaurant if top_restaurant else "Анализируем..."}</div>
            <div style="position: absolute; top: -20px; right: -20px; width: 60px; height: 60px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
            transform: translateY(0);
            transition: all 0.3s ease;
            border: none;
            position: relative;
            overflow: hidden;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">⭐</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem;">Средняя оценка</div>
            <div style="font-size: 1.2rem; opacity: 0.9; font-weight: 500;">{f"{avg_satisfaction:.1f}/5" if avg_satisfaction > 0 else "Анализируем..."}</div>
            <div style="position: absolute; top: -20px; right: -20px; width: 60px; height: 60px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3);
            transform: translateY(0);
            transition: all 0.3s ease;
            border: none;
            position: relative;
            overflow: hidden;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem;">Топ цель</div>
            <div style="font-size: 1.2rem; opacity: 0.9; font-weight: 500;">{top_purpose if top_purpose else "Определяем..."}</div>
            <div style="position: absolute; top: -20px; right: -20px; width: 60px; height: 60px; background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Добавляем CSS для hover эффектов
    st.markdown("""
    <style>
    div[style*="background: linear-gradient"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Вкладки для разных анализов
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Посещаемость", 
        "🏪 Рестораны", 
        "💰 Ценообразование", 
        "📈 Удовлетворенность",
        "👥 Профиль потребителей"
    ])
    
    with tab1:
        st.markdown("### 🎯 Анализ посещаемости суши-ресторанов")
        
        col1_tab1, col2_tab1 = st.columns(2)
        
        with col1_tab1:
            # График целей посещения
            if 'цель посещения' in df_market.columns and 'кол-во' in df_market.columns:
                purpose_data = df_market[['цель посещения', 'кол-во']].dropna()
                if not purpose_data.empty:
                    fig_purpose = px.pie(
                        purpose_data, 
                        values='кол-во', 
                        names='цель посещения',
                        title="🎯 Цели посещения суши-ресторанов",
                        color_discrete_sequence=[STREAMLIT_COLORS['primary'], STREAMLIT_COLORS['secondary'], STREAMLIT_COLORS['success']]
                    )
                    fig_purpose.update_traces(
                        textposition='inside', 
                        textinfo='percent+label', 
                        textfont_size=15,
                        hovertemplate='<b>%{label}</b><br>Количество: %{value}<br>Процент: %{percent}<extra></extra>'
                    )
                    fig_purpose = create_custom_chart(fig_purpose)
                    st.plotly_chart(fig_purpose, use_container_width=True)
        
        with col2_tab1:
            # График частоты посещений
            if 'Как часто посещают суши-рестораны' in df_market.columns:
                frequency_col = df_market.columns[df_market.columns.str.contains('кол-во')][1] if len(df_market.columns[df_market.columns.str.contains('кол-во')]) > 1 else 'кол-во'
                frequency_data = df_market[['Как часто посещают суши-рестораны', frequency_col]].dropna()
                if not frequency_data.empty:
                    fig_freq = px.bar(
                        frequency_data,
                        x='Как часто посещают суши-рестораны',
                        y=frequency_col,
                        title="📊 Частота посещения суши-ресторанов",
                        color_discrete_sequence=[STREAMLIT_COLORS['info']]
                    )
                    fig_freq.update_layout(
                        xaxis_tickangle=-45,
                        xaxis_title="Частота посещений",
                        yaxis_title="Количество респондентов"
                    )
                    fig_freq.update_traces(
                        hovertemplate='<b>%{x}</b><br>Количество: %{y}<extra></extra>'
                    )
                    fig_freq = create_custom_chart(fig_freq)
                    st.plotly_chart(fig_freq, use_container_width=True)
    
    with tab2:
        st.markdown("### 🏪 Анализ знания и посещения ресторанов")
        
        col1_tab2, col2_tab2 = st.columns(2)
        
        with col1_tab2:
            # Топ известных ресторанов
            if 'Какие суши-рестораны в г. Омск  знают' in df_market.columns and 'кол-во.1' in df_market.columns:
                known_data = df_market[['Какие суши-рестораны в г. Омск  знают', 'кол-во.1']].dropna()
                if not known_data.empty:
                    known_data = known_data.sort_values('кол-во.1', ascending=True)
                    fig_known = px.bar(
                        known_data,
                        x='кол-во.1',
                        y='Какие суши-рестораны в г. Омск  знают',
                        orientation='h',
                        title="🏆 Известность суши-ресторанов в Омске",
                        color='кол-во.1',
                        color_continuous_scale=[[0, STREAMLIT_COLORS['warning']], [1, STREAMLIT_COLORS['secondary']]]
                    )
                    fig_known.update_layout(
                        xaxis_title="Количество упоминаний",
                        yaxis_title="Рестораны"
                    )
                    fig_known = create_custom_chart(fig_known)
                    st.plotly_chart(fig_known, use_container_width=True)
        
        with col2_tab2:
            # Фактическое посещение
            if 'В какие суши-рестораны в г. Омск бычно ходят' in df_market.columns and 'кол-во.2' in df_market.columns:
                visit_data = df_market[['В какие суши-рестораны в г. Омск бычно ходят', 'кол-во.2']].dropna()
                if not visit_data.empty:
                    visit_data = visit_data.sort_values('кол-во.2', ascending=False)
                    fig_visit = px.pie(
                        visit_data,
                        values='кол-во.2',
                        names='В какие суши-рестораны в г. Омск бычно ходят',
                        title="🍽️ Фактическое посещение ресторанов",
                        color_discrete_sequence=[STREAMLIT_COLORS['success'], STREAMLIT_COLORS['purple'], STREAMLIT_COLORS['warning'], STREAMLIT_COLORS['info']]
                    )
                    fig_visit.update_traces(
                        textposition='inside', 
                        textinfo='percent+label', 
                        textfont_size=15,
                        hovertemplate='<b>%{label}</b><br>Посещений: %{value}<br>Процент: %{percent}<extra></extra>'
                    )
                    fig_visit = create_custom_chart(fig_visit)
                    st.plotly_chart(fig_visit, use_container_width=True)
        
        # Самые популярные рестораны
        if 'Какой суши-ресторан  посещают чаще всего' in df_market.columns and 'кол-во.3' in df_market.columns:
            popular_data = df_market[['Какой суши-ресторан  посещают чаще всего', 'кол-во.3']].dropna()
            if not popular_data.empty:
                fig_popular = px.treemap(
                    popular_data,
                    path=['Какой суши-ресторан  посещают чаще всего'],
                    values='кол-во.3',
                    title="🌟 Самые часто посещаемые рестораны",
                    color='кол-во.3',
                    color_continuous_scale=[[0, STREAMLIT_COLORS['light']], [0.5, STREAMLIT_COLORS['primary']], [1, STREAMLIT_COLORS['dark']]]
                )
                fig_popular = create_custom_chart(fig_popular)
                st.plotly_chart(fig_popular, use_container_width=True)
    
    with tab3:
        st.markdown("### 💰 Анализ ценообразования")
        
        # Поиск колонок с ценами
        price_columns = []
        for col in df_market.columns:
            if any(word in col.lower() for word in ['цена', 'цены', 'стоимость', 'руб']):
                price_columns.append(col)
        
        if price_columns:
            st.info(f"📊 Найденные колонки с ценами: {', '.join(price_columns[:3])}...")
            
            # Анализируем количество данных в каждой ценовой колонке
            st.markdown("#### 📈 Статистика по ценовым данным")
            price_stats = {}
            for col in price_columns:
                non_null_count = df_market[col].count()
                price_stats[col] = non_null_count
                
            # Показываем статистику
            stats_df = pd.DataFrame([
                {"Колонка": col, "Количество ответов": count} 
                for col, count in price_stats.items()
            ])
            st.dataframe(stats_df, use_container_width=True)
            
            col1_tab3, col2_tab3 = st.columns(2)
            
            # Ищем конкретные колонки по ключевым словам
            max_price_cols = [col for col in df_market.columns if 'выше' in col.lower() and 'цен' in col.lower()]
            min_price_cols = [col for col in df_market.columns if 'ниже' in col.lower() and 'цен' in col.lower()]
            fair_price_cols = [col for col in df_market.columns if 'справедлив' in col.lower() and 'цен' in col.lower()]
            
            with col1_tab3:
                if max_price_cols:
                    max_price_data = df_market[max_price_cols[0]].dropna()
                    if len(max_price_data) >= 3:  # Минимум 3 значения для графика
                        fig_max_price = px.histogram(
                            x=max_price_data,
                            title="💸 Максимальная приемлемая цена",
                            nbins=min(10, len(max_price_data)),
                            color_discrete_sequence=[STREAMLIT_COLORS['primary']]
                        )
                        fig_max_price.update_layout(
                            xaxis_title="Цена (руб.)",
                            yaxis_title="Количество респондентов",
                            bargap=0.1
                        )
                        fig_max_price = create_custom_chart(fig_max_price)
                        st.plotly_chart(fig_max_price, use_container_width=True)
                        
                        # Показываем статистику
                        st.markdown(f"**📊 Статистика по максимальной цене:**")
                        st.write(f"• Респондентов: {len(max_price_data)}")
                        st.write(f"• Средняя цена: {max_price_data.mean():.0f} ₽")
                        st.write(f"• Диапазон: {max_price_data.min():.0f} - {max_price_data.max():.0f} ₽")
                    else:
                        st.warning(f"⚠️ Недостаточно данных для максимальной цены (только {len(max_price_data)} ответов)")
                else:
                    st.info("💭 Данные о максимальной цене не найдены")
            
            with col2_tab3:
                if min_price_cols:
                    min_price_data = df_market[min_price_cols[0]].dropna()
                    if len(min_price_data) >= 3:  # Минимум 3 значения для графика
                        fig_min_price = px.histogram(
                            x=min_price_data,
                            title="✨ Минимальная цена для качества",
                            nbins=min(10, len(min_price_data)),
                            color_discrete_sequence=[STREAMLIT_COLORS['success']]
                        )
                        fig_min_price.update_layout(
                            xaxis_title="Цена (руб.)",
                            yaxis_title="Количество респондентов",
                            bargap=0.1
                        )
                        fig_min_price = create_custom_chart(fig_min_price)
                        st.plotly_chart(fig_min_price, use_container_width=True)
                        
                        # Показываем статистику  
                        st.markdown(f"**📊 Статистика по минимальной цене:**")
                        st.write(f"• Респондентов: {len(min_price_data)}")
                        st.write(f"• Средняя цена: {min_price_data.mean():.0f} ₽")
                        st.write(f"• Диапазон: {min_price_data.min():.0f} - {min_price_data.max():.0f} ₽")
                    else:
                        st.warning(f"⚠️ Недостаточно данных для минимальной цены (только {len(min_price_data)} ответов)")
                else:
                    st.info("💭 Данные о минимальной цене не найдены")
            
            # Справедливая цена
            if fair_price_cols:
                fair_price_data = df_market[fair_price_cols[0]].dropna()
                if len(fair_price_data) >= 3:
                    fig_fair_price = px.box(
                        y=fair_price_data,
                        title="⚖️ Распределение справедливой цены",
                        color_discrete_sequence=[STREAMLIT_COLORS['secondary']]
                    )
                    fig_fair_price.update_layout(yaxis_title="Цена (руб.)")
                    fig_fair_price = create_custom_chart(fig_fair_price)
                    st.plotly_chart(fig_fair_price, use_container_width=True)
                    
                    # Дополнительная статистика
                    col_stats1, col_stats2, col_stats3 = st.columns(3)
                    with col_stats1:
                        st.metric("Респондентов", len(fair_price_data))
                    with col_stats2:
                        st.metric("Средняя цена", f"{fair_price_data.mean():.0f} ₽")
                    with col_stats3:
                        st.metric("Медианная цена", f"{fair_price_data.median():.0f} ₽")
                else:
                    st.warning(f"⚠️ Недостаточно данных для справедливой цены (только {len(fair_price_data)} ответов)")
            
            # Общий анализ всех ценовых колонок
            if price_columns:
                st.markdown("#### 📈 Сравнительный анализ цен")
                numeric_price_cols = df_market[price_columns].select_dtypes(include=[np.number]).columns
                if len(numeric_price_cols) > 0:
                    price_data = df_market[numeric_price_cols].describe().round(2)
                    st.dataframe(price_data, use_container_width=True)
                    
                    # Предупреждение о малом количестве данных
                    low_data_cols = [col for col in numeric_price_cols if df_market[col].count() < 10]
                    if low_data_cols:
                        st.warning(f"⚠️ **Внимание:** В следующих колонках мало данных (менее 10 ответов): {', '.join(low_data_cols)}")
                        st.info("💡 **Рекомендация:** Необходимо собрать больше данных для более точного анализа ценообразования.")
        else:
            st.warning("🔍 Не найдены колонки с ценовыми данными. Проверьте структуру файла.")
    
    with tab4:
        st.markdown("### 📈 Анализ удовлетворенности")
        
        # Поиск колонок с удовлетворенностью
        satisfaction_columns = []
        for col in df_market.columns:
            if any(word in col.lower() for word in ['удовлетвор', 'оценк', 'балл', 'рейтинг']):
                satisfaction_columns.append(col)
        
        if satisfaction_columns:
            st.info(f"📊 Найденные колонки с оценками: {', '.join(satisfaction_columns[:3])}...")
            
            col1_tab4, col2_tab4 = st.columns(2)
            
            # Поиск конкретных колонок
            general_satisfaction_cols = [col for col in df_market.columns if 'удовлетворены суши-рестораном' in col]
            characteristics_cols = [col for col in df_market.columns if 'характеристик' in col.lower()]
            importance_cols = [col for col in df_market.columns if 'важность' in col.lower()]
            
            with col1_tab4:
                if general_satisfaction_cols and any('кол-во' in col for col in df_market.columns):
                    count_col = [col for col in df_market.columns if 'кол-во.4' in col]
                    if count_col:
                        satisfaction_data = df_market[[general_satisfaction_cols[0], count_col[0]]].dropna()
                        if not satisfaction_data.empty:
                            fig_satisfaction = px.bar(
                                satisfaction_data,
                                x=general_satisfaction_cols[0],
                                y=count_col[0],
                                title="😊 Общая удовлетворенность",
                                color_discrete_sequence=[STREAMLIT_COLORS['success']]
                            )
                            fig_satisfaction.update_layout(
                                xaxis_tickangle=-45,
                                xaxis_title="Уровень удовлетворенности",
                                yaxis_title="Количество респондентов"
                            )
                            fig_satisfaction = create_custom_chart(fig_satisfaction)
                            st.plotly_chart(fig_satisfaction, use_container_width=True)
                else:
                    st.info("💭 Данные об общей удовлетворенности не найдены")
            
            with col2_tab4:
                if characteristics_cols and 'балл' in df_market.columns:
                    char_data = df_market[[characteristics_cols[0], 'балл']].dropna()
                    if not char_data.empty:
                        fig_char = px.scatter(
                            char_data,
                            x=characteristics_cols[0],
                            y='балл',
                            title="⭐ Оценка характеристик",
                            size='балл',
                            color='балл',
                            color_continuous_scale=[[0, STREAMLIT_COLORS['warning']], [1, STREAMLIT_COLORS['primary']]]
                        )
                        fig_char.update_layout(
                            xaxis_tickangle=-45,
                            xaxis_title="Характеристики",
                            yaxis_title="Оценка (балл)"
                        )
                        fig_char = create_custom_chart(fig_char)
                        st.plotly_chart(fig_char, use_container_width=True)
                else:
                    st.info("💭 Данные об оценке характеристик не найдены")
            
            # Важность характеристик
            if importance_cols and '%' in df_market.columns:
                importance_data = df_market[[importance_cols[0], '%']].dropna()
                if not importance_data.empty:
                    fig_importance = px.bar(
                        importance_data,
                        x='%',
                        y=importance_cols[0],
                        orientation='h',
                        title="🎯 Важность характеристик (%)",
                        color='%',
                        color_continuous_scale=[[0, STREAMLIT_COLORS['light']], [1, STREAMLIT_COLORS['info']]]
                    )
                    fig_importance.update_layout(
                        xaxis_title="Важность (%)",
                        yaxis_title="Характеристики"
                    )
                    fig_importance = create_custom_chart(fig_importance)
                    st.plotly_chart(fig_importance, use_container_width=True)
            
            # Общий анализ всех колонок с оценками
            if satisfaction_columns:
                st.markdown("#### 📊 Статистика по всем оценкам")
                numeric_satisfaction = df_market[satisfaction_columns].select_dtypes(include=[np.number])
                if not numeric_satisfaction.empty:
                    satisfaction_stats = numeric_satisfaction.describe().round(2)
                    st.dataframe(satisfaction_stats, use_container_width=True)
        else:
            st.warning("🔍 Не найдены колонки с данными об удовлетворенности.")
    
    with tab5:
        st.markdown("### 👥 Профиль потребителей суши-ресторанов")
        
        col1_tab5, col2_tab5 = st.columns(2)
        
        with col1_tab5:
            # Анализ по полу
            if 'пол' in df_profile.columns:
                gender_data = df_profile['пол'].value_counts()
                fig_gender = px.pie(
                    values=gender_data.values,
                    names=gender_data.index,
                    title="👥 Распределение по полу",
                    color_discrete_sequence=[STREAMLIT_COLORS['primary'], STREAMLIT_COLORS['secondary']]
                )
                fig_gender.update_traces(
                    textposition='inside', 
                    textinfo='percent+label', 
                    textfont_size=15,
                    hovertemplate='<b>%{label}</b><br>Количество: %{value}<br>Процент: %{percent}<extra></extra>'
                )
                fig_gender = create_custom_chart(fig_gender)
                st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2_tab5:
            # Анализ по возрасту
            if 'возраст' in df_profile.columns:
                age_data = df_profile['возраст'].value_counts()
                fig_age = px.bar(
                    x=age_data.index,
                    y=age_data.values,
                    title="🎂 Распределение по возрастам",
                    color_discrete_sequence=[STREAMLIT_COLORS['info']]
                )
                fig_age.update_layout(
                    xaxis_title="Возрастная группа",
                    yaxis_title="Количество респондентов"
                )
                fig_age.update_traces(
                    hovertemplate='<b>%{x}</b><br>Количество: %{y}<extra></extra>'
                )
                fig_age = create_custom_chart(fig_age)
                st.plotly_chart(fig_age, use_container_width=True)
        
        col3_tab5, col4_tab5 = st.columns(2)
        
        with col3_tab5:
            # Анализ по доходу
            if 'доход' in df_profile.columns:
                income_data = df_profile['доход'].value_counts()
                fig_income = px.pie(
                    values=income_data.values,
                    names=income_data.index,
                    title="💰 Распределение по доходу",
                    color_discrete_sequence=[STREAMLIT_COLORS['success'], STREAMLIT_COLORS['warning'], STREAMLIT_COLORS['purple'], STREAMLIT_COLORS['accent']]
                )
                fig_income.update_traces(
                    textposition='inside', 
                    textinfo='percent+label', 
                    textfont_size=12,
                    hovertemplate='<b>%{label}</b><br>Количество: %{value}<br>Процент: %{percent}<extra></extra>'
                )
                fig_income = create_custom_chart(fig_income)
                st.plotly_chart(fig_income, use_container_width=True)
        
        with col4_tab5:
            # Топ любимых суши/роллов
            if 'Какие суши\\роллы  любят больше всего' in df_profile.columns:
                # Разбираем данные по любимым суши/роллам
                sushi_data = df_profile['Какие суши\\роллы  любят больше всего'].dropna()
                
                # Создаем список всех упомянутых суши/роллов
                all_sushi = []
                for entry in sushi_data:
                    if isinstance(entry, str):
                        # Разделяем по запятым и очищаем
                        sushi_list = [s.strip().lower() for s in entry.split(',')]
                        all_sushi.extend(sushi_list)
                
                # Подсчитываем частоту
                from collections import Counter
                sushi_counts = Counter(all_sushi)
                
                # Берем топ-10
                top_sushi = dict(sushi_counts.most_common(10))
                
                if top_sushi:
                    fig_sushi = px.bar(
                        x=list(top_sushi.values()),
                        y=list(top_sushi.keys()),
                        orientation='h',
                        title="🍣 Топ-10 любимых суши/роллов",
                        color=list(top_sushi.values()),
                        color_continuous_scale=[[0, STREAMLIT_COLORS['light']], [1, STREAMLIT_COLORS['primary']]]
                    )
                    fig_sushi.update_layout(
                        xaxis_title="Количество упоминаний",
                        yaxis_title="Суши/Роллы"
                    )
                    fig_sushi = create_custom_chart(fig_sushi)
                    st.plotly_chart(fig_sushi, use_container_width=True)
        
        # Статистическая сводка профиля потребителей
        st.markdown("#### 📈 Общая статистика профиля потребителей")
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.markdown("**📊 Основные показатели:**")
            total_respondents = len(df_profile)
            st.metric("Общее количество респондентов", total_respondents)
            
            if 'пол' in df_profile.columns:
                female_pct = (df_profile['пол'] == 'Женский').mean() * 100
                st.metric("Доля женщин", f"{female_pct:.1f}%")
        
        with col_stats2:
            if 'возраст' in df_profile.columns:
                young_pct = (df_profile['возраст'] == '18-24').mean() * 100
                st.metric("Доля молодежи (18-24)", f"{young_pct:.1f}%")
            
            if 'доход' in df_profile.columns:
                middle_income = df_profile['доход'].value_counts().index[0]
                st.metric("Наиболее частый доход", middle_income)
    
    # Дополнительная информация
    st.markdown("---")
    st.markdown("### 🎉 Итоги и рекомендации")
    
    col1_extra, col2_extra, col3_extra = st.columns(3)
    
    with col1_extra:
        st.info("""
        **📊 Анализ рынка суши в Омске**
        
        Дашборд показывает комплексный анализ предпочтений потребителей суши-ресторанов
        """)
    
    with col2_extra:
        st.success("""
        **🎯 Ключевые направления**
        
        • Поведение потребителей  
        • Ценовые предпочтения  
        • Качество сервиса  
        • Популярность брендов
        """)
    
    with col3_extra:
        st.warning("""
        **💡 Рекомендации**
        
        • Фокус на популярные рестораны  
        • Оптимизация ценовой политики  
        • Улучшение качества обслуживания  
        • Мониторинг удовлетворенности
        """)

if __name__ == "__main__":
    main() 
