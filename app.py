import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import versDV as dv
import deviatoire as dev
from math import pi

# Import pandas for data export (optional)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Configuration de la page avec le thème École Centrale Lyon
st.set_page_config(
    page_title="Critère de Dang Van - École Centrale Lyon",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec les couleurs de l'école
st.markdown("""
<style>
    /* Palette de couleurs Centrale Lyon (version rouge) */
    :root {
        --primary-red: #D52B1E;
        --secondary-red: #B22222;
        --accent-red: #8B0000;
        --light-gray: #F5F5F5;
        --dark-gray: #333333;
    }
    
    /* Style général */
    .main {
        background-color: white;
    }
    
    /* Header stylisé */
    .centrale-header {
        background: linear-gradient(90deg, var(--primary-red) 0%, var(--secondary-red) 100%);
        padding: 1.5rem;
        border-radius: 0 0 10px 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .centrale-title {
        font-family: 'Georgia', serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .centrale-subtitle {
        font-family: 'Arial', sans-serif;
        text-align: center;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Cartes et widgets */
    .centrale-card {
        border-left: 4px solid var(--accent-red);
        padding: 1rem;
        background-color: var(--light-gray);
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, var(--primary-red) 0%, var(--secondary-red) 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(213, 43, 30, 0.3);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Figures et graphiques */
    .stPlotlyChart, .stPyplot {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        background-color: white;
    }
    
    /* Footer */
    .centrale-footer {
        background-color: var(--dark-gray);
        color: white;
        padding: 1rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 8px 8px 0 0;
    }
    
    /* Séparateurs */
    .stDivider {
        border-color: var(--primary-red);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        color: var(--primary-red) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--dark-gray) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: var(--light-gray);
        padding: 0.5rem;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-red) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Header avec logo et titre
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="centrale-header">
        <h1 class="centrale-title">ÉCOLE CENTRALE LYON</h1>
        <h2 class="centrale-subtitle">Analyse de Fatigue - Critère de Dang Van</h2>
    </div>
    """, unsafe_allow_html=True)

# Sidebar avec paramètres et informations
with st.sidebar:
    # Logo dans la sidebar
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <img src="https://images.seeklogo.com/logo-png/48/2/ecole-centrale-de-lyon-logo-png_seeklogo-481949.png"
              width="150" style="margin-bottom: 1rem;">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 Paramètres d'étude")
    st.markdown("---")
    
    # Paramètres d'entrée
    st.markdown("**Chargement uniaxial**")
    sigma1 = st.slider(
        "Amplitude σ₁ (MPa)", 
        min_value=10, 
        max_value=200, 
        value=100,
        help="Amplitude de contrainte en traction-compression"
    )
    
    st.markdown("**Propriétés temporelles**")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        omega = st.slider(
            "ω (rad/s)", 
            min_value=0.1, 
            max_value=10.0, 
            value=2*pi, 
            step=0.1,
            help="Fréquence angulaire du chargement"
        )
    with col_sb2:
        fin = st.slider(
            "Temps final", 
            min_value=0.1, 
            max_value=2.0, 
            value=1.0, 
            step=0.1
        )
    
    pasTemps = st.slider(
        "Pas de temps", 
        min_value=0.001, 
        max_value=0.1, 
        value=0.01, 
        step=0.001,
        format="%.3f"
    )
    
    st.markdown("---")
    
    # Informations supplémentaires
    with st.expander("ℹ️ Informations"):
        st.markdown("""
        **Étudiants :**
        - Prénom NOM
        - Prénom NOM
        
        **Enseignant :**
        - Dr. Prénom NOM
        
        **UE :** Mécanique des Matériaux
        **Date :** """ + st.session_state.get('date', '2024'))
    
    with st.expander("📊 Options d'affichage"):
        point_size = st.slider("Taille des points", 10, 100, 30)
        show_grid = st.checkbox("Afficher la grille", value=True)
        theme = st.selectbox("Thème du graphique", ["Classique", "Moderne", "Scientifique"])

# Contenu principal
st.markdown("### Objectif de l'étude")
st.markdown("""
<div class="centrale-card">
Cette application permet d'analyser le comportement en fatigue des matériaux selon le critère de Dang Van. 
Le critère permet de prédire l'apparition de fissures de fatigue en considérant simultanément la pression 
hydrostatique et l'amplitude de cisaillement.
</div>
""", unsafe_allow_html=True)

# Bouton de calcul
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    compute_button = st.button(
        "🚀 Lancer le calcul et la visualisation", 
        type="primary",
        use_container_width=True
    )

if compute_button:
    with st.spinner("Calcul en cours... Veuillez patienter."):
        # Barre de progression
        progress_bar = st.progress(0)
        
        # Calcul des points pour chargement uniaxial
        progress_bar.progress(25)
        points_uniaxial = dv.nuage(sigma1, omega, pasTemps, fin)
        
        # Calcul des points pour torsion
        progress_bar.progress(50)
        points_torsion = dv.nuageOrt(sigma1, omega, pasTemps, fin)
        
        # Préparation de la figure
        progress_bar.progress(75)
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Configuration du style selon le thème choisi
        if theme == "Moderne":
            plt.style.use('seaborn-v0_8-darkgrid')
        elif theme == "Scientifique":
            plt.style.use('seaborn-v0_8-paper')
        
        # Tracé des points
        scatter1 = ax.scatter(
            points_uniaxial[:, 0],
            points_uniaxial[:, 1],
            s=point_size,
            alpha=0.7,
            label='Traction-Compression',
            color='#D52B1E',  # Rouge Centrale Lyon
            edgecolors='white',
            linewidth=1
        )

        scatter2 = ax.scatter(
            points_torsion[:, 0],
            points_torsion[:, 1],
            s=point_size,
            alpha=0.7,
            label='Torsion',
            color='#B22222',  # Rouge secondaire
            edgecolors='white',
            linewidth=1
        )
        
        # Configuration des axes et titres
        ax.set_xlabel("Pression hydrostatique (MPa)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Amplitude de cisaillement max (MPa)", fontsize=12, fontweight='bold')
        ax.set_title("Diagramme de Dang Van - École Centrale Lyon", 
                    fontsize=14, fontweight='bold', pad=20)
        
        if show_grid:
            ax.grid(True, linestyle='--', alpha=0.3)
        
        ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
        
        # Ajustement des limites
        xlim_min = min(points_uniaxial[:, 0].min(), points_torsion[:, 0].min()) - 10
        xlim_max = max(points_uniaxial[:, 0].max(), points_torsion[:, 0].max()) + 10
        ylim_max = max(points_uniaxial[:, 1].max(), points_torsion[:, 1].max()) + 10
        ax.set_xlim(xlim_min, xlim_max)
        ax.set_ylim(0, ylim_max)
        
        progress_bar.progress(100)
        st.success("Calcul terminé avec succès !")
    
    # Affichage du graphique
    st.pyplot(fig)
    
    # Métriques et résultats
    st.markdown("### 📊 Résultats statistiques")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    
    with col_res1:
        st.metric(
            label="Points uniaxiaux", 
            value=len(points_uniaxial),
            delta=f"σ₁={sigma1}MPa"
        )
    
    with col_res2:
        st.metric(
            label="Points torsion", 
            value=len(points_torsion),
            delta=f"ω={omega:.2f} rad/s"
        )
    
    with col_res3:
        mean_hydro = np.mean(points_uniaxial[:, 0])
        st.metric(
            label="Pression hydro. moyenne",
            value=f"{mean_hydro:.1f} MPa",
            delta="Uniaxial"
        )

    with col_res4:
        max_shear = max(points_uniaxial[:, 1].max(), points_torsion[:, 1].max())
        st.metric(
            label="Cisaillement max",
            value=f"{max_shear:.1f} MPa"
        )
    
    with col_res4:
        max_shear = max(points_uniaxial[:, 1].max(), points_torsion[:, 1].max())
        st.metric(
            label="Cisaillement max", 
            value=f"{max_shear:.1f} MPa"
        )
    
    # Tabs pour données détaillées
    tab1, tab2, tab3 = st.tabs(["📈 Données détaillées", "📄 Analyse", "💾 Export"])
    
    with tab1:
        col_data1, col_data2 = st.columns(2)
        
        with col_data1:
            st.markdown("**Données traction-compression**")
            st.dataframe(
                pd.DataFrame(points_uniaxial, columns=['Pression hydrostatique', 'Cisaillement max']).head(20),
                use_container_width=True,
                height=300
            )
        
        with col_data2:
            st.markdown("**Données torsion**")
            st.dataframe(
                pd.DataFrame(points_torsion, columns=['Pression hydrostatique', 'Cisaillement max']).head(20),
                use_container_width=True,
                height=300
            )
    
    with tab2:
        st.markdown("#### Analyse du critère de Dang Van")
        st.markdown("""
        Le critère de Dang Van s'exprime sous la forme :
        
        $$
        \\tau_{a,max} + \\alpha p_h \\leq \\beta
        $$
        
        où :
        - $\\tau_{a,max}$ est l'amplitude maximale de cisaillement
        - $p_h$ est la pression hydrostatique
        - $\\alpha$ et $\\beta$ sont des constantes matériau
        """)
        
        # Calcul de la droite de Dang Van (exemple)
        if len(points_uniaxial) > 0:
            alpha_est = 0.5  # Valeur exemple
            beta_est = points_uniaxial[:, 1].max() + alpha_est * points_uniaxial[:, 0].mean()
            
            st.markdown(f"""
            **Paramètres estimés :**
            - $\\alpha \\approx {alpha_est:.3f}$
            - $\\beta \\approx {beta_est:.1f}$ MPa
            """)
    
    with tab3:
        st.markdown("#### Options d'export")

        if PANDAS_AVAILABLE:
            df_uniaxial = pd.DataFrame(points_uniaxial, columns=['Pression_hydrostatique', 'Cisaillement_max'])
            df_torsion = pd.DataFrame(points_torsion, columns=['Pression_hydrostatique', 'Cisaillement_max'])

            col_exp1, col_exp2 = st.columns(2)

            with col_exp1:
                st.download_button(
                    label="📥 Télécharger données uniaxial (CSV)",
                    data=df_uniaxial.to_csv(index=False),
                    file_name="dangvan_uniaxial.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col_exp2:
                st.download_button(
                    label="📥 Télécharger données torsion (CSV)",
                    data=df_torsion.to_csv(index=False),
                    file_name="dangvan_torsion.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Installez pandas pour activer l'export CSV : `pip install pandas`")
        
        # Export de l'image
        if 'fig' in locals():
            import io
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
            buf.seek(0)
            
            st.download_button(
                label="🖼️ Télécharger le graphique (PNG)",
                data=buf,
                file_name="dangvan_diagram.png",
                mime="image/png",
                use_container_width=True
            )

# Footer
st.markdown("""
<div class="centrale-footer">
    <p><strong>École Centrale Lyon</strong> | Mécanique des Matériaux | UE: Fatigue et Fissuration</p>
    <p style="font-size: 0.8rem; opacity: 0.8;">
        Rapport technique - © 2024 - Tous droits réservés
    </p>
</div>
""", unsafe_allow_html=True)

# Note explicative (affichée même sans calcul)
st.markdown("---")
st.markdown("""
### 📝 À propos du critère de Dang Van
<div class="centrale-card">
Le critère de Dang Van est un critère multiaxial de fatigue à haute durée de vie. 
Il permet de prendre en compte l'effet de la pression hydrostatique sur l'endurance 
en fatigue des matériaux métalliques. Cette application visualise le domaine de 
sécurité défini par ce critère pour différents types de chargements.
</div>
""", unsafe_allow_html=True)