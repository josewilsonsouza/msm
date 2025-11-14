import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ============= CONFIGURAÇÃO DA PÁGINA =============
st.set_page_config(
    page_title="Math Study Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= ESTILOS CUSTOMIZADOS ELEGANTES =============
st.markdown("""
<style>
    /* Variáveis de cores elegantes */
    :root {
        --primary: #7C3AED;
        --danger: #EF4444;
        --warning: #F97316;
        --success: #10B981;
        --info: #06B6D4;
        --dark-bg: #0F172A;
        --card-bg: #1E293B;
        --border: #334155;
        --text: #F1F5F9;
    }
    
    /* Animações suaves */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header elegante */
    .main-header {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        padding: 2.5rem;
        border-radius: 1.25rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.2);
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-size: 1.125rem;
        color: rgba(255, 255, 255, 0.85);
        margin-top: 0.5rem;
    }
    
    /* Metrics elegantes */
    .metric-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%);
        border: 2px solid rgba(124, 58, 237, 0.3);
        border-radius: 1rem;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.25) 0%, rgba(99, 102, 241, 0.25) 100%);
        border-color: rgba(124, 58, 237, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.15);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #E9D5FF;
        margin-bottom: 0.5rem;
    }
    
    .metric-desc {
        font-size: 0.75rem;
        color: #64748B;
    }
    
    /* Task Card */
    .task-card {
        border: 1px solid;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, rgba(31, 41, 55, 0.8) 0%, rgba(17, 24, 39, 0.8) 100%);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .task-card:hover {
        box-shadow: 0 12px 40px rgba(124, 58, 237, 0.2);
        transform: translateY(-4px);
        border-color: #7C3AED;
        background: linear-gradient(135deg, rgba(31, 41, 55, 1) 0%, rgba(17, 24, 39, 1) 100%);
    }
    
    /* Indicador de prioridade (barra esquerda) */
    .task-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        transition: width 0.3s ease;
    }
    
    .task-card:hover::before {
        width: 6px;
    }
    
    /* Cores por prioridade */
    .task-card-Alta::before { background: linear-gradient(180deg, #EF4444 0%, #DC2626 100%); }
    .task-card-Média::before { background: linear-gradient(180deg, #F97316 0%, #EA580C 100%); }
    .task-card-Baixa::before { background: linear-gradient(180deg, #06B6D4 0%, #0891B2 100%); }
    .task-card-Concluída::before { background: linear-gradient(180deg, #10B981 0%, #059669 100%); }
    
    /* Bordas por prioridade */
    .task-card-Alta { border-color: rgba(239, 68, 68, 0.3); }
    .task-card-Média { border-color: rgba(249, 115, 22, 0.3); }
    .task-card-Baixa { border-color: rgba(6, 182, 212, 0.3); }
    .task-card-Concluída { 
        border-color: rgba(16, 185, 129, 0.3);
        opacity: 0.85;
    }
    
    /* Status badges elegantes */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        background: rgba(124, 58, 237, 0.15);
        color: #E9D5FF;
        border: 1px solid rgba(124, 58, 237, 0.3);
        backdrop-filter: blur(4px);
        transition: all 0.3s ease;
    }
    
    /* Variações de cores para badges */
    .badge-success { background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.3); color: #A7F3D0; }
    .badge-warning { background: rgba(249, 115, 22, 0.15); border-color: rgba(249, 115, 22, 0.3); color: #FFEDD5; }
    .badge-danger { background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); color: #FECACA; }
    .badge-info { background: rgba(6, 182, 212, 0.15); border-color: rgba(6, 182, 212, 0.3); color: #A5F3FC; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1.5rem;
        background: rgba(51, 65, 85, 0.5);
        border-radius: 0.75rem 0.75rem 0 0;
        border: 1px solid rgba(124, 58, 237, 0.2);
        color: #94A3B8;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.3) 0%, rgba(99, 102, 241, 0.3) 100%);
        color: #E9D5FF;
        border-color: #7C3AED;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
    }
    
    /* Divisores elegantes */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Botões primários */
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 0.75rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(124, 58, 237, 0.4);
    }
    
    /* Inputs elegantes */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(51, 65, 85, 0.8);
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        color: #F1F5F9;
        border-radius: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    /* Container com borda */
    .stContainer {
        border-radius: 1rem;
    }
    
    /* Subheadings */
    h2, h3 {
        color: #F1F5F9;
        font-weight: 700;
    }
    
    h2 {
        border-left: 4px solid #7C3AED;
        padding-left: 1rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============= INICIALIZAÇÃO DE DADOS =============
def init_session_state():
    """Inicializa o estado da sessão com dados de exemplo"""
    if 'tarefas' not in st.session_state:
        st.session_state.tarefas = [
            {
                'id': 1,
                'titulo': 'Estudar Cálculo II - Integrais',
                'categoria': 'Matemática',
                'prioridade': 'Alta',
                'status': 'Em Progresso',
                'prazo': datetime.now() + timedelta(days=2),
                'descricao': 'Revisão completa de integrais impróprias e técnicas de integração'
            },
            {
                'id': 2,
                'titulo': 'Projeto IC - Análise de Dados',
                'categoria': 'Projeto IC',
                'prioridade': 'Alta',
                'status': 'Em Progresso',
                'prazo': datetime.now() + timedelta(days=7),
                'descricao': 'Implementação do pipeline de análise e visualização'
            },
            {
                'id': 3,
                'titulo': 'Revisar Álgebra Linear',
                'categoria': 'Matemática',
                'prioridade': 'Média',
                'status': 'Pendente',
                'prazo': datetime.now() + timedelta(days=5),
                'descricao': 'Foco em transformações lineares e autovalores'
            },
            {
                'id': 4,
                'titulo': 'Relatório de Pesquisa',
                'categoria': 'Projeto IC',
                'prioridade': 'Alta',
                'status': 'Pendente',
                'prazo': datetime.now() - timedelta(days=1),
                'descricao': 'Escrita e revisão final do relatório'
            },
            {
                'id': 5,
                'titulo': 'Exercícios de Geometria Analítica',
                'categoria': 'Matemática',
                'prioridade': 'Baixa',
                'status': 'Pendente',
                'prazo': datetime.now() + timedelta(days=15),
                'descricao': 'Capítulos 3-5 do livro de texto'
            },
            {
                'id': 6,
                'titulo': 'Apresentação IC',
                'categoria': 'Projeto IC',
                'prioridade': 'Média',
                'status': 'Concluída',
                'prazo': datetime.now() - timedelta(days=2),
                'descricao': 'Apresentação dos resultados preliminares'
            },
        ]
    
    if 'categorias' not in st.session_state:
        st.session_state.categorias = ['Matemática', 'Projeto IC']
    
    if 'show_edit_form' not in st.session_state:
        st.session_state.show_edit_form = False
    
    if 'edit_tarefa_id' not in st.session_state:
        st.session_state.edit_tarefa_id = None

init_session_state()

# ============= FUNÇÕES AUXILIARES =============
def calcular_metricas():
    """Calcula métricas principais"""
    tarefas = st.session_state.tarefas
    concluidas = sum(1 for t in tarefas if t['status'] == 'Concluída')
    em_progresso = sum(1 for t in tarefas if t['status'] == 'Em Progresso')
    pendentes = sum(1 for t in tarefas if t['status'] == 'Pendente')
    total = len(tarefas)
    percentual_conclusao = (concluidas / total * 100) if total > 0 else 0
    
    return {
        'concluidas': concluidas,
        'em_progresso': em_progresso,
        'pendentes': pendentes,
        'total': total,
        'percentual': percentual_conclusao
    }

def get_cor_prioridade(prioridade):
    """Retorna cor hex baseada na prioridade"""
    cores = {
        "Alta": "#EF4444",
        "Média": "#F97316",
        "Baixa": "#06B6D4"
    }
    return cores.get(prioridade, "#7C3AED")

def get_emoji_prioridade(prioridade):
    """Retorna emoji baseado na prioridade"""
    emojis = {
        "Alta": "🔴",
        "Média": "🟠",
        "Baixa": "🔵"
    }
    return emojis.get(prioridade, "⚪")

def get_emoji_status(status):
    """Retorna emoji baseado no status"""
    emojis = {
        'Pendente': '⏸️',
        'Em Progresso': '▶️',
        'Concluída': '✅'
    }
    return emojis.get(status, '❓')

def exibir_tarefa_estilizada(tarefa):
    """Renderiza um card de tarefa elegante com opções de ação"""
    
    card_class = f"task-card-{tarefa['status']}" if tarefa['status'] == 'Concluída' else f"task-card-{tarefa['prioridade']}"
    
    emoji_status = get_emoji_status(tarefa['status'])
    emoji_prioridade = get_emoji_prioridade(tarefa['prioridade'])
    titulo = tarefa['titulo']
    categoria = tarefa['categoria']
    prioridade = tarefa['prioridade']
    cor_prioridade = get_cor_prioridade(prioridade)
    descricao = tarefa.get('descricao', '')
    
    dias_restantes = (tarefa['prazo'].date() - datetime.now().date()).days
    
    if tarefa['status'] == 'Concluída':
        valor_prazo = "✓"
        status_class = "badge-success"
        label_prazo = "Concluída"
    elif dias_restantes < 0:
        valor_prazo = f"{abs(dias_restantes)}d"
        status_class = "badge-danger"
        label_prazo = "Atrasada!"
    elif dias_restantes <= 3:
        valor_prazo = f"{dias_restantes}d"
        status_class = "badge-warning"
        label_prazo = f"{dias_restantes} dias"
    else:
        valor_prazo = f"{dias_restantes}d"
        status_class = "badge-info"
        label_prazo = f"{dias_restantes} dias"
    
    # Usar HTML customizado já que os componentes não permitem o layout que queremos
    card_html = f"""
    <div class="task-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; width: 100%; gap: 1.5rem;">
            <div style="flex-grow: 1;">
                <h3 style="margin: 0 0 0.75rem 0; font-size: 1.125rem; color: #F1F5F9;">
                    {emoji_status} {titulo}
                </h3>
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 0.75rem;">
                    <span style="font-size: 0.875rem; color: #94A3B8;">📁 <strong>{categoria}</strong></span>
                    <span style="color: {cor_prioridade}; font-weight: 600; font-size: 0.875rem;">
                        {emoji_prioridade} {prioridade}
                    </span>
                </div>
                {f'<small style="color: #64748B; display: block; margin-top: 0.5rem;">{descricao}</small>' if descricao else ''}
            </div>
            <div style="flex-shrink: 0; text-align: center; min-width: 110px;">
                <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 700;">
                    Prazo
                </div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {cor_prioridade}; margin-bottom: 0.75rem;">
                    {valor_prazo}
                </div>
                <span class="status-badge {status_class}">{label_prazo}</span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Botões de ação
    col_actions = st.columns([1, 1, 1, 1])
    
    with col_actions[0]:
        if st.button("✏️ Editar", key=f"editar_{tarefa['id']}", use_container_width=True):
            st.session_state.edit_tarefa_id = tarefa['id']
            st.session_state.show_edit_form = True
    
    with col_actions[1]:
        if tarefa['status'] != 'Concluída':
            if st.button("✅ Concluir", key=f"concluir_{tarefa['id']}", use_container_width=True):
                # Encontrar e atualizar a tarefa
                for t in st.session_state.tarefas:
                    if t['id'] == tarefa['id']:
                        t['status'] = 'Concluída'
                        st.success(f"✨ Tarefa '{tarefa['titulo']}' concluída!")
                        st.rerun()
                        break
        else:
            st.button("✅ Concluída", key=f"concluir_{tarefa['id']}", use_container_width=True, disabled=True)
    
    with col_actions[2]:
        if st.button("🗑️ Excluir", key=f"excluir_{tarefa['id']}", use_container_width=True):
            st.session_state.tarefas = [t for t in st.session_state.tarefas if t['id'] != tarefa['id']]
            st.success(f"🗑️ Tarefa '{tarefa['titulo']}' excluída!")
            st.rerun()

def criar_chart_elegante(df_filtrado):
    """Cria um treemap elegante"""
    df_filtrado = df_filtrado.copy()
    df_filtrado['contagem'] = 1
    
    cores_prioridade = {
        'Alta': '#EF4444',
        'Média': '#F97316',
        'Baixa': '#06B6D4',
    }
    
    fig = px.treemap(
        df_filtrado,
        path=[px.Constant("Tarefas"), 'categoria', 'prioridade', 'status'],
        values='contagem',
        color='prioridade',
        color_discrete_map=cores_prioridade,
    )
    
    fig.update_layout(
        margin=dict(t=40, l=20, r=20, b=20),
        height=500,
        paper_bgcolor='rgba(15, 23, 42, 0.9)',
        font=dict(
            color='#F1F5F9',
            family='system-ui, -apple-system, sans-serif',
            size=13
        ),
    )
    
    fig.update_traces(
        textinfo="label+value",
        textfont=dict(
            size=12,
            color='white',
            family='system-ui, -apple-system, sans-serif'
        ),
        textposition='middle center',
        marker=dict(
            line=dict(width=2, color='rgba(15, 23, 42, 0.95)')
        )
    )
    
    return fig

# ============= INTERFACE PRINCIPAL =============

# Modal de edição de tarefa
if st.session_state.show_edit_form and st.session_state.edit_tarefa_id:
    # Encontrar a tarefa a ser editada
    tarefa_edit = None
    for t in st.session_state.tarefas:
        if t['id'] == st.session_state.edit_tarefa_id:
            tarefa_edit = t
            break
    
    if tarefa_edit:
        st.markdown("### ✏️ Editar Tarefa")
        
        with st.form("editar_tarefa_form", border=True):
            titulo = st.text_input(
                "✏️ Título da Tarefa",
                value=tarefa_edit['titulo'],
                max_chars=100
            )
            
            descricao = st.text_area(
                "📝 Descrição",
                value=tarefa_edit['descricao'],
                max_chars=500,
                height=100
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                categoria = st.selectbox(
                    "📂 Categoria",
                    st.session_state.categorias,
                    index=st.session_state.categorias.index(tarefa_edit['categoria']) if tarefa_edit['categoria'] in st.session_state.categorias else 0
                )
            
            with col2:
                prioridade = st.selectbox(
                    "🎯 Prioridade",
                    ["Alta", "Média", "Baixa"],
                    index=["Alta", "Média", "Baixa"].index(tarefa_edit['prioridade'])
                )
            
            with col3:
                status = st.selectbox(
                    "📊 Status",
                    ["Pendente", "Em Progresso", "Concluída"],
                    index=["Pendente", "Em Progresso", "Concluída"].index(tarefa_edit['status'])
                )
            
            prazo = st.date_input(
                "📅 Data de Prazo",
                value=tarefa_edit['prazo'].date()
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                submitted = st.form_submit_button(
                    "💾 Salvar Alterações",
                    type="primary",
                    use_container_width=True
                )
            
            with col_btn2:
                if st.form_submit_button(
                    "❌ Cancelar",
                    use_container_width=True
                ):
                    st.session_state.show_edit_form = False
                    st.session_state.edit_tarefa_id = None
                    st.rerun()
            
            if submitted:
                if not titulo.strip():
                    st.error("❌ O título é obrigatório!")
                else:
                    # Atualizar a tarefa
                    for t in st.session_state.tarefas:
                        if t['id'] == st.session_state.edit_tarefa_id:
                            t['titulo'] = titulo
                            t['descricao'] = descricao
                            t['categoria'] = categoria
                            t['prioridade'] = prioridade
                            t['status'] = status
                            t['prazo'] = datetime.combine(prazo, datetime.min.time())
                            st.success(f"✨ Tarefa '{titulo}' atualizada com sucesso!")
                            st.session_state.show_edit_form = False
                            st.session_state.edit_tarefa_id = None
                            st.rerun()
                            break
        
        st.divider()

# Header elegante
st.markdown("""
    <div class="main-header">
        <h1>🎯 Math Study Manager</h1>
        <p>Gerencie suas tarefas de estudo e projetos</p>
    </div>
""", unsafe_allow_html=True)

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "🎯 Minhas Tarefas",
    "➕ Nova Tarefa",
    "⚙️ Categorias"
])

# ============= TAB 1: VISÃO GERAL =============
with tab1:
    metricas = calcular_metricas()
    
    # Progresso
    st.markdown("### 📈 Seu Progresso Geral")
    st.progress(metricas['percentual'] / 100, text=f"{metricas['percentual']:.0f}% Concluído")
    
    st.divider()
    
    # Métricas
    st.markdown("### 📊 Estatísticas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total</div>
                <div class="metric-value">{metricas['total']}</div>
                <div class="metric-desc">tarefas cadastradas</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Pendentes</div>
                <div class="metric-value">{metricas['pendentes']}</div>
                <div class="metric-desc">aguardando início</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Em Progresso</div>
                <div class="metric-value">{metricas['em_progresso']}</div>
                <div class="metric-desc">sendo trabalhadas</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Concluídas</div>
                <div class="metric-value">{metricas['concluidas']}</div>
                <div class="metric-desc">finalizadas</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gráfico
    st.markdown("### 📂 Distribuição por Categorias")
    df_tarefas = pd.DataFrame(st.session_state.tarefas)
    
    categorias_disponiveis = list(df_tarefas['categoria'].unique())
    tags_categorias = st.multiselect(
        "Selecione as categorias:",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
        label_visibility="collapsed"
    )
    
    if not tags_categorias:
        st.warning("📌 Selecione pelo menos uma categoria para visualizar o gráfico.")
    elif df_tarefas.empty or not df_tarefas['categoria'].isin(tags_categorias).any():
        st.info("ℹ️ Nenhuma tarefa encontrada para as categorias selecionadas.")
    else:
        df_filtrado = df_tarefas[df_tarefas['categoria'].isin(tags_categorias)].copy()
        fig = criar_chart_elegante(df_filtrado)
        st.plotly_chart(fig, width='stretch')
    
    st.divider()
    
    # Urgentes
    st.markdown("### 🔥 Foco da Semana - Tarefas Urgentes")
    
    tarefas_urgentes = [
        t for t in st.session_state.tarefas
        if t['status'] != 'Concluída' and
        (t['prazo'].date() - datetime.now().date()).days <= 7
    ]
    
    if tarefas_urgentes:
        tarefas_urgentes_sorted = sorted(tarefas_urgentes, key=lambda x: x['prazo'])
        
        for tarefa in tarefas_urgentes_sorted:
            dias_restantes = (tarefa['prazo'].date() - datetime.now().date()).days
            
            if dias_restantes < 0:
                st.error(f"🚨 **ATRASADA**: {tarefa['titulo']} ({tarefa['categoria']}) - {abs(dias_restantes)} dias atrás")
            elif dias_restantes == 0:
                st.error(f"🔴 **VENCE HOJE**: {tarefa['titulo']} ({tarefa['categoria']})")
            elif dias_restantes <= 3:
                st.warning(f"🟠 **VENCE EM {dias_restantes} DIAS**: {tarefa['titulo']} ({tarefa['categoria']})")
            else:
                st.info(f"🔵 **VENCE EM {dias_restantes} DIAS**: {tarefa['titulo']} ({tarefa['categoria']})")
    else:
        st.success("✅ Nenhuma tarefa urgente para os próximos 7 dias! Excelente trabalho!")

# ============= TAB 2: MINHAS TAREFAS =============
with tab2:
    st.markdown("### 📋 Lista de Tarefas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_categoria = st.selectbox(
            "Categoria",
            ["Todas"] + list(pd.DataFrame(st.session_state.tarefas)['categoria'].unique()),
            key='filtro_cat_tab2'
        )
    with col2:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Pendente", "Em Progresso", "Concluída"],
            key='filtro_status_tab2'
        )
    with col3:
        filtro_prioridade = st.selectbox(
            "Prioridade",
            ["Todas", "Alta", "Média", "Baixa"],
            key='filtro_prio_tab2'
        )
    
    tarefas_filtradas = st.session_state.tarefas
    if filtro_categoria != "Todas":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['categoria'] == filtro_categoria]
    if filtro_status != "Todos":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['status'] == filtro_status]
    if filtro_prioridade != "Todas":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['prioridade'] == filtro_prioridade]
    
    st.divider()
    
    if not tarefas_filtradas:
        st.info("📭 Nenhuma tarefa encontrada com esses filtros.")
    else:
        tarefas_filtradas.sort(key=lambda x: (x['status'] == 'Concluída', x['prazo']))
        for tarefa in tarefas_filtradas:
            exibir_tarefa_estilizada(tarefa)

