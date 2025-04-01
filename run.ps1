# run using the local .github_token file
conda activate metrix
$env:GITHUB_USERNAME = "joanroig"
$env:DEBUG_MODE = "true"
python ./src/main.py