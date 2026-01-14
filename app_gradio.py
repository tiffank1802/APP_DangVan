import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import versDV as dv
import deviatoire as dev
from math import pi
import pandas as pd
import io
import base64

# CSS personnalisé avec les couleurs de l'école
css = """
/* Palette de couleurs Centrale Lyon (version rouge) */
:root {
    --primary-red: #D52B1E;
    --secondary-red: #B22222;
    --accent-red: #8B0000;
    --light-gray: #F5F5F5;
    --dark-gray: #333333;
}

.gradio-container {
    font-family: 'Arial', sans-serif;
}

.main-header {
    background: linear-gradient(90deg, var(--primary-red) 0%, var(--secondary-red) 100%);
    padding: 1.5rem;
    border-radius: 0 0 10px 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.centrale-title {
    font-family: 'Georgia', serif;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.centrale-subtitle {
    font-family: 'Arial', sans-serif;
    font-size: 1.2rem;
    opacity: 0.9;
}

.centrale-card {
    border-left: 4px solid var(--accent-red);
    padding: 1rem;
    background-color: var(--light-gray);
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
}

.footer {
    background-color: var(--dark-gray);
    color: white;
    padding: 1rem;
    text-align: center;
    margin-top: 2rem;
    border-radius: 8px 8px 0 0;
    font-size: 0.9rem;
}
"""

def create_header():
    """Crée le header HTML avec le style Centrale Lyon"""
    return f"""
    <div class="main-header">
        <h1 class="centrale-title">ÉCOLE CENTRALE LYON</h1>
        <h2 class="centrale-subtitle">Analyse de Fatigue - Critère de Dang Van</h2>
    </div>
    """

def create_info_panel():
    """Crée le panneau d'informations"""
    return """
    <div class="centrale-card">
        <h3>📝 À propos du critère de Dang Van</h3>
        <p>Le critère de Dang Van est un critère multiaxial de fatigue à haute durée de vie. 
        Il permet de prendre en compte l'effet de la pression hydrostatique sur l'endurance 
        en fatigue des matériaux métalliques. Cette application visualise le domaine de 
        sécurité défini par ce critère pour différents types de chargements.</p>
        
        <h4>👥 Équipe</h4>
        <p><strong>Étudiants :</strong> Kevin TONGUE, Paul LORTHIOIR</p>
        <p><strong>Enseignants :</strong> Éric FEULVACH, Françoise FAUVIN</p>
        <p><strong>UE :</strong> Projet de recherche et innovation</p>
        <p><strong>Thème :</strong> Analyse en fatigue de structures industrielles soumises à des chargements complexes</p>
        <p><strong>Date :</strong> 2026</p>
    </div>
    """

