import pandas as pd
import glob, os

# ⚠️ Remplacez ces chemins par vos dossiers locaux si besoin
# On recommande de garder processed/ dans le même dossier que le script
input_folder = r"processed"    # dossier contenant les CSV *_events_clean.csv
os.makedirs(input_folder, exist_ok=True)

# Charger tous les fichiers *_events_clean.csv
files = glob.glob(os.path.join(input_folder, "*_events_clean.csv"))
data = []

for file in files:
    df = pd.read_csv(file)
    operator = os.path.basename(file).split("_")[0]
    df["Operator"] = operator
    data.append(df)

df_all = pd.concat(data, ignore_index=True)
print("📊 Nombre total d'événements :", len(df_all))
print("Opérateurs trouvés :", df_all["Operator"].unique())

# Détecter la colonne des événements
if "EventType" in df_all.columns:
    event_col = "EventType"
elif "Event" in df_all.columns:
    event_col = "Event"
else:
    event_col = df_all.columns[0]  # première colonne si nom inconnu

# Comptage par type d'événement
handover = df_all[df_all[event_col].str.contains("handover", case=False, na=False)].groupby("Operator").size()
drop = df_all[df_all[event_col].str.contains("drop", case=False, na=False)].groupby("Operator").size()
failures = df_all[df_all[event_col].str.contains("fail|error|reject", case=False, na=False)].groupby("Operator").size()

# Résumé statistique
events_summary = pd.DataFrame({
    "Handovers": handover,
    "Drop_Calls": drop,
    "Failures": failures
}).fillna(0).astype(int)

events_summary.to_csv(os.path.join(input_folder, "resume_stats_events.csv"), index=True)
print(f"✅ Résumé statistique événements sauvegardé dans {input_folder}")

# Détail complet des événements
events_detail = (
    df_all.groupby(["Operator", event_col])
    .size()
    .reset_index(name="Count")
    .pivot(index="Operator", columns=event_col, values="Count")
    .fillna(0)
    .astype(int)
)

events_detail.to_csv(os.path.join(input_folder, "resume_events_detail.csv"), index=True)
print(f"✅ Détail des événements sauvegardé dans {input_folder}")
