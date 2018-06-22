fruit-cli monitor \
  | sh $(dirname $0)/../JSON.sh \
  | grep '"volumes","/media/root-ro","free"' \
  | sed 's/","volumes","\/media\/root-ro","free"\]//g' \
  | sed 's/\["//g' \
  | sed 's/"//g' \
  | awk '{print $2 " " $1}'
