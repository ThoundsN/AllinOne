#!/usr/bin/bash


# cat /root/AllinOne/domains.txt | while read $line || [[ -n $line ]];
# do
#    python3 /root/AllinOne/allinone.py --domain=$p run
# done


while IFS="" read -r p || [ -n "$p" ]
do
  printf '%s\n' "$p"
  bash -c "python3 /root/AllinOne/allinone.py --domain=$p run"
done < /root/AllinOne/domains.txt 