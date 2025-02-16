while IFS= read -r line; do
  if [[ $line != '#'* ]] fly secrets set "$line"
done <.env
