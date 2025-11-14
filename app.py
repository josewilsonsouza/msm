import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import base64

# Configuração da página
st.set_page_config(
    page_title="Math Study Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============= PWA SETUP =============
def add_pwa_support():
    """Adiciona suporte PWA com manifest e service worker"""
    
    # Manifest JSON
    manifest = {
        "name": "Math Study Manager",
        "short_name": "StudyApp",
        "description": "Gerenciador de estudos em matemática, projetos de IC e tarefas",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0e1117",
        "theme_color": "#ff4b4b",
        "orientation": "portrait-primary",
        "icons": [
            {
                "src": "https://cdn-icons-png.flaticon.com/512/3976/3976625.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "https://cdn-icons-png.flaticon.com/512/3976/3976625.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    
    manifest_json = json.dumps(manifest)
    manifest_base64 = base64.b64encode(manifest_json.encode()).decode()
    
    # Service Worker simplificado
    service_worker = """
    const CACHE_NAME = 'study-manager-v1';
    const urlsToCache = ['/'];
    
    self.addEventListener('install', event => {
        event.waitUntil(
            caches.open(CACHE_NAME)
                .then(cache => cache.addAll(urlsToCache))
        );
    });
    
    self.addEventListener('fetch', event => {
        event.respondWith(
            caches.match(event.request)
                .then(response => response || fetch(event.request))
        );
    });
    """
    
    sw_base64 = base64.b64encode(service_worker.encode()).decode()
    
    # Injetar no HTML
    pwa_html = f"""
    <link rel="manifest" href="data:application/json;base64,{manifest_base64}">
    <meta name="theme-color" content="#ff4b4b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="StudyApp">
    
    <script>
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register(
                'data:text/javascript;base64,{sw_base64}'
            ).catch(err => console.log('SW registration failed'));
        }}
    </script>
    
    <style>
        /* Botão de instalação PWA */
        .install-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            display: none;
            z-index: 1000;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
    </style>
    
    <button class="install-button" id="installButton">📱 Instalar App</button>
    
    <script>
        let deferredPrompt;
        const installButton = document.getElementById('installButton');
        
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            installButton.style.display = 'block';
        }});
        
        installButton.addEventListener('click', async () => {{
            if (deferredPrompt) {{
                deferredPrompt.prompt();
                const {{ outcome }} = await deferredPrompt.userChoice;
                deferredPrompt = null;
                installButton.style.display = 'none';
            }}
        }});
    </script>
    """
    
    st.markdown(pwa_html, unsafe_allow_html=True)

# Adicionar PWA
add_pwa_support()

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
                'tempo_estimado': 4.0,
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
        ]
    
    if 'sessoes_estudo' not in st.session_state:
        # Gerar histórico dos últimos 14 dias
        st.session_state.sessoes_estudo = []
        for i in range(14):
            data = datetime.now() - timedelta(days=i)
            st.session_state.sessoes_estudo.append({
                'data': data,
                'horas': round(2 + (i % 4) * 0.5, 1),
                'categoria': ['Matemática', 'Projeto IC'][i % 2]
            })

init_session_state()

# ============= FUNÇÕES AUXILIARES =============
def calcular_metricas():
    """Calcula métricas principais"""
    tarefas = st.session_state.tarefas
    
    total_tarefas = len(tarefas)
    concluidas = sum(1 for t in tarefas if t['status'] == 'Concluída')
    em_progresso = sum(1 for t in tarefas if t['status'] == 'Em Progresso')
    pendentes = sum(1 for t in tarefas if t['status'] == 'Pendente')
    
    total_horas_estimadas = sum(t['tempo_estimado'] for t in tarefas)
    total_horas_gastas = sum(t['tempo_gasto'] for t in tarefas)
    
    # Horas estudadas últimos 7 dias
    semana_passada = datetime.now() - timedelta(days=7)
    horas_semana = sum(
        s['horas'] for s in st.session_state.sessoes_estudo 
        if s['data'] >= semana_passada
    )
    
    return {
        'total_tarefas': total_tarefas,
        'concluidas': concluidas,
        'em_progresso': em_progresso,
        'pendentes': pendentes,
        'taxa_conclusao': (concluidas / total_tarefas * 100) if total_tarefas > 0 else 0,
        'horas_estimadas': total_horas_estimadas,
        'horas_gastas': total_horas_gastas,
        'horas_semana': horas_semana
    }

# ============= INTERFACE =============
st.title("📚 Math Study Manager")
st.markdown("*Gerenciador de estudos, projetos de IC e tarefas - PWA Ready*")

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "✅ Tarefas", "📈 Progresso", "➕ Nova Tarefa"])

# ============= TAB 1: DASHBOARD =============
with tab1:
    metricas = calcular_metricas()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Tarefas Totais", 
            metricas['total_tarefas'],
            f"{metricas['concluidas']} concluídas"
        )
    
    with col2:
        st.metric(
            "Em Progresso", 
            metricas['em_progresso'],
            f"{metricas['pendentes']} pendentes"
        )
    
    with col3:
        st.metric(
            "Taxa de Conclusão", 
            f"{metricas['taxa_conclusao']:.0f}%"
        )
    
    with col4:
        st.metric(
            "Horas (7 dias)", 
            f"{metricas['horas_semana']:.1f}h",
            f"{metricas['horas_semana']/7:.1f}h/dia"
        )
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Histórico de Estudos")
        df_sessoes = pd.DataFrame(st.session_state.sessoes_estudo)
        df_sessoes = df_sessoes.sort_values('data')
        
        fig = px.line(
            df_sessoes, 
            x='data', 
            y='horas',
            color='categoria',
            title='Horas de Estudo por Dia',
            markers=True
        )
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title='Data',
            yaxis_title='Horas'
        )
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.subheader("📊 Distribuição de Tarefas")
        df_tarefas = pd.DataFrame(st.session_state.tarefas)
        
        status_counts = df_tarefas['status'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=.4,
            marker_colors=['#ff4b4b', '#ffa500', '#00cc00']
        )])
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")
    
    # Tarefas urgentes
    st.subheader("🔥 Tarefas Urgentes")
    tarefas_urgentes = [
        t for t in st.session_state.tarefas 
        if t['status'] != 'Concluída' and 
        (t['prazo'] - datetime.now()).days <= 3
    ]
    
    if tarefas_urgentes:
        for tarefa in sorted(tarefas_urgentes, key=lambda x: x['prazo']):
            dias_restantes = (tarefa['prazo'] - datetime.now()).days
            cor = "🔴" if dias_restantes <= 1 else "🟡"
            
            st.warning(
                f"{cor} **{tarefa['titulo']}** - "
                f"Prazo: {tarefa['prazo'].strftime('%d/%m/%Y')} "
                f"({dias_restantes} dias)"
            )
    else:
        st.success("✅ Nenhuma tarefa urgente no momento!")

