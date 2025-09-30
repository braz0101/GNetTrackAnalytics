import os
import subprocess
import pandas as pd

# 📂 Dossiers de travail
BASE_FOLDER = "."  # dossier racine du projet (remplacer si nécessaire)
RAW_FOLDER = os.path.join(BASE_FOLDER, "raw_logs")
PROCESSED_FOLDER = os.path.join(BASE_FOLDER, "processed")
GRAPH_FOLDER = os.path.join(PROCESSED_FOLDER, "graphs")
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# 🔹 Changer le répertoire courant vers le dossier de base
os.chdir(BASE_FOLDER)

# ==========================
# 1️⃣ Nettoyage des fichiers TXT
# ==========================
print("🔹 Etape 1 : Nettoyage des fichiers TXT...")
subprocess.run(["python", "clean_txt_to_csv.py"], check=True)
print("✅ Fichiers TXT nettoyés et CSV générés.\n")

# ==========================
# 2️⃣ Analyse qualité radio
# ==========================
print("🔹 Etape 2 : Analyse qualité radio (RSRP/SNR/CQI)...")
subprocess.run(["python", "plot_signal_quality.py"], check=True)
print("✅ Graphiques radio générés.\n")

# ==========================
# 3️⃣ Analyse performance data
# ==========================
print("🔹 Etape 3 : Analyse performance data (Download/Upload/Ping)...")
subprocess.run(["python", "analyze_datatest.py"], check=True)
print("✅ Graphiques data générés.\n")

# ==========================
# 4️⃣ Analyse événements
# ==========================
print("🔹 Etape 4 : Analyse événements réseau...")
subprocess.run(["python", "analyze_events.py"], check=True)
subprocess.run(["python", "plot_events.py"], check=True)  # ⚡ Nom corrigé
print("✅ Graphiques événements générés.\n")

# ==========================
# 5️⃣ Résumé global par opérateur
# ==========================
print("🔹 Etape 5 : Génération du résumé global...")

# Charger statistiques radio
df_radio = pd.read_csv(os.path.join(GRAPH_FOLDER, "resume_stats_radio.csv"), index_col=0)

# Charger statistiques data
df_data = pd.read_csv(os.path.join(GRAPH_FOLDER, "resume_stats_datatest.csv"), index_col=0)

# Charger statistiques événements
df_events = pd.read_csv(os.path.join(PROCESSED_FOLDER, "resume_stats_events.csv"), index_col=0)

# Fusionner toutes les stats par opérateur
summary = df_radio.join(df_data, how="outer").join(df_events, how="outer")
summary.fillna(0, inplace=True)

# Sauvegarder le résumé global
summary.to_csv(os.path.join(GRAPH_FOLDER, "resume_global.csv"))

print("✅ Résumé global sauvegardé : resume_global.csv\n")
print("🎯 Pipeline terminé avec succès ! Tous les résultats et graphiques sont dans :")
print(GRAPH_FOLDER)
