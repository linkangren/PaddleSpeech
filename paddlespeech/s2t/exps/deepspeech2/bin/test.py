# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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
"""Evaluation for DeepSpeech2 model."""
from yacs.config import CfgNode

from paddlespeech.s2t.exps.deepspeech2.model import DeepSpeech2Tester as Tester
from paddlespeech.s2t.training.cli import default_argument_parser
from paddlespeech.s2t.utils.utility import print_arguments


def main_sp(config, args):
    exp = Tester(config, args)
    with exp.eval():
        exp.setup()
        exp.run_test()


def main(config, args):
    main_sp(config, args)


if __name__ == "__main__":
    parser = default_argument_parser()
    parser.add_argument(
        "--model_type", type=str, default='offline', help='offline/online')
    # save asr result to 
    parser.add_argument(
        "--result_file", type=str, help="path of save the asr result")
    parser.add_argument(
        '--nxpu',
        type=int,
        default=0,
        choices=[0, 1],
        help="if nxpu == 0 and ngpu == 0, use cpu.")
    args = parser.parse_args()
    print_arguments(args, globals())
    print("model_type:{}".format(args.model_type))

    # https://yaml.org/type/float.html
    config = CfgNode(new_allowed=True)
    if args.config:
        config.merge_from_file(args.config)
    if args.decode_cfg:
        decode_confs = CfgNode(new_allowed=True)
        decode_confs.merge_from_file(args.decode_cfg)
        config.decode = decode_confs
    if args.opts:
        config.merge_from_list(args.opts)
    config.freeze()
    print(config)
    if args.dump_config:
        with open(args.dump_config, 'w') as f:
            print(config, file=f)

    main(config, args)
