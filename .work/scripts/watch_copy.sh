#!/bin/bash
# Poll for .work/copy.txt, up to 20 minutes, 5s interval
D=/d/code/unitree-site/.work
for i in $(seq 1 240); do
  if [ -f "$D/copy.txt" ]; then
    echo "FOUND $(date -u +%FT%TZ) after ${i} polls" > "$D/copy-watch.status"
    exit 0
  fi
  sleep 5
done
echo "TIMEOUT $(date -u +%FT%TZ)" > "$D/copy-watch.status"
exit 1
