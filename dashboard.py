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
    'dark': '#1F2937',         # темно-серый
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
        color: #1F2937;
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
        color: #1F2937;
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
        'title_font': dict(size=24, family=f'"{font_family}", Arial, sans-serif', color="#1F2937"),
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'margin': dict(l=60, r=60, t=100, b=60),
        'hoverlabel': dict(
            bgcolor="white",
            bordercolor=STREAMLIT_COLORS['primary'],
            font_size=14, 
            font_family=f'"{font_family}", Arial, sans-serif'
        ),
        'colorway': list(STREAMLIT_COLORS.values())
    }

@st.cache_data
def load_data():
    """Загрузка данных из Excel файла"""
    try:
        df = pd.read_excel('данные по рынку суши.xlsx')
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        return None

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
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor=STREAMLIT_COLORS['light'],
            borderwidth=1,
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
    df = load_data()
    
    if df is None:
        st.error("Не удалось загрузить данные. Проверьте наличие файла 'данные по рынку суши.xlsx'")
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
        with st.expander("📋 Таблица данных", expanded=False):
            st.dataframe(df, use_container_width=True)
    
    # Отладочная информация
    if st.sidebar.checkbox("🔍 Показать структуру данных"):
        with st.expander("🗂️ Названия колонок", expanded=False):
            for i, col in enumerate(df.columns):
                st.write(f"`{i}:` {col}")
    
    # Основные метрики с красивыми карточками
    st.markdown("### 📈 Ключевые показатели")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📋 Записей в данных",
            value=len(df),
            delta="строк данных"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📊 Параметров анализа",
            value=len(df.columns),
            delta="переменных"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        non_null_ratio = (df.count().sum() / (len(df) * len(df.columns)) * 100)
        st.metric(
            label="✅ Заполненность данных",
            value=f"{non_null_ratio:.1f}%",
            delta="качество данных"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        st.metric(
            label="🔢 Числовых колонок",
            value=len(numeric_cols),
            delta="для анализа"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Вкладки для разных анализов
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Посещаемость", 
        "🏪 Рестораны", 
        "💰 Ценообразование", 
        "📈 Удовлетворенность"
    ])
    
    with tab1:
        st.markdown("### 🎯 Анализ посещаемости суши-ресторанов")
        
        col1_tab1, col2_tab1 = st.columns(2)
        
        with col1_tab1:
            # График целей посещения
            if 'цель посещения' in df.columns and 'кол-во' in df.columns:
                purpose_data = df[['цель посещения', 'кол-во']].dropna()
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
            if 'Как часто посещают суши-рестораны' in df.columns:
                frequency_col = df.columns[df.columns.str.contains('кол-во')][1] if len(df.columns[df.columns.str.contains('кол-во')]) > 1 else 'кол-во'
                frequency_data = df[['Как часто посещают суши-рестораны', frequency_col]].dropna()
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
            if 'Какие суши-рестораны в г. Омск  знают' in df.columns and 'кол-во.1' in df.columns:
                known_data = df[['Какие суши-рестораны в г. Омск  знают', 'кол-во.1']].dropna()
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
            if 'В какие суши-рестораны в г. Омск бычно ходят' in df.columns and 'кол-во.2' in df.columns:
                visit_data = df[['В какие суши-рестораны в г. Омск бычно ходят', 'кол-во.2']].dropna()
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
        if 'Какой суши-ресторан  посещают чаще всего' in df.columns and 'кол-во.3' in df.columns:
            popular_data = df[['Какой суши-ресторан  посещают чаще всего', 'кол-во.3']].dropna()
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
        for col in df.columns:
            if any(word in col.lower() for word in ['цена', 'цены', 'стоимость', 'руб']):
                price_columns.append(col)
        
        if price_columns:
            st.info(f"📊 Найденные колонки с ценами: {', '.join(price_columns[:3])}...")
            
            col1_tab3, col2_tab3 = st.columns(2)
            
            # Ищем конкретные колонки по ключевым словам
            max_price_cols = [col for col in df.columns if 'выше' in col.lower() and 'цен' in col.lower()]
            min_price_cols = [col for col in df.columns if 'ниже' in col.lower() and 'цен' in col.lower()]
            fair_price_cols = [col for col in df.columns if 'справедлив' in col.lower() and 'цен' in col.lower()]
            
            with col1_tab3:
                if max_price_cols:
                    max_price_data = df[max_price_cols[0]].dropna()
                    if not max_price_data.empty:
                        fig_max_price = px.histogram(
                            x=max_price_data,
                            title="💸 Максимальная приемлемая цена",
                            nbins=10,
                            color_discrete_sequence=[STREAMLIT_COLORS['primary']]
                        )
                        fig_max_price.update_layout(
                            xaxis_title="Цена (руб.)",
                            yaxis_title="Количество респондентов",
                            bargap=0.1
                        )
                        fig_max_price = create_custom_chart(fig_max_price)
                        st.plotly_chart(fig_max_price, use_container_width=True)
                else:
                    st.info("💭 Данные о максимальной цене не найдены")
            
            with col2_tab3:
                if min_price_cols:
                    min_price_data = df[min_price_cols[0]].dropna()
                    if not min_price_data.empty:
                        fig_min_price = px.histogram(
                            x=min_price_data,
                            title="✨ Минимальная цена для качества",
                            nbins=10,
                            color_discrete_sequence=[STREAMLIT_COLORS['success']]
                        )
                        fig_min_price.update_layout(
                            xaxis_title="Цена (руб.)",
                            yaxis_title="Количество респондентов",
                            bargap=0.1
                        )
                        fig_min_price = create_custom_chart(fig_min_price)
                        st.plotly_chart(fig_min_price, use_container_width=True)
                else:
                    st.info("💭 Данные о минимальной цене не найдены")
            
            # Справедливая цена
            if fair_price_cols:
                fair_price_data = df[fair_price_cols[0]].dropna()
                if not fair_price_data.empty:
                    fig_fair_price = px.box(
                        y=fair_price_data,
                        title="⚖️ Распределение справедливой цены",
                        color_discrete_sequence=[STREAMLIT_COLORS['secondary']]
                    )
                    fig_fair_price.update_layout(yaxis_title="Цена (руб.)")
                    fig_fair_price = create_custom_chart(fig_fair_price)
                    st.plotly_chart(fig_fair_price, use_container_width=True)
            
            # Общий анализ всех ценовых колонок
            if price_columns:
                st.markdown("#### 📈 Сравнительный анализ цен")
                numeric_price_cols = df[price_columns].select_dtypes(include=[np.number]).columns
                if len(numeric_price_cols) > 0:
                    price_data = df[numeric_price_cols].describe().round(2)
                    st.dataframe(price_data, use_container_width=True)
        else:
            st.warning("🔍 Не найдены колонки с ценовыми данными. Проверьте структуру файла.")
    
    with tab4:
        st.markdown("### 📈 Анализ удовлетворенности")
        
        # Поиск колонок с удовлетворенностью
        satisfaction_columns = []
        for col in df.columns:
            if any(word in col.lower() for word in ['удовлетвор', 'оценк', 'балл', 'рейтинг']):
                satisfaction_columns.append(col)
        
        if satisfaction_columns:
            st.info(f"📊 Найденные колонки с оценками: {', '.join(satisfaction_columns[:3])}...")
            
            col1_tab4, col2_tab4 = st.columns(2)
            
            # Поиск конкретных колонок
            general_satisfaction_cols = [col for col in df.columns if 'удовлетворены суши-рестораном' in col]
            characteristics_cols = [col for col in df.columns if 'характеристик' in col.lower()]
            importance_cols = [col for col in df.columns if 'важность' in col.lower()]
            
            with col1_tab4:
                if general_satisfaction_cols and any('кол-во' in col for col in df.columns):
                    count_col = [col for col in df.columns if 'кол-во.4' in col]
                    if count_col:
                        satisfaction_data = df[[general_satisfaction_cols[0], count_col[0]]].dropna()
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
                if characteristics_cols and 'балл' in df.columns:
                    char_data = df[[characteristics_cols[0], 'балл']].dropna()
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
            if importance_cols and '%' in df.columns:
                importance_data = df[[importance_cols[0], '%']].dropna()
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
                numeric_satisfaction = df[satisfaction_columns].select_dtypes(include=[np.number])
                if not numeric_satisfaction.empty:
                    satisfaction_stats = numeric_satisfaction.describe().round(2)
                    st.dataframe(satisfaction_stats, use_container_width=True)
        else:
            st.warning("🔍 Не найдены колонки с данными об удовлетворенности.")
    
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
