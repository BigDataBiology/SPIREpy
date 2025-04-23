import os

from spirepy import Study
from spirepy.metadata import cluster_metadata

data_folder = "/home/alexandre/Documents/projects/micro_fr_pred/data"
study_name = "Lloyd-Price_2019_HMP2IBD"

study = Study(study_name, os.path.join(data_folder, study_name))
sample = study.samples[-1]

# Tests

print("###Global###")
print(f"Clusters:\n {cluster_metadata()}\n")

print("###Study ###")
print(f"Name: {study.name}\n")
print(f"Metadata:\n {study.metadata}\n")

print("###Sample ###")
print(f"Name: {sample.id}\n")
print(f"Metadata: {sample.metadata}\n")
print(f"MAGs:\n {sample.mags}\n")
# print(f"Abundances:\n {sample.get_abundances()}\n")
# print(f"Manifest:\n {sample.manifest}\n")

# sample.manifest.to_csv(f"{sample.out_folder}sample_manifest.csv")
