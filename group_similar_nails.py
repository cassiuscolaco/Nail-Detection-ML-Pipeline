import csv

# Adjustable tolerance values
height_tol_mm = 5.0  # group nails within ±1mm
weight_tol_g = 1.0   # group nails within ±0.1g

# Read nail measurements
nails = []
with open("nail_measurements.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nails.append({
            'image': row['Image'],
            'nail': int(row['NailNumber']),
            'length_mm': float(row['Length_mm']),
            'weight_g': float(row['Weight_g']),
        })

# Sort nails by length for easier grouping
nails.sort(key=lambda n: n['length_mm'])

groups = []
used = set()

for i, n1 in enumerate(nails):
    if i in used:
        continue
    group = [n1]
    used.add(i)
    for j in range(i + 1, len(nails)):
        if j in used:
            continue
        n2 = nails[j]
        # Check tolerances
        if abs(n1['length_mm'] - n2['length_mm']) <= height_tol_mm and abs(n1['weight_g'] - n2['weight_g']) <= weight_tol_g:
            group.append(n2)
            used.add(j)
    groups.append(group)

# Print groups
for idx, group in enumerate(groups, 1):
    print(f"\nGroup {idx} ({len(group)} nails):")
    for nail in group:
        print(f"  {nail['image']} nail#{nail['nail']} - {nail['length_mm']}mm, {nail['weight_g']}g")

# Optional: save groups to file
with open("nail_groups.txt", "w") as f:
    for idx, group in enumerate(groups, 1):
        f.write(f"Group {idx} ({len(group)} nails):\n")
        for nail in group:
            f.write(f"  {nail['image']} nail#{nail['nail']} - {nail['length_mm']}mm, {nail['weight_g']}g\n")
        f.write("\n")

print("\n[INFO] Grouping complete. Results saved to nail_groups.txt.")
