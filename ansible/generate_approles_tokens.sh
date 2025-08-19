#!/bin/bash

# Get JSON entry for ids
# Get JSON entry for ids secrets
# Get role name

# Retrieve from JSON ids, the results.stdout.data.role_id
# - Loop on results 
# - In the Loop retireve result.stdout.data.role_id
# - Put each iteration in map with role name
# Retrieve from JSON ids, the results.stdout.data.secret_id
# - Loop on results 
# - In the Loop retireve result.stdout.data.secret_id
# - Put each iteration in map with role name

# In file print literraly role name role_id and secret_id
# then Loop on the maps 
# - In each iteration print role name, role_id and secret_id with space in a file

roles_ids_file="$1"
secrets_ids_file="$2"
output_file="$3"

mkdir -p "$(dirname "$output_file")"

# Extraction role_id per role
declare -A role_to_roleid
while IFS=" " read -r role role_id; do
  role_to_roleid["$role"]="$role_id"
done < <(jq -r '.results[] | "\(.item.role) \((.stdout | fromjson).data.role_id)"' "$roles_ids_file")

# Extraction secret_id per role
declare -A role_to_secretid
while IFS=" " read -r role secret_id; do
  role_to_secretid["$role"]="$secret_id"
done < <(jq -r '.results[] | "\(.item.role) \((.stdout | fromjson).data.secret_id)"' "$secrets_ids_file")

# Header
echo -e "id\ttoken" > "$output_file"

# Writting role name and token in file
for role in "${!role_to_roleid[@]}"; do
  role_id="${role_to_roleid[$role]}"
  secret_id="${role_to_secretid[$role]}"
  token=$(docker exec vault vault write -format=json auth/approle/login \
    role_id="$role_id" \
    secret_id="$secret_id" | jq -r '.auth.client_token')
  #auth.client_token
  echo -e "${role}\t${token}" >> "$output_file"
done

echo "File generated : $output_file"




