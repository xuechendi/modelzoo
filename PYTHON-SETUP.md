# Software setup

The get more info about software setup and dependencies, please visit our developer doc page [here](https://docs.cerebras.net/en/latest/wsc/getting-started/setup-environment.html).

## Cerebras Wafer-Scale Cluster instructions

After installing all the Cerebras packages distributed in the CSoft platform, to support all the functionalities in Model Zoo, please install other external packages to your python environment.

For PyTorch environment, please install the packages by running:

```bash
pip install -r requirements_cb_pt.txt
```

**NOTE:** The rest of this guide concerns to *GPU Python environment only*.

Along with the Cerebras Wafer-Scale Cluster, the Model Zoo allows for models to be run on GPUs as well. To run the model code on a GPU, certain packages need to be installed. This is usually best done in a virtual environment using ``virtualenv`` or `conda`. We provide instructions for setting up a ``virtualenv`` in this setup instructions.

Follow along below for setting up a GPU environment setup.

## GPU instructions

### CUDA requirements

To run on a GPU, the CUDA libraries must be installed on the system. This includes both the CUDA toolkit as well as the cuDNN libraries. To install these packages, please follow the instructions provided on the [CUDA website](https://developer.nvidia.com/cuda-zone). And make sure to also include the [cuDNN library installation](https://developer.nvidia.com/cudnn).

### PyTorch GPU setup

Currently, the Model Zoo only supports PyTorch version `1.11` which requires CUDA version `10.1/10.2`.

Once all the CUDA requirements are installed, create a `virtualenv` on your system, with Python version `3.8` or newer, activate the `virtualenv` and install the packages needed for running PyTorch models using the below steps:

```bash
    virtualenv -p python3.8 /path/to/venv_gpu 
    source /path/to/venv_pt/bin/activate
    pip install -r requirements_gpu_pt.txt
```

To test if PyTorch is able to properly access the GPU, start a Python session through the virtual environment create above and run the following commands:

```bash
    $ source /path/to/venv_pt/bin/activate
    $ python
    >>> import torch
    >>> torch.__version__
    1.11 # Confirm that the PT version is 1.11
    >>> torch.cuda.is_available()
    True # Should return True
    >>> torch.cuda.device_count()
    1 # Number of devices present
    >>> torch.cuda.get_device_name(0)
    # Should return the proper GPU type
```

**Note:** While it is not needed for GPU/CPU run, we use PyTorch/XLA in our container because we depend on XLA backend [PyTorch/XLA website](https://github.com/pytorch/xla).

### CUDA troubleshoot

If you do not see GPU returned in the setup verification steps mentioned above, then you can troubleshoot by verifying if all the CUDA libraries are correctly loaded, otherwise the output would indicate which CUDA libraries did not load correctly.

Note that some methods of installing CUDA `10.1/10.2` require a installing the cuBLAS library from CUDA `10.2`, while the rest of the CUDA libraries are from version `10.1`.
This may require adding the path to the `lib64` directory in both installations to the `LD_LIBRARY_PATH` variable. You can do it by following the below steps:

```bash
export CUDA_VERSION=cuda-10.1

# Add /usr/local/${CUDA_VERSION}/lib64 to your LD_LIBRARY_PATH.
export LD_LIBRARY_PATH=/usr/local/${CUDA_VERSION}/lib64:$LD_LIBRARY_PATH

# Add /usr/local/${CUDA_VERSION}/extras/CUPTI/lib64 to your LD_LIBRARY_PATH.
export LD_LIBRARY_PATH=/usr/local/${CUDA_VERSION}/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Add /usr/local/cuda-10.2/lib64/ to your LD_LIBRARY_PATH.
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64/
```
