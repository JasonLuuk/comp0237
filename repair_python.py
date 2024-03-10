"""
Automated program repair ::
"""
import sys
import random
import argparse
from pathlib import Path
from pyggi.base import Patch, AbstractProgram
from pyggi.line import LineProgram
from pyggi.line import LineReplacement, LineInsertion, LineDeletion
from pyggi.tree import TreeProgram
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.algorithms import LocalSearch

class MyProgram(AbstractProgram):
    def compute_fitness(self, result, return_code, stdout, stderr, elapsed_time):
        import re
        # m = re.findall("runtime: ([0-9.]+)", stdout)

        if "runtime" in stdout:
            failed = re.findall("([0-9]+) failed", stdout)
            pass_all = len(failed) == 0
            failed = int(failed[0]) if not pass_all else 0
            result.fitness = failed
            # print((stdout))
            # print((stderr))
        else:
            # print((stdout))
            result.status = 'PARSE_ERROR'
            # quit()    

class MyLineProgram(LineProgram, MyProgram):
    pass

class MyTreeProgram(TreeProgram, MyProgram):
    pass

class MyTabuSearch(LocalSearch):
    def setup(self):
        self.tabu = []

    def get_neighbour(self, patch):
        var = 0
        while (var <= 10000):
            temp_patch = patch.clone()
            if len(temp_patch) > 0 and random.random() < 0.5:
                temp_patch.remove(random.randrange(0, len(temp_patch)))
            else:
                edit_operator = random.choice(self.operators)
                temp_patch.add(edit_operator.create(self.program, method="weighted"))
            if not any(item == temp_patch for item in self.tabu):
                self.tabu.append(temp_patch)
                break
            var = var + 1
        return temp_patch

    def is_better_than_the_best(self, fitness, best_fitness):
        return fitness < best_fitness

    def stopping_criterion(self, iter, fitness):
        return fitness == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PYGGI Bug Repair Example')
    parser.add_argument('--project_path', type=str, default='../sample/Triangle_bug_python')
    parser.add_argument('--mode', type=str, default='line')
    parser.add_argument('--epoch', type=int, default=30,
        help='total epoch(default: 30)')
    parser.add_argument('--iter', type=int, default=100,
        help='total iterations per epoch(default: 100)')
    args = parser.parse_args()
    assert args.mode in ['line', 'tree']

    if args.mode == 'line':
        program = MyLineProgram(args.project_path)
        tabu_search = MyTabuSearch(program)
        tabu_search.operators = [LineReplacement, LineInsertion, LineDeletion]
    elif args.mode == 'tree':
        program = MyTreeProgram(args.project_path)
        tabu_search = MyTabuSearch(program)
        tabu_search.operators = [StmtReplacement, StmtInsertion, StmtDeletion]

    result = tabu_search.run(warmup_reps=1, epoch=args.epoch, max_iter=args.iter, timeout=10)
    print("======================RESULT======================")
    print(result)
    with open(Path(args.project_path) / f"{args.mode}Result.txt", "w") as f:
        # only Patch __str__ has the patch details, not __repr__ so we need to convert to string
        to_write = [{k: str(v) if isinstance(v, Patch) else v for k, v in r.items()} for r in result]
        f.write(str(to_write))
    program.remove_tmp_variant()
