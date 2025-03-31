# run using the local .github_token file
conda activate metrix
$env:GITHUB_USERNAME = "octocat"
$env:DEBUG = "true"
python ./src/main.py