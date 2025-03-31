# rebuild conda environment
conda deactivate
conda env remove -n metrix -y
conda env create -f environment.yml
conda activate metrix
# install git hooks
git config core.hooksPath .githooks