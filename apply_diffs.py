import re, os
import argparse
from pathlib import Path
import astor, ast


def apply_diff(og, diff):
    ## Verification of line numbers
    og_lines = re.findall(r"\*\*\* ([0-9]+),([0-9]+) \*\*\*\*", diff)[0]
    modified_lines = re.findall(r"--- ([0-9]+),([0-9]+) ----", diff)[0]
    assert og_lines[0] == modified_lines[0]

    # All of our files have only one diff so we can always assume there's just one
    if "!" in diff:
        # Split diff for replacement
        before = re.findall(r" \*\*\*\*\n((?:.|\n)+?)\-\-\-", diff)[0].rstrip()
        after = re.findall(r" \-\-\-\-\n((?:.|\n)+?)$", diff)[0].rstrip()
        before = "\n".join([b[2:] for b in before.split("\n")])
        after = "\n".join([a[2:] for a in after.split("\n")])

        modified = og.replace(before, after)
        assert modified != og
        return modified

    else:
        # Diff is unified bc it's either addition or removal
        unified = re.findall(r" \-\-\-\-\n((?:.|\n)+?)$", diff)[0].rstrip()
        unified = unified.split("\n")

        before = [u for u in unified if u.startswith("-") or u.startswith(" ")]
        after = [u for u in unified if u.startswith("+") or u.startswith(" ")]
        before = "\n".join([b[2:] for b in before])
        after = "\n".join([a[2:] for a in after])

        modified = og.replace(before, after)
        assert modified != og
        return modified


def get_and_apply_all_diffs(og, project_path):
    tree_diffs = [*project_path.glob("diffs/tree/*.diff")]
    line_diffs = [*project_path.glob("diffs/line/*.diff")]

    # Apply every diff and save it as a modified python file

    for diff in tree_diffs:
        with open(diff) as f:
            diff_data = f.read()
            # Tree diffs have autoremoved whitespace and formatting due to how astor redumps parsed files
            new_og = astor.to_source(ast.parse(og))
            modified = apply_diff(new_og, diff_data)

            with open(project_path / "modified/tree" / diff.with_suffix(".py").name, "w") as f:
                f.write(modified)

    for diff in line_diffs:
        with open(diff) as f:
            diff_data = f.read()
            modified = apply_diff(og, diff_data)

            with open(project_path / "modified/line" / diff.with_suffix(".py").name, "w") as f:
                f.write(modified)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_path", type=str)

    args = parser.parse_args()
    project_path = Path(args.project_path)

    (project_path / "modified/tree").mkdir(parents=True, exist_ok=True)
    (project_path / "modified/line").mkdir(parents=True, exist_ok=True)

    # .keep file to keep the folder in git even if it's empty
    open(project_path / "modified/tree/.keep", "w").close()
    open(project_path / "modified/line/.keep", "w").close()

    # get last directory name
    project_name = project_path.parts[-1]

    with open(project_path / f"{project_name}.py") as f:
        og = f.read()

    get_and_apply_all_diffs(og, project_path)
