#!/bin/zsh
# wait until the Mac has room for a model job (free >= 35 %, swap <= 4.5 GB); prints the state; gives up after 10 min
for i in {1..60}; do
  free=$(memory_pressure | awk '/free percentage/ {print $5+0}')
  swap=$(sysctl -n vm.swapusage | awk '{gsub("M","",$6); print $6+0}')
  if (( free >= 35 && swap <= 4600 )); then echo "memory ok: ${free}% free, swap ${swap}M"; exit 0; fi
  echo "waiting: ${free}% free, swap ${swap}M"; sleep 10
done
echo "memory still tight: ${free}% free, swap ${swap}M"; exit 1
