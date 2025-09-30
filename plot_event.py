import pandas as pd
import matplotlib.pyplot as plt
import os

input_folder = r"C:\Users\ibraz\Downloads\Campagnes Plateau G-Net Track Pro\drive_test\processed"
graphs_folder = os.path.join(input_folder, "graphs")
os.makedirs(graphs_folder, exist_ok=True)

df_stats = pd.read_csv(os.path.join(input_folder, "resume_stats_events.csv"), index_col=0)
df_detail = pd.read_csv(os.path.join(input_folder, "resume_events_detail.csv"), index_col=0)

# Graphique fiabilité brute
df_stats.plot(kind="bar", figsize=(8,5))
plt.title("Comparaison de la fiabilité par opérateur")
plt.ylabel("Nombre d'événements")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"fiabilite_barres.png"))
plt.close()

# Stacked bar chart
df_stats.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Événements de fiabilité par opérateur (stacked)")
plt.ylabel("Nombre d'événements")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"fiabilite_stacked.png"))
plt.close()

# Top 10 événements majeurs
major_events = [col for col in df_detail.columns][:10]
df_detail[major_events].sum(axis=0).sort_values(ascending=False).plot(kind="bar", figsize=(10,5))
plt.title("Top 10 événements majeurs (tous opérateurs confondus)")
plt.ylabel("Nombre d'occurrences")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"evenements_majeurs.png"))
plt.close()

# Comparaison par opérateur
df_detail[major_events].plot(kind="bar", figsize=(10,6))
plt.title("Comparaison des événements majeurs par opérateur")
plt.ylabel("Nombre d'occurrences")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Opérateurs")
plt.tight_layout()
plt.savefig(os.path.join(graphs_folder,"evenements_majeurs_operateurs.png"))
plt.close()
