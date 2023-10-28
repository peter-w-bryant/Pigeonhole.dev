import json
import os

def combine_json_files(file_path_1, file_path_2):
    with open(file_path_1) as f1:
        json_data_1 = json.load(f1)
    with open(file_path_2) as f2:
        json_data_2 = json.load(f2)

    # Combine entries that don't have the same values
    combined_entries = {}
    for key in set(json_data_1.keys()) | set(json_data_2.keys()):
        if key in json_data_1 and key in json_data_2:
            if json_data_1[key] != json_data_2[key]:
                combined_entries[key] = (json_data_1[key], json_data_2[key])
        else:
            if key in json_data_1:
                combined_entries[key] = json_data_1[key]
            else:
                combined_entries[key] = json_data_2[key]

    # Write combined entries to a new JSON file
    file_path = os.path.join(os.getcwd(), 'repo_scrapers', 'static_repo_data.json')
    with open(file_path, 'w') as f:
        json.dump(combined_entries, f, indent=4)

    return {"success": f"Combined entries from {file_path_1} and {file_path_2} into {file_path}"}

if __name__ == "__main__":
    file_path_1 = os.path.join(os.getcwd(), 'repo_scrapers', 'u4g.json')
    file_path_2 = os.path.join(os.getcwd(), 'repo_scrapers', 'old.json')
    combined_entries = combine_json_files(file_path_1, file_path_2)
