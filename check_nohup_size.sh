#!/bin/bash
file_path="./laoyue.out"

# 检查文件是否存在
while true; do
    if [ -f "$file_path" ]; then
        initial_size=$(du -s "$file_path" | cut -f1)
        sleep 7200

        current_size=$(du -s "$file_path" | cut -f1)

        if [ "$current_size" == "$initial_size" ]; then
            rm -f "$file_path"
            nohup python laoyue.py -d "SRC.txt" -z -n -m -f -a &
            break
        fi
    fi
    echo "laoyue.out文件打不开"
    sleep 360
done