# ============= TAB 2: TAREFAS =============
with tab2:
    st.subheader("Lista de Tarefas")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_categoria = st.selectbox(
            "Categoria",
            ["Todas", "Matemática", "Projeto IC", "Outros"]
        )
    with col2:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Pendente", "Em Progresso", "Concluída"]
        )
    with col3:
        filtro_prioridade = st.selectbox(
            "Prioridade",
            ["Todas", "Alta", "Média", "Baixa"]
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
    
    # Exibir tarefas
    for tarefa in tarefas_filtradas:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                status_emoji = {
                    'Pendente': '⏸️',
                    'Em Progresso': '▶️',
                    'Concluída': '✅'
                }
                st.markdown(f"### {status_emoji[tarefa['status']]} {tarefa['titulo']}")
                st.caption(f"📁 {tarefa['categoria']} | 🎯 {tarefa['prioridade']} | 📅 {tarefa['prazo'].strftime('%d/%m/%Y')}")
            
            with col2:
                progresso = (tarefa['tempo_gasto'] / tarefa['tempo_estimado'] * 100) if tarefa['tempo_estimado'] > 0 else 0
                st.metric("Progresso", f"{progresso:.0f}%")
                st.caption(f"{tarefa['tempo_gasto']:.1f}h / {tarefa['tempo_estimado']:.1f}h")
            
            with col3:
                dias_restantes = (tarefa['prazo'] - datetime.now()).days
                cor_dias = "🔴" if dias_restantes <= 1 else "🟡" if dias_restantes <= 3 else "🟢"
                st.metric("Prazo", f"{dias_restantes}d")
                st.caption(f"{cor_dias} dias restantes")
        
        st.divider()

# ============= TAB 3: PROGRESSO =============
with tab3:
    st.subheader("📈 Análise de Progresso")
    
    df_tarefas = pd.DataFrame(st.session_state.tarefas)
    
    # Tempo por categoria
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⏱️ Tempo Gasto por Categoria")
        tempo_categoria = df_tarefas.groupby('categoria')['tempo_gasto'].sum().reset_index()
        
        fig = px.bar(
            tempo_categoria,
            x='categoria',
            y='tempo_gasto',
            color='categoria',
            title='Distribuição de Tempo'
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.markdown("#### 🎯 Eficiência por Prioridade")
        eficiencia = df_tarefas.groupby('prioridade', group_keys=False).apply(
            lambda x: (x['tempo_gasto'].sum() / x['tempo_estimado'].sum() * 100) 
            if x['tempo_estimado'].sum() > 0 else 0, include_groups=False
        ).reset_index()
        eficiencia.columns = ['prioridade', 'eficiencia']
        
        fig = px.bar(
            eficiencia,
            x='prioridade',
            y='eficiencia',
            color='prioridade',
            title='% do Tempo Estimado Utilizado'
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, width="stretch")
    
    # Tabela resumo
    st.markdown("#### 📋 Resumo Detalhado")
    resumo = df_tarefas.groupby(['categoria', 'status']).agg({
        'id': 'count',
        'tempo_estimado': 'sum',
        'tempo_gasto': 'sum'
    }).reset_index()
    resumo.columns = ['Categoria', 'Status', 'Quantidade', 'Horas Estimadas', 'Horas Gastas']
    st.dataframe(resumo, width="stretch", hide_index=True)

# ============= TAB 4: NOVA TAREFA =============
with tab4:
    st.subheader("➕ Criar Nova Tarefa")
    
    with st.form("nova_tarefa_form"):
        titulo = st.text_input("Título da Tarefa*")
        
        col1, col2 = st.columns(2)
        with col1:
            categoria = st.selectbox(
                "Categoria*",
                ["Matemática", "Projeto IC", "Outros"]
            )
            prioridade = st.selectbox(
                "Prioridade*",
                ["Alta", "Média", "Baixa"]
            )
        
        with col2:
            prazo = st.date_input(
                "Prazo*",
                value=datetime.now() + timedelta(days=7)
            )
            tempo_estimado = st.number_input(
                "Tempo Estimado (horas)*",
                min_value=0.5,
                max_value=100.0,
                value=2.0,
                step=0.5
            )
        
        descricao = st.text_area("Descrição (opcional)")
        
        submitted = st.form_submit_button("✅ Criar Tarefa", width="stretch")
        
        if submitted:
            if not titulo:
                st.error("⚠️ O título é obrigatório!")
            else:
                nova_tarefa = {
                    'id': max([t['id'] for t in st.session_state.tarefas]) + 1,
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

# ============= FOOTER =============
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
    📱 <b>PWA Ready</b> - Instale este app na tela inicial do seu celular<br>
    Funciona offline | Notificações push | Experiência nativa
    </div>
    """,
    unsafe_allow_html=True
)