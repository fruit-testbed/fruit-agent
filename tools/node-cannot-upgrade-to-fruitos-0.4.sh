# Below command generates a list of nodes that cannot be
# upgraded to FruitOS 0.4 since their root partitions
# are not large enough. They should be upgraded by flashing
# the SSD.

fruit-cli monitor \
  | sh $(dirname $0)/../JSON.sh \
  | grep '"volumes","/media/root-ro","size"' \
  | sed 's/","volumes","\/media\/root-ro","size"\]//g' \
  | sed 's/\["//g' \
  | sed 's/"//g' \
  | awk '{if ($2 < 400000) print $1 " " $2}'
