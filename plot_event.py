import pandas as pd
import matplotlib.pyplot as plt
import os

# Dossier où se trouvent les fichiers CSV générés par analyze_events.py
input_folder = "processed"  # remplacer par votre propre chemin si besoin
graphs_folder = os.path.join(input_folder, "graphs")
os.makedirs(graphs_folder, exist_ok=True)

# Charger les fichiers de résumé d'événements
df_stats = pd.read_csv(os.path.join(input_folder, "resume_stats_events.csv"), index_col=0)
df_detail = pd.read_csv(os.path.join(input_folder, "resume_events_detail.csv"), index_col=0)

# ---- Graphiques fiabilité ----

# 1. Bar chart simple (fiabilité brute)
df_stats.plot(kind="bar", figsize=(8,5))
plt.title("Comparaison de la fiabilité par opérateur")
plt.ylabel("Nombre d'événements")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"fiabilite_barres.png"))
plt.close()

# 2. Bar chart empilé (stacked)
df_stats.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Événements de fiabilité par opérateur (stacked)")
plt.ylabel("Nombre d'événements")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"fiabilite_stacked.png"))
plt.close()

# ---- Top événements ----

# Sélection des 10 événements les plus fréquents
major_events = df_detail.columns[:10]

# 3. Top 10 événements majeurs (tous opérateurs confondus)
df_detail[major_events].sum(axis=0).sort_values(ascending=False).plot(kind="bar", figsize=(10,5))
plt.title("Top 10 événements majeurs (tous opérateurs confondus)")
plt.ylabel("Nombre d'occurrences")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"evenements_majeurs.png"))
plt.close()

# 4. Comparaison des événements majeurs par opérateur
df_detail[major_events].plot(kind="bar", figsize=(10,6))
plt.title("Comparaison des événements majeurs par opérateur")
plt.ylabel("Nombre d'occurrences")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Opérateurs")
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"evenements_majeurs_operateurs.png"))
plt.close()

print(f"✅ Tous les graphiques événements sauvegardés dans {graphs_folder}")
