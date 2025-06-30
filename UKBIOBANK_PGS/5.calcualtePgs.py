import os
import subprocess
import shutil

weights_dir = 'UKBIOBANK_WEIGHTS/'
output_dir = 'UKBIOBANK_RESULTS/'
vcf_data_path = 'plink_format_vcf/merged'

folders = os.listdir(output_dir)
for f in folders:
    p = os.path.join(output_dir, f)
    shutil.rmtree(p)

for w in os.listdir(weights_dir):
    weight_path = os.path.join(weights_dir, w, 'plink_weights.txt')
    output_subdir = os.path.join(output_dir, w)

    if not os.path.exists(weight_path):
        print(f"Weights file does not exist {w}, pomijam.")
        continue

    if os.path.exists(output_subdir):
        shutil.rmtree(output_subdir)
    os.makedirs(output_subdir, exist_ok=True)

    output_file = os.path.join(output_subdir, 'pgs')

    cmd = [
        'plink2',
        '--bfile', vcf_data_path,
        '--score', weight_path, '1', '2', '3', 'header', 'list-variants',
        '--out', output_file
    ]

    print("Running... :", " ".join(cmd))

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error calculating PGS for {w}, continuing anyway.")
        print("PLINK error message:")
        print(e.stderr)
    print("\n\n")
