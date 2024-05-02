nvcc --version
nvidia-smi
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3
eval "$(/root/miniconda3/bin/conda shell.bash hook)" 
conda init
conda env update
conda activate gaussian_splatting

# python train.py -s ./dataset/Proyecto_test/