import pandas as pd
import glob, os

input_folder = r"C:\Users\ibraz\Downloads\Campagnes Plateau G-Net Track Pro\drive_test\processed"
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

# Détecter colonne des événements
if "EventType" in df_all.columns:
    event_col = "EventType"
elif "Event" in df_all.columns:
    event_col = "Event"
else:
    event_col = df_all.columns[0]

# Comptage fiabilité
handover = df_all[df_all[event_col].str.contains("handover", case=False, na=False)].groupby("Operator").size()
drop = df_all[df_all[event_col].str.contains("drop", case=False, na=False)].groupby("Operator").size()
failures = df_all[df_all[event_col].str.contains("fail|error|reject", case=False, na=False)].groupby("Operator").size()

events_summary = pd.DataFrame({"Handovers":handover, "Drop_Calls":drop, "Failures":failures}).fillna(0).astype(int)
events_summary.to_csv(os.path.join(input_folder, "resume_stats_events.csv"), index=True)

# Détail événements
events_detail = df_all.groupby(["Operator", event_col]).size().reset_index(name="Count").pivot(index="Operator", columns=event_col, values="Count").fillna(0).astype(int)
events_detail.to_csv(os.path.join(input_folder, "resume_events_detail.csv"), index=True)
