import pandas as pd
import glob
import os

# Dossier contenant les fichiers bruts
input_folder = r"C:\Users\ibraz\Downloads\Campagnes Plateau G-Net Track Pro\drive_test\raw_logs"
output_folder = r"C:\Users\ibraz\Downloads\Campagnes Plateau G-Net Track Pro\drive_test\processed"

os.makedirs(output_folder, exist_ok=True)

# Chercher tous les fichiers .txt
files = glob.glob(os.path.join(input_folder, "*.txt"))

for file in files:
    print(f"📂 Traitement de {file} ...")

    # Charger
    df = pd.read_csv(file, sep=r'\t+', engine="python")

    # Ajouter le nom du fichier comme identifiant
    df["SourceFile"] = os.path.basename(file)

    # Remplacer les valeurs manquantes ("-") par NaN
    df.replace("-", pd.NA, inplace=True)

    # Convertir certaines colonnes numériques
    for col in ["Level", "Qual", "SNR", "CQI", "LTERSSI", "Altitude", "Distance", "ARFCN"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sauvegarder en CSV propre
    out_file = os.path.join(output_folder, os.path.basename(file).replace(".txt", "_clean.csv"))
    df.to_csv(out_file, index=False)
    print(f"✅ Fichier nettoyé sauvegardé : {out_file}")
