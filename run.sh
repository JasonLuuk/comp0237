if [ -z "$1" ]; then
    echo "Error: Missing the name"
    exit 1
fi

if ! [ -d "./$1" ]; then
    echo "Error: Invalid bug name"
    exit 1
fi


python3 ./repair_python.py --project_path ./$1 --mode line --epoch 20 --iter 200
python3 ./repair_python.py --project_path ./$1 --mode tree --epoch 20 --iter 200
python3 ./result.py --project_path ./$1 > ./$1/results.txt
python3 ./apply_diffs.py --project_path ./$1
