#/bin/zsh

while IFS= read -r line; do
  if [[ $line == 'POST'* ]] fly secrets set "$line"
done <.env