def calculate_dang_van(sigma1, omega, fin, pasTemps, point_size, show_grid, theme):
    """
    Fonction principale de calcul pour le critère de Dang Van
    """
    try:
        # Configuration du style selon le thème choisi
        if theme == "Moderne":
            plt.style.use('seaborn-v0_8-darkgrid')
        elif theme == "Scientifique":
            plt.style.use('seaborn-v0_8-paper')
        else:
            plt.style.use('default')
        
        # Calcul des points pour chargement uniaxial
        points_uniaxial = dv.nuage(sigma1, omega, pasTemps, fin)
        
        # Calcul des points pour torsion
        points_torsion = dv.nuageOrt(sigma1, omega, pasTemps, fin)
        
        # Préparation de la figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Tracé des points
        scatter1 = ax.scatter(
            points_uniaxial[:, 0],
            points_uniaxial[:, 1],
            s=point_size,
            alpha=0.7,
            label='Traction-Compression',
            edgecolors='white',
            linewidth=1
        )

        scatter2 = ax.scatter(
            points_torsion[:, 0],
            points_torsion[:, 1],
            s=point_size,
            alpha=0.7,
            label='Torsion',
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
        
        # Sauvegarde de la figure
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plot_url = f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"
        plt.close(fig)
        
        # Calcul des statistiques
        stats_uniaxial = len(points_uniaxial)
        stats_torsion = len(points_torsion)
        mean_hydro = np.mean(points_uniaxial[:, 0])
        max_shear = max(points_uniaxial[:, 1].max(), points_torsion[:, 1].max())
        
        # Création des DataFrames pour l'export
        df_uniaxial = pd.DataFrame(points_uniaxial, columns=['Pression_hydrostatique', 'Cisaillement_max'])
        df_torsion = pd.DataFrame(points_torsion, columns=['Pression_hydrostatique', 'Cisaillement_max'])
        
        # Analyse du critère
        alpha_est = 0.5
        beta_est = points_uniaxial[:, 1].max() + alpha_est * points_uniaxial[:, 0].mean()
        
        analysis_text = f"""
        ### Analyse du critère de Dang Van
        
        Le critère de Dang Van s'exprime sous la forme :
        
        τ_a,max + α × p_h ≤ β
        
        où :
        - τ_a,max est l'amplitude maximale de cisaillement
        - p_h est la pression hydrostatique
        - α et β sont des constantes matériau
        
        **Paramètres estimés :**
        - α ≈ {alpha_est:.3f}
        - β ≈ {beta_est:.1f} MPa
        """
        
        stats_text = f"""
        ### 📊 Résultats statistiques
        
        **Points uniaxiaux :** {stats_uniaxial} (σ₁={sigma1}MPa)
        **Points torsion :** {stats_torsion} (ω={omega:.2f} rad/s)
        **Pression hydro. moyenne :** {mean_hydro:.1f} MPa (Uniaxial)
        **Cisaillement max :** {max_shear:.1f} MPa
        """
        
        return (
            plot_url,
            stats_text,
            analysis_text,
            df_uniaxial.head(20).to_html(classes='table table-striped'),
            df_torsion.head(20).to_html(classes='table table-striped'),
            df_uniaxial.to_csv(index=False),
            df_torsion.to_csv(index=False),
            buf.getvalue()
        )
        
    except Exception as e:
        error_msg = f"Erreur lors du calcul : {str(e)}"
        return None, error_msg, "", "", "", "", "", None

# Interface Gradio
with gr.Blocks(title="Critère de Dang Van - École Centrale Lyon") as demo:
    gr.HTML(create_header())
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔧 Paramètres d'étude")
            
            sigma1 = gr.Slider(
                minimum=10,
                maximum=200,
                value=100,
                step=5,
                label="Amplitude σ₁ (MPa)",
                info="Amplitude de contrainte en traction-compression"
            )
            
            omega = gr.Slider(
                minimum=0.1,
                maximum=10.0,
                value=2*pi,
                step=0.1,
                label="ω (rad/s)",
                info="Fréquence angulaire du chargement"
            )
            
            fin = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=1.0,
                step=0.1,
                label="Temps final"
            )
            
            pasTemps = gr.Slider(
                minimum=0.001,
                maximum=0.1,
                value=0.01,
                step=0.001,
                label="Pas de temps"
            )
            
            gr.Markdown("### 📊 Options d'affichage")
            point_size = gr.Slider(10, 100, 30, label="Taille des points")
            show_grid = gr.Checkbox(True, label="Afficher la grille")
            theme = gr.Dropdown(
                ["Classique", "Moderne", "Scientifique"],
                value="Classique",
                label="Thème du graphique"
            )
            
            calculate_btn = gr.Button(
                "🚀 Lancer le calcul et la visualisation",
                variant="primary",
                size="lg"
            )
            
        with gr.Column(scale=2):
            gr.Markdown("### Objectif de l'étude")
            gr.HTML("""
            <div class="centrale-card">
                <p>Cette application permet d'analyser le comportement en fatigue des matériaux selon le critère de Dang Van. 
                Le critère permet de prédire l'apparition de fissures de fatigue en considérant simultanément la pression 
                hydrostatique et l'amplitude de cisaillement.</p>
            </div>
            """)
            
            plot_output = gr.HTML()
            
            with gr.Tabs():
                with gr.TabItem("📈 Statistiques"):
                    stats_output = gr.Markdown()
                
                with gr.TabItem("📄 Analyse"):
                    analysis_output = gr.Markdown()
                
                with gr.TabItem("💾 Export des données"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("**Données Traction-Compression**")
                            uniaxial_table = gr.HTML()
                        with gr.Column():
                            gr.Markdown("**Données Torsion**")
                            torsion_table = gr.HTML()
                    
                    with gr.Row():
                        uniaxial_csv = gr.File(label="CSV Traction-Compression")
                        torsion_csv = gr.File(label="CSV Torsion")
                        plot_download = gr.File(label="Graphique PNG")
    
    # Informations
    gr.HTML(create_info_panel())
    
    # Footer
    gr.HTML("""
    <div class="footer">
        <p><strong>École Centrale Lyon</strong> | Mécanique des Matériaux | UE: Fatigue et Fissuration</p>
        <p style="font-size: 0.8rem; opacity: 0.8;">
            Rapport technique - © 2024 - Tous droits réservés
        </p>
    </div>
    """)
    
    # Gestion des événements
    calculate_btn.click(
        fn=calculate_dang_van,
        inputs=[sigma1, omega, fin, pasTemps, point_size, show_grid, theme],
        outputs=[
            plot_output,
            stats_output,
            analysis_output,
            uniaxial_table,
            torsion_table,
            uniaxial_csv,
            torsion_csv,
            plot_download
        ]
    )

# Lancement de l'application
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        css=css
    )