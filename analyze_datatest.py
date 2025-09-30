import pandas as pd
import glob, os
import matplotlib.pyplot as plt
import seaborn as sns

input_folder = r"C:\Users\ibraz\Downloads\Campagnes Plateau G-Net Track Pro\drive_test\processed"
graphs_folder = os.path.join(input_folder, "graphs")
os.makedirs(graphs_folder, exist_ok=True)

files = glob.glob(os.path.join(input_folder, "*_datatest_clean.csv"))
data = []

for file in files:
    df = pd.read_csv(file)
    operator = os.path.basename(file).split("_")[0]
    df["Operator"] = operator

    rename_map = {"TESTDOWNLINK":"Download_Mbps", "TESTUPLINK":"Upload_Mbps", "PINGAVG":"Ping_ms"}
    df = df.rename(columns=rename_map)
    keep_cols = ["Operator", "Download_Mbps", "Upload_Mbps", "Ping_ms"]
    df = df[[c for c in keep_cols if c in df.columns]]
    data.append(df)

df_all = pd.concat(data, ignore_index=True)
print("📊 Nombre total de tests data :", len(df_all))
print("Opérateurs trouvés :", df_all["Operator"].unique())

# Résumé statistique
stats = df_all.groupby("Operator").agg(
    Download_mean=("Download_Mbps","mean"), Download_median=("Download_Mbps","median"),
    Download_min=("Download_Mbps","min"), Download_max=("Download_Mbps","max"),
    Upload_mean=("Upload_Mbps","mean"), Upload_median=("Upload_Mbps","median"),
    Upload_min=("Upload_Mbps","min"), Upload_max=("Upload_Mbps","max"),
    Ping_mean=("Ping_ms","mean"), Ping_median=("Ping_ms","median"),
    Ping_min=("Ping_ms","min"), Ping_max=("Ping_ms","max")
).round(2)

stats.to_csv(os.path.join(graphs_folder, "resume_stats_datatest.csv"))
print(f"✅ Résumé statistique data sauvegardé dans {graphs_folder}")

# Graphiques : boxplots et barplots
for kpi in ["Download_Mbps","Upload_Mbps","Ping_ms"]:
    if kpi in df_all.columns:
        plt.figure(figsize=(10,6))
        sns.boxplot(x="Operator", y=kpi, data=df_all)
        plt.title(f"Comparaison {kpi} par opérateur")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.savefig(os.path.join(graphs_folder, f"boxplot_{kpi.lower()}.png"))
        plt.close()

        mean_values = df_all.groupby("Operator")[kpi].mean()
        plt.figure(figsize=(8,5))
        sns.barplot(x=mean_values.index, y=mean_values.values)
        plt.title(f"{kpi} moyen par opérateur")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.savefig(os.path.join(graphs_folder, f"barplot_{kpi.lower()}.png"))
        plt.close()

# Optionnel : CDF Download
plt.figure(figsize=(8,6))
sns.ecdfplot(data=df_all, x="Download_Mbps", hue="Operator")
plt.title("CDF – Débit descendant par opérateur")
plt.xlabel("Débit (Mbps)")
plt.ylabel("Probabilité cumulée")
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig(os.path.join(graphs_folder,"cdf_download.png"))
plt.close()
