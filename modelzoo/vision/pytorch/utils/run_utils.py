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

import os

from modelzoo import CSOFT_PACKAGE, CSoftPackage


def get_default_inis():
    return {
        "ws_cv_auto_inis": True,
        "ws_opt_target_max_actv_wios": 16,
        "ws_opt_max_wgt_port_group_size": 8,
        "ws_run_memoize_actv_mem_mapping": True,
        "ws_opt_bidir_act": False,
        "ws_variable_lanes": True,
        "ws_matmul_half_prec_acc_len": 0,
        "ws_dmatmul_half_prec_acc_len": 0,
    }


def update_runconfig_debug_args_path(params, default_inis_dict):
    if CSOFT_PACKAGE != CSoftPackage.NONE:
        from cerebras_appliance.run_utils import (
            DebugArgs,
            set_ini,
            write_debug_args,
        )

        if not params["runconfig"].get("debug_args_path"):
            debug_args = DebugArgs()
            set_ini(debug_args, **default_inis_dict)

            # in the case debug_args_path is not set
            # create a default debug_args file in the debug_args_dir
            debug_args_path = os.path.join(
                params["runconfig"]["model_dir"], ".debug_args.proto"
            )
            write_debug_args(debug_args, debug_args_path)
            params["runconfig"]["debug_args_path"] = debug_args_path
