rm outputs/*
rm Imagens/*
for i in $(seq 0 4); do
    python3 GenerateData.py
    python3 Main.py -A -R -W 0 -I $i
    python3 Main.py -D -R -W 0 -I $i
    python3 Main.py -G -R -W 0 -I $i
    /bin/bash clean.sh
done