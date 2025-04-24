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
print(f"Metadata:\n {sample.metadata}\n")
print(f"AMR annotations (deepARG):\n {sample.get_amr_annotations()}")
print(f"AMR annotations (megares):\n {sample.get_amr_annotations(mode='megares')}")
print(f"AMR annotations (vfdb):\n {sample.get_amr_annotations(mode='vfdb')}")
print(f"MAGs:\n {sample.mags}\n")
