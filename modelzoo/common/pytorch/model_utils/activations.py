# Copyright 2022 Cerebras Systems.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This code is adapted from
# https://github.com/huggingface/transformers/blob/master/src/transformers/activations.py
#
# Copyright 2022 Cerebras Systems.
#
# Copyright 2020 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

import torch
from packaging import version
from torch import nn

# TODO: Figure logging
# from .utils import logging
# logger = logging.get_logger(__name__)


def _gelu_python(x):
    """
    Original Implementation of the GELU activation function in Google BERT repo when initially created. For
    information: OpenAI GPT's GELU is slightly different (and gives slightly different results): 0.5 * x * (1 +
    torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3)))) This is now written in C in nn.functional
    Also see the Gaussian Error Linear Units paper: https://arxiv.org/abs/1606.08415
    """
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))


def gelu_new(x):
    """
    Implementation of the GELU activation function currently in Google BERT repo (identical to OpenAI GPT). Also see
    the Gaussian Error Linear Units paper: https://arxiv.org/abs/1606.08415
    """
    return (
        0.5
        * x
        * (
            1.0
            + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x * x * x))
        )
    )


if version.parse(torch.__version__) < version.parse("1.4"):
    gelu = _gelu_python
else:
    gelu = nn.functional.gelu


def gelu_fast(x):
    return (
        0.5
        * x
        * (1.0 + torch.tanh(x * 0.7978845608 * (1.0 + 0.044715 * x * x)))
    )


def quick_gelu(x):
    return x * torch.sigmoid(1.702 * x)


def squared_gelu(x):
    g = gelu(x)
    return g * g


def _silu_python(x):
    """
    See Gaussian Error Linear Units (Hendrycks et al., https://arxiv.org/abs/1606.08415) where the SiLU (Sigmoid Linear
    Unit) was originally introduced and coined, and see Sigmoid-Weighted Linear Units for Neural Network Function
    Approximation in Reinforcement Learning (Elfwing et al., https://arxiv.org/abs/1702.03118) and Swish: a Self-Gated
    Activation Function (Ramachandran et al., https://arxiv.org/abs/1710.05941v1) where the SiLU was experimented with
    later.
    """
    return x * torch.sigmoid(x)


if version.parse(torch.__version__) < version.parse("1.7"):
    silu = _silu_python
else:
    silu = nn.functional.silu


def _mish_python(x):
    """
    See Mish: A Self-Regularized Non-Monotonic Activation Function (Misra., https://arxiv.org/abs/1908.08681). Also
    visit the official repository for the paper: https://github.com/digantamisra98/Mish
    """
    return x * torch.tanh(nn.functional.softplus(x))


if version.parse(torch.__version__) < version.parse("1.9"):
    mish = _mish_python
else:
    mish = nn.functional.mish


def linear_act(x):
    return x


# GLU bivariate Activations implementation
def glu_bivariate_base_fn(x1, x2, activation_fn):
    assert (
        x1.shape == x2.shape
    ), "GLU activation inputs must have the same shape"
    return x1 * activation_fn(x2)


def liglu(x1, x2):
    identity = lambda x: x
    return glu_bivariate_base_fn(x1, x2, identity)


def geglu(x1, x2):
    return glu_bivariate_base_fn(x1, x2, gelu)


def reglu(x1, x2):
    return glu_bivariate_base_fn(x1, x2, nn.functional.relu)


def swiglu(x1, x2):
    return glu_bivariate_base_fn(x1, x2, nn.functional.silu)


GLU_ACTIVATIONS = {
    "liglu",
    "geglu",
    "reglu",
    "swiglu",
}

ACT2FN = {
    "relu": nn.functional.relu,
    "leaky_relu": nn.functional.leaky_relu,
    "silu": silu,
    "swish": silu,
    "gelu": gelu,
    "tanh": torch.tanh,
    "gelu_new": gelu_new,
    "gelu_fast": gelu_fast,
    "quick_gelu": quick_gelu,
    "squared_gelu": squared_gelu,
    "mish": mish,
    "linear": linear_act,
    "sigmoid": torch.sigmoid,
    "relu6": nn.functional.relu6,
    "liglu": liglu,
    "geglu": geglu,
    "reglu": reglu,
    "swiglu": swiglu,
    None: linear_act,
}


def get_activation(activation):
    if callable(activation):
        return activation
    if activation is not None:
        activation = activation.lower()
    if activation in ACT2FN:
        return ACT2FN[activation]
    else:
        raise KeyError(
            f"function {activation} not found in ACT2FN mapping {list(ACT2FN.keys())}"
        )


def is_glu_activation(activation):
    if hasattr(activation, "is_glu_activation"):
        return getattr(activation, "is_glu_activation")
    if isinstance(activation, str):
        activation = activation.lower()
    return activation in GLU_ACTIVATIONS
