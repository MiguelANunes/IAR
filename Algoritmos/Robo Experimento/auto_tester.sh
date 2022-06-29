INPUTS="./inputs"
for i in $(seq 0 4); do
    python3 GenerateData.py
    python3 Main.py -A -W 0 -I $i
    python3 Main.py -D -W 0 -I $i
    python3 Main.py -G -W 0 -I $i
done