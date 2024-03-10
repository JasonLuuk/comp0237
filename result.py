

import re, os
import argparse
from pathlib import Path



def data_analysis(result, type, project_path):
    # Use RegEx to extract data from the results file
    fitness_evals = [*map(int, re.findall(r''''FitnessEval': ([0-9]+)''', result))]
    invalid_patches = [*map(int, re.findall(r''''InvalidPatch': ([0-9]+)''', result))]
    best_patches = re.findall(r''''BestPatch': ((?:["'].+?["'])|None), 'Success''', result)
    diffs = re.findall(r''''diff': ["']((?:.|\n)+?)["'], 'Time''', result)
    times = [*map(float, re.findall(r''''Time': ([0-9.]+)''', result))]

    # Find only valid patches
    valid_best_patches = [patch.strip('"').strip("'") for patch in best_patches if patch != "None"]

    # Calculations
    average_iterations = sum(fitness_evals) / len(fitness_evals)
    average_invalid = sum(invalid_patches) / len(invalid_patches)
    total_time = sum(times)
    average_time = total_time / len(times)

    total_minutes, total_seconds = divmod(total_time, 60)

    average_time_per_iteration = average_time / average_iterations

    # Print statistics
    print(f"Average Iterations Per Epoch: {average_iterations:.2f}")
    print(f"Average Invalid Patches Per Epoch: {average_invalid:.2f}")
    print(f"Average Percentage of Invalid Patches: {average_invalid / average_iterations * 100:.2f}%")
    print(f"Total Time: {total_minutes:.0f}m {total_seconds:.2f}s")
    print(f"Average Time Per Epoch: {average_time:.2f}s")
    print(f"Average Time Per Iteration: {average_time_per_iteration:.2f}s")
    print(f"Average Iterations Per Second: {1 / average_time_per_iteration:.2f}")

    # Print all unique patches
    print(f"Unique Best Patches: {len(set(valid_best_patches))}")
    if valid_best_patches:
        print("Best Patches:")
        print("\n".join(set(valid_best_patches)))

    # Save each diff
    for i, d in enumerate(diffs, start=1):
        if d == "None": continue
        with open(project_path / f"diffs/{type}/epoch{i}.diff", "w") as f:
            f.write(d)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_path", type=str)

    args = parser.parse_args()
    project_path = Path(args.project_path)

    (project_path / "diffs/tree").mkdir(parents=True, exist_ok=True)
    (project_path / "diffs/line").mkdir(parents=True, exist_ok=True)

    # .keep file to keep the folder in git even if it's empty
    open(project_path / "diffs/tree/.keep", "w").close()
    open(project_path / "diffs/line/.keep", "w").close()

    with open(project_path / "treeResult.txt") as f:
        tree_result = f.read().replace("\\n", "\n")
    
    with open(project_path / "lineResult.txt") as f:
        line_result = f.read().replace("\\n", "\n")


    print("Tree:")
    data_analysis(tree_result, "tree", project_path)
    print("\n")

    print("Line:")
    data_analysis(line_result, "line", project_path)
    