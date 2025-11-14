import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- Configuração da Página ---
# Usamos um emoji de alvo para focar em "tarefas"
st.set_page_config(
    page_title="Math Study Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Paleta de Cores e Estilos ---
# Vamos definir algumas cores para usar no app
CORES = {
    "Alta": "#ff4b4b",  # Vermelho
    "Média": "#ffaa00", # Laranja
    "Baixa": "#00b0f0", # Azul
    "Concluída": "#00c851", # Verde
    "Em Progresso": "#ffaa00", # Laranja
    "Pendente": "#a0a0a0"  # Cinza
}

# Injetar CSS customizado para os cards de tarefa
# Isso nos dá mais controle sobre o design
st.markdown(f"""
<style>
    .task-card {{
        border: 2px solid;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .task-card:hover {{
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }}
    .task-card-Alta {{ border-color: {CORES['Alta']}; }}
    .task-card-Média {{ border-color: {CORES['Média']}; }}
    .task-card-Baixa {{ border-color: {CORES['Baixa']}; }}
    .task-card-Concluída {{ 
        border-color: {CORES['Concluída']}; 
        background-color: #f0fdf4; /* Um leve fundo verde */
    }}
    
    /* Remover espaço extra criado pelo st.metric */
    div[data-testid="stMetric"] {{
        padding-bottom: 0px;
    }}
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
                'prazo': datetime.now() + timedelta(days=3),
                'tempo_estimado': 4.0, # Mantido, mas não será exibido
                'tempo_gasto': 1.5
            },
            {
                'id': 2,
                'titulo': 'Projeto IC - Análise de Dados',
                'categoria': 'Projeto IC',
                'prioridade': 'Alta',
                'status': 'Em Progresso',
                'prazo': datetime.now() + timedelta(days=7),
                'tempo_estimado': 10.0,
                'tempo_gasto': 3.0
            },
            {
                'id': 3,
                'titulo': 'Revisar Álgebra Linear',
                'categoria': 'Matemática',
                'prioridade': 'Média',
                'status': 'Pendente',
                'prazo': datetime.now() + timedelta(days=5),
                'tempo_estimado': 3.0,
                'tempo_gasto': 0.0
            },
            {
                'id': 4,
                'titulo': 'Relatório de Pesquisa',
                'categoria': 'Projeto IC',
                'prioridade': 'Alta',
                'status': 'Pendente',
                'prazo': datetime.now() + timedelta(days=10),
                'tempo_estimado': 6.0,
                'tempo_gasto': 0.0
            },
            {
                'id': 5,
                'titulo': 'Exercícios de Geometria Analítica',
                'categoria': 'Matemática',
                'prioridade': 'Baixa',
                'status': 'Pendente',
                'prazo': datetime.now() + timedelta(days=15),
                'tempo_estimado': 5.0,
                'tempo_gasto': 0.0
            },
            {
                'id': 6,
                'titulo': 'Apresentação IC',
                'categoria': 'Projeto IC',
                'prioridade': 'Média',
                'status': 'Concluída',
                'prazo': datetime.now() - timedelta(days=2),
                'tempo_estimado': 4.0,
                'tempo_gasto': 4.0
            },
        ]
    
    # sessoes_estudo foi removido, como solicitado.

init_session_state()

# ============= FUNÇÕES AUXILIARES =============
def calcular_metricas():
    """Calcula métricas principais (apenas contagem de tarefas)"""
    tarefas = st.session_state.tarefas
    
    total_tarefas = len(tarefas)
    concluidas = sum(1 for t in tarefas if t['status'] == 'Concluída')
    em_progresso = sum(1 for t in tarefas if t['status'] == 'Em Progresso')
    pendentes = sum(1 for t in tarefas if t['status'] == 'Pendente')
    
    return {
        'total_tarefas': total_tarefas,
        'concluidas': concluidas,
        'em_progresso': em_progresso,
        'pendentes': pendentes,
    }

def exibir_tarefa_estilizada(tarefa):
    """Renderiza um card de tarefa com cores e estilo."""
    
    status_emoji = {
        'Pendente': '⏸️',
        'Em Progresso': '▶️',
        'Concluída': '✅'
    }
    
    # Define a classe CSS baseada na prioridade ou status
    if tarefa['status'] == 'Concluída':
        card_class = "task-card-Concluída"
    else:
        card_class = f"task-card-{tarefa['prioridade']}"
    
    # Container com a classe CSS customizada
    with st.container():
        st.markdown(f'<div class="task-card {card_class}">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Título com status
            st.markdown(f"### {status_emoji[tarefa['status']]} {tarefa['titulo']}")
            
            # Tags de Categoria e Prioridade (usando markdown para cores)
            cor_prioridade = CORES.get(tarefa['prioridade'], '#888')
            
            st.markdown(
                f"📁 **{tarefa['categoria']}** | <span style='color:{cor_prioridade};'>**🎯 {tarefa['prioridade']}**</span>",
                unsafe_allow_html=True
            )
        
        with col2:
            # Prazo
            dias_restantes = (tarefa['prazo'].date() - datetime.now().date()).days
            cor_dias = "🔴" if dias_restantes <= 1 else "🟡" if dias_restantes <= 3 else "🟢"
            
            if tarefa['status'] == 'Concluída':
                st.metric("Prazo", "Finalizada")
                st.caption(f"✅ Concluída")
            elif dias_restantes < 0:
                st.metric("Prazo", f"{abs(dias_restantes)}d")
                st.caption(f"🔴 Atrasada!")
            else:
                st.metric("Prazo", f"{dias_restantes}d")
                st.caption(f"{cor_dias} restantes")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ============= INTERFACE =============
st.title("🎯 Math Study Manager")
st.markdown("*Seu gerenciador de tarefas de estudo e projetos de IC.*")

# Tabs principais (reorganizadas e simplificadas)
tab1, tab2, tab3 = st.tabs([
    "📊 Visão Geral", 
    "🎯 Minhas Tarefas", 
    "➕ Nova Tarefa"
])

# ============= TAB 1: VISÃO GERAL (Novo Dashboard) =============
with tab1:
    
    # Métricas de contagem (simplificado)
    metricas = calcular_metricas()
    col1, col2, col3 = st.columns(3)
    col1.metric("Pendentes", metricas['pendentes'])
    col2.metric("Em Progresso", metricas['em_progresso'])
    col3.metric("Concluídas", metricas['concluidas'])
    
    st.divider()

    # --- Visualização de Tarefas por Categoria (o "Grafo") ---
    st.subheader("Visualização por Categorias (Treemap)")
    
    df_tarefas = pd.DataFrame(st.session_state.tarefas)
    
    # "Tags" para filtrar o gráfico
    categorias_disponiveis = df_tarefas['categoria'].unique()
    tags_categorias = st.multiselect(
        "Filtrar por 'Tags' (Categorias):",
        options=categorias_disponiveis,
        default=categorias_disponiveis
    )
    
    if not tags_categorias:
        st.warning("Selecione pelo menos uma categoria para ver o gráfico.")
    elif df_tarefas.empty or not df_tarefas['categoria'].isin(tags_categorias).any():
        st.info("Nenhuma tarefa encontrada para as tags selecionadas.")
    else:
        df_filtrado = df_tarefas[df_tarefas['categoria'].isin(tags_categorias)]
        
        # Adicionando uma coluna 'contagem' para o treemap
        df_filtrado['contagem'] = 1
        
        # Criando o Treemap
        fig = px.treemap(
            df_filtrado,
            path=[px.Constant("Todas as Tarefas"), 'categoria', 'prioridade', 'status'],
            values='contagem',
            color='categoria',
            color_discrete_map={
                'Matemática': '#1f77b4',
                'Projeto IC': '#ff7f0e',
                'Outros': '#2ca02c',
                '(?)': '#d62728'
            },
            title="Distribuição de Tarefas por Categoria, Prioridade e Status"
        )
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            height=450
        )
        fig.update_traces(textinfo="label+value", textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- Tarefas Urgentes (Estilo mantido e melhorado) ---
    st.subheader("🔥 Tarefas Urgentes (Próximos 3 dias)")
    
    tarefas_urgentes = [
        t for t in st.session_state.tarefas 
        if t['status'] != 'Concluída' and 
        (t['prazo'].date() - datetime.now().date()).days <= 3
    ]
    
    if tarefas_urgentes:
        for tarefa in sorted(tarefas_urgentes, key=lambda x: x['prazo']):
            dias_restantes = (tarefa['prazo'].date() - datetime.now().date()).days
            
            if dias_restantes < 0:
                cor_emoji = "🚨"
                mensagem_dias = f"Atrasada em {abs(dias_restantes)} dias!"
            elif dias_restantes == 0:
                cor_emoji = "🔴"
                mensagem_dias = "Vence HOJE!"
            elif dias_restantes == 1:
                cor_emoji = "🔴"
                mensagem_dias = "Vence amanhã!"
            else:
                cor_emoji = "🟡"
                mensagem_dias = f"Vence em {dias_restantes} dias."
            
            # Usando o st.warning que você gostou
            st.warning(
                f"{cor_emoji} **{tarefa['titulo']}** ({tarefa['categoria']}) - "
                f"Prazo: {tarefa['prazo'].strftime('%d/%m/%Y')} | **{mensagem_dias}**"
            )
    else:
        st.success("✅ Nenhuma tarefa urgente no momento!")

# ============= TAB 2: MINHAS TAREFAS (Lista Estilizada) =============
with tab2:
    st.subheader("Lista de Tarefas")
    
    # Filtros ("Tags" de filtragem)
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_categoria = st.selectbox(
            "Categoria",
            ["Todas", "Matemática", "Projeto IC", "Outros"],
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
    
    # Aplicar filtros
    tarefas_filtradas = st.session_state.tarefas
    
    if filtro_categoria != "Todas":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['categoria'] == filtro_categoria]
    if filtro_status != "Todos":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['status'] == filtro_status]
    if filtro_prioridade != "Todas":
        tarefas_filtradas = [t for t in tarefas_filtradas if t['prioridade'] == filtro_prioridade]
    
    st.divider()
    
    # Exibir tarefas estilizadas
    if not tarefas_filtradas:
        st.info("Nenhuma tarefa encontrada com esses filtros.")
    else:
        # Ordenar: Concluídas por último, mais urgentes primeiro
        tarefas_filtradas.sort(key=lambda x: (x['status'] == 'Concluída', x['prazo']))
        
        for tarefa in tarefas_filtradas:
            exibir_tarefa_estilizada(tarefa)


# ============= TAB 3: NOVA TAREFA (Formulário com Emojis) =============
with tab3:
    st.subheader("➕ Criar Nova Tarefa")
    
    with st.form("nova_tarefa_form"):
        # Campo obrigatório
        titulo = st.text_input("✏️ Título da Tarefa*")
        
        col1, col2 = st.columns(2)
        with col1:
            # Campos obrigatórios
            categoria = st.selectbox(
                "📁 Categoria*",
                ["Matemática", "Projeto IC", "Outros"]
            )
            prioridade = st.selectbox(
                "🎯 Prioridade*",
                ["Alta", "Média", "Baixa"],
                index=1 # Default Média
            )
        
        with col2:
            # Campo obrigatório
            prazo = st.date_input(
                "📅 Prazo*",
                value=datetime.now() + timedelta(days=7)
            )
            # Campo opcional (sem *)
            tempo_estimado = st.number_input(
                "⏱️ Tempo Estimado (horas)",
                min_value=0.0,
                max_value=100.0,
                value=1.0, # Default 1.0, mas 0.0 é permitido
                step=0.5
            )
        
        # Campo opcional
        descricao = st.text_area("🗒️ Descrição (opcional)")
        
        submitted = st.form_submit_button("✅ Criar Tarefa", use_container_width=True)
        
        if submitted:
            # Apenas o título é realmente verificado
            if not titulo:
                st.error("⚠️ O título é obrigatório!")
            else:
                nova_tarefa = {
                    'id': max([t['id'] for t in st.session_state.tarefas], default=0) + 1,
                    'titulo': titulo,
                    'categoria': categoria,
                    'prioridade': prioridade,
                    'status': 'Pendente',
                    'prazo': datetime.combine(prazo, datetime.min.time()),
                    'tempo_estimado': tempo_estimado,
                    'tempo_gasto': 0.0
                }
                
                st.session_state.tarefas.append(nova_tarefa)
                st.success(f"✅ Tarefa '{titulo}' criada com sucesso!")
                st.balloons()