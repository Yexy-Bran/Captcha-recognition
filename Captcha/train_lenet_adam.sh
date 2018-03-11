#!/usr/bin/env sh
set -e

./build/tools/caffe train \
    --solver=examples/Captcha/lenet_solver_adam.prototxt \
    --snapshot=examples/Captcha/lenet_iter_4182.solverstate $@
