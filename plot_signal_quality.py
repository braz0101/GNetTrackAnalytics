import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

input_folder = r"C:\Users\ibraz\Downloads\Campagnes Plateau G-Net Track Pro\drive_test\processed"
graphs_folder = os.path.join(input_folder, "graphs")
os.makedirs(graphs_folder, exist_ok=True)

# Charger tous les fichiers *_log_clean.csv
files = glob.glob(os.path.join(input_folder, "*_log_clean.csv"))
data = []

for file in files:
    df = pd.read_csv(file)
    operator = os.path.basename(file).split("_")[0]
    df["Operator"] = operator
    data.append(df)

df_all = pd.concat(data, ignore_index=True)
print("📊 Nombre total de mesures :", len(df_all))
print("Opérateurs trouvés :", df_all["Operator"].unique())

# Colonnes KPI radio
kpi_columns = ["Level", "SNR", "CQI"]

# Résumé statistique
stats = df_all.groupby("Operator")[kpi_columns].agg(["mean","median","min","max"]).round(2)
stats.to_csv(os.path.join(graphs_folder, "resume_stats_radio.csv"))
print(f"✅ Résumé statistique radio sauvegardé dans {graphs_folder}")

# Graphiques : boxplot et barplot moyenne
for kpi in kpi_columns:
    if kpi in df_all.columns:
        # Boxplot
        plt.figure(figsize=(10,6))
        sns.boxplot(x="Operator", y=kpi, data=df_all)
        plt.title(f"Comparaison {kpi} par opérateur")
        plt.ylabel(kpi)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.savefig(os.path.join(graphs_folder, f"boxplot_{kpi.lower()}.png"))
        plt.close()

        # Barplot moyenne
        mean_values = df_all.groupby("Operator")[kpi].mean()
        plt.figure(figsize=(8,5))
        sns.barplot(x=mean_values.index, y=mean_values.values)
        plt.title(f"{kpi} moyen par opérateur")
        plt.ylabel(f"{kpi} moyen")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.savefig(os.path.join(graphs_folder, f"barplot_{kpi.lower()}.png"))
        plt.close()

# Scatter RSRP vs SNR
if "Level" in df_all.columns and "SNR" in df_all.columns:
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df_all, x="Level", y="SNR", hue="Operator", alpha=0.5)
    plt.title("Relation RSRP vs SNR par opérateur")
    plt.xlabel("RSRP (dBm)")
    plt.ylabel("SNR (dB)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(os.path.join(graphs_folder, "scatter_rsrp_snr.png"))
    plt.close()

print(f"✅ Tous les graphiques radio sauvegardés dans {graphs_folder}")
