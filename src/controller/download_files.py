import os

from config import ROOT_PATH
from database.models.sample import get_sample

base_sample_result_folder = f"{ROOT_PATH}pipeline/Phenotypes_Finder/result/Trimmomatic/"
base_sample_sheet_folder = f"{ROOT_PATH}pipeline/Phenotypes_Finder/result/SNP_Sheet/"
def download_file(file_type, sample_uuid, gene):
    sample_result_folder = f"{base_sample_result_folder}{sample_uuid}/{gene}"
    sample_sheet_folder = f"{base_sample_sheet_folder}{sample_uuid}/{gene}"
    sample_name = get_sample(sample_uuid)['name']
    file_name = ''
    if file_type == "BAM":
        file = os.path.join(sample_result_folder,[f for f in os.listdir(sample_result_folder) if f.endswith("_sorted.bam")][0])
        file_name = f"{sample_name}_{gene}_sorted.bam"
    if file_type == "VCF":
        file = os.path.join(sample_result_folder,[f for f in os.listdir(sample_result_folder) if f.endswith("_test.vcf.gz")][0])
        file_name = f"{sample_name}_{gene}.vcf.gz"
    if file_type == "FASTA":
        file = os.path.join(sample_result_folder,[f for f in os.listdir(sample_result_folder) if f.endswith("_new_consensus.fasta")][0])
        file_name = f"{sample_name}_{gene}_aligned.fasta"
    if file_type == "CSV":
        file = os.path.join(sample_sheet_folder,[f for f in os.listdir(sample_sheet_folder) if f.endswith(".csv")][0])
        file_name = f"{sample_name}_{gene}_.csv"
    if file_type == "XLSX":
        file = os.path.join(sample_sheet_folder,[f for f in os.listdir(sample_sheet_folder) if f.endswith(".xlsx")][0])
        file_name = f"{sample_name}_{gene}_.xlsx"
    return {'path': file, 'file_name': file_name}
