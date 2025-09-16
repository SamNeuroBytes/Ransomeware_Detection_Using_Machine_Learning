import pandas as pd
import numpy as np

def generate_sample_data(n, is_ransomware):
    data = []

    for _ in range(n):
        if is_ransomware:
            cpu = np.random.uniform(70, 100)  
            memory = np.random.uniform(6001, 16000)
            disk = np.random.uniform(15.01, 500)
            network = np.random.uniform(3, 100)
            created = np.random.randint(101, 1000)
            deleted = np.random.randint(101, 1000)
            renamed = np.random.randint(101, 1000)
        else:
            cpu = np.random.uniform(0, 70)
            memory = np.random.uniform(0, 6000)
            disk = np.random.uniform(0, 15)
            network = np.random.uniform(0, 5)
            created = np.random.randint(0, 101)
            deleted = np.random.randint(0, 101)
            renamed = np.random.randint(0, 101)

        data.append({
            "CPU (%)": round(cpu, 2),
            "Memory (MB)": round(memory, 2),
            "Disk (MB/s)": round(disk, 2),
            "Network (Mbps)": round(network, 2),
            "Files Created": created,
            "Files Deleted": deleted,
            "Files Renamed": renamed,
            "is_ransomware": int(is_ransomware)
        })

    return data

# Generate 5,000 normal and 5,000 ransomware samples
normal_data = generate_sample_data(5000, is_ransomware=0)
ransom_data = generate_sample_data(5000, is_ransomware=1)

# Combine and save
df = pd.DataFrame(normal_data + ransom_data)
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle

df.to_csv("synthetic_ransomware_dataset.csv", index=False)
print("✅ Dataset created with 10,000 rows (based on handwritten ranges).")
