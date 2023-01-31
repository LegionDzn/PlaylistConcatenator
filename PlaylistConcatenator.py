import os
import json
def print_ascii_text(text):
    print("_" * (len(text) + 4))
    print("| " + text + " |")
    print("-" * (len(text) + 4))
    print("\n")
    print('Playlist files are typically located at \n"C:\Program Files\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\Saved\SaveGames\Playlists"\nFor online playlists you must download them first to create a local file.\n\n')
print_ascii_text("LegionDzn's Playlist Merge Tool")
def merge_scenario_lists(file1, file2, consistent_play_count=None):
    with open(file1, 'r') as f1:
        data1 = json.load(f1)
    with open(file2, 'r') as f2:
        data2 = json.load(f2)

    scenario_list = data1["scenarioList"] + data2["scenarioList"]
    scenario_list = list({v['scenario_Name']:v for v in scenario_list}.values())

    data1["scenarioList"] = scenario_list
    data1["playlistName"] = f"{data1['playlistName']} & {data2['playlistName']} Merged"
    data1["description"] = f"This is a merged scenario list of {data1['playlistName']} & {data2['playlistName']} Created using LegionDzn's playlist merge tool."
    data1["playlistId"] = 123456
    data1["authorName"] = "LegionDzn"
    if consistent_play_count is not None:
        for scenario in data1["scenarioList"]:
            scenario["play_Count"] = consistent_play_count

    return data1

file1 = input("Enter the first file location: (You can also drag and drop, which is easier.) ").strip('"')
file2 = input("Enter the second file location: (You can also drag and drop, which is easier.) ").strip('"')

use_consistent_play_count = input("Do you want to set a consistent play count for the merged scenarios (y/n)? ")
consistent_play_count = int(input("What should the play count be? ")) if use_consistent_play_count.lower() == "y" else None

merged_data = merge_scenario_lists(file1, file2, consistent_play_count)

sort_alphabetically = input("Do you want to sort the scenarios alphabetically (y/n)? ")
if sort_alphabetically.lower() == "y":
    merged_data['scenarioList'].sort(key=lambda x: x['scenario_Name'])

if merged_data["scenarioList"]:
    max_scenario_name_length = max(len(scenario["scenario_Name"]) for scenario in merged_data["scenarioList"])
    print("scenario_Name" + " " * (max_scenario_name_length - len("scenario_Name")) + "\tplay_Count")
    for scenario in merged_data["scenarioList"]:
        print(scenario["scenario_Name"] + " " * (max_scenario_name_length - len(scenario["scenario_Name"])) + "\t\t" + str(scenario["play_Count"]))
else:
    print("The merged scenario list is empty.")

print(f"Total scenarios: {len(merged_data['scenarioList'])}")


script_dir = os.path.dirname(os.path.abspath(__file__))
merged_data = merge_scenario_lists(file1, file2, consistent_play_count)
merged_file_path = os.path.join(script_dir, f"{merged_data['playlistName']}_merged.json")
with open(merged_file_path, "w") as f:
    json.dump(merged_data, f, indent=2)
    print("File created at " + merged_file_path)