# ============= TAB 3: NOVA TAREFA =============
with tab3:
    st.markdown("### ✨ Criar Nova Tarefa")
    
    with st.form("nova_tarefa_form", border=True):
        titulo = st.text_input(
            "✏️ Título da Tarefa",
            placeholder="Ex: Estudar Transformadas de Laplace",
            max_chars=100
        )
        
        descricao = st.text_area(
            "📝 Descrição (opcional)",
            placeholder="Detalhe o que precisa ser feito...",
            max_chars=500,
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            categoria = st.selectbox(
                "📂 Categoria",
                st.session_state.categorias
            )
            prioridade = st.selectbox(
                "🎯 Prioridade",
                ["Média", "Alta", "Baixa"]
            )
        
        with col2:
            prazo = st.date_input(
                "📅 Data de Prazo",
                value=datetime.now() + timedelta(days=7)
            )
        
        col_submit = st.columns([1, 4])
        with col_submit[0]:
            submitted = st.form_submit_button(
                "✅ Criar Tarefa",
                width='stretch',
                type="primary"
            )
        
        if submitted:
            if not titulo.strip():
                st.error("❌ O título é obrigatório!")
            else:
                nova_tarefa = {
                    'id': max([t['id'] for t in st.session_state.tarefas], default=0) + 1,
                    'titulo': titulo,
                    'categoria': categoria,
                    'prioridade': prioridade,
                    'status': 'Pendente',
                    'prazo': datetime.combine(prazo, datetime.min.time()),
                    'descricao': descricao,
                }
                
                st.session_state.tarefas.append(nova_tarefa)
                st.success(f"🎉 Tarefa '{titulo}' criada com sucesso!")
                st.balloons()

# ============= TAB 4: CATEGORIAS =============
with tab4:
    st.markdown("### 🏷️ Gerenciar Categorias")
    st.markdown("Adicione ou remova categorias para organizar melhor suas tarefas.")
    
    st.divider()
    
    st.markdown("#### 📋 Categorias Existentes")
    
    if st.session_state.categorias:
        for cat in st.session_state.categorias:
            tarefas_cat = sum(1 for t in st.session_state.tarefas if t['categoria'] == cat)
            col_info, col_btn = st.columns([4, 1])
            
            with col_info:
                st.markdown(f"**📁 {cat}** • {tarefas_cat} tarefa(s)")
            
            with col_btn:
                if st.button("🗑️ Remover", key=f"del_{cat}"):
                    if tarefas_cat > 0:
                        st.error(f"❌ Não é possível remover '{cat}' pois há {tarefas_cat} tarefa(s) associada(s).")
                    else:
                        st.session_state.categorias.remove(cat)
                        st.success(f"✅ Categoria '{cat}' removida!")
                        st.rerun()
    else:
        st.info("ℹ️ Nenhuma categoria criada ainda.")
    
    st.divider()
    
    st.markdown("#### ➕ Adicionar Nova Categoria")
    
    col_input, col_btn = st.columns([3, 1])
    
    with col_input:
        nova_categoria = st.text_input(
            "Nome da categoria",
            placeholder="Ex: Programação, Línguas, etc...",
            max_chars=50,
            label_visibility="collapsed"
        )
    
    with col_btn:
        st.write("")
        if st.button("✅ Adicionar", type="primary", use_container_width=True):
            if not nova_categoria.strip():
                st.error("❌ Digite um nome para a categoria!")
            elif nova_categoria in st.session_state.categorias:
                st.error(f"❌ A categoria '{nova_categoria}' já existe!")
            else:
                st.session_state.categorias.append(nova_categoria)
                st.success(f"🎉 Categoria '{nova_categoria}' criada com sucesso!")
                st.rerun()

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: #64748B; font-size: 0.875rem;'><p>🎯 Math Study Manager</p><p style='font-size: 0.75rem;'></p></div>", unsafe_allow_html=True)