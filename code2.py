import os
import json
from pathlib import Path

# Current directory based on pwd output
base_dir = "/users/s011356/sitescope/configs/FileMonitors/files/files"

def extract_json_info(directory):
    """
    Go through all .json files in the directory and subdirectories,
    extract the filename (name without .json) and the file system path from inside.
    """
    results = []
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                # Full path to the json file
                json_path = os.path.join(root, file)
                
                # Extract name without .json extension
                name_without_ext = file[:-5]  # Removes '.json'
                
                # Try to parse the JSON and extract file system path
                try:
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                    
                    # Try common keys for file system path
                    file_path = None
                    
                    # Check various possible keys
                    if 'path' in data:
                        file_path = data['path']
                    elif 'filePath' in data:
                        file_path = data['filePath']
                    elif 'fileSystemPath' in data:
                        file_path = data['fileSystemPath']
                    elif 'monitorPath' in data:
                        file_path = data['monitorPath']
                    elif 'fileName' in data:
                        file_path = data['fileName']
                    else:
                        # Debug: show all keys
                        file_path = data.get('path', data.get('filePath', 'PATH_NOT_FOUND'))
                    
                    results.append({
                        'json_file': file,
                        'name': name_without_ext,
                        'full_path': json_path,
                        'file_system_path': file_path,
                        'all_keys': list(data.keys()) if file_path == 'PATH_NOT_FOUND' else None
                    })
                    
                except json.JSONDecodeError as e:
                    results.append({
                        'json_file': file,
                        'name': name_without_ext,
                        'full_path': json_path,
                        'file_system_path': f'JSON_ERROR: {e}',
                        'all_keys': None
                    })
                except Exception as e:
                    results.append({
                        'json_file': file,
                        'name': name_without_ext,
                        'full_path': json_path,
                        'file_system_path': f'ERROR: {e}',
                        'all_keys': None
                    })
    
    return results

# Execute the extraction
results = extract_json_info(base_dir)

# Print results in a readable format
print(f"Found {len(results)} JSON files:\n")
print("-" * 80)
print(f"{'Name':<35} {'File System Path':<45}")
print("-" * 80)

for r in results:
    name = r['name']
    path = r['file_system_path']
    if len(path) > 42:
        path = path[:39] + "..."
    print(f"{name:<35} {path:<45}")

print("-" * 80)

# Save as CSV for easier viewing
import csv
csv_path = "json_filesystem_paths.csv"

with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['json_file', 'name', 'full_path', 'file_system_path'])
    writer.writeheader()
    for r in results:
        writer.writerow({
            'json_file': r['json_file'],
            'name': r['name'],
            'full_path': r['full_path'],
            'file_system_path': r['file_system_path']
        })

print(f"\nCSV saved to: {csv_path}")
