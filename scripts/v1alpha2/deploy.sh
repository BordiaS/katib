#!/bin/bash

# Copyright 2018 The Kubeflow Authors.
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

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

SCRIPT_ROOT=$(dirname ${BASH_SOURCE})/../..

cd ${SCRIPT_ROOT}
kubectl apply -f manifests/v1alpha2/0-namespace.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/crds.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/rbac.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/mcrbac.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/service.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/secret.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/trialTemplateConfigmap.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/metricsControllerConfigMap.yaml
kubectl apply -f manifests/v1alpha2/katib-controller/katib-controller.yaml
kubectl apply -f manifests/v1alpha2/katib/manager/service.yaml
kubectl apply -f manifests/v1alpha2/katib/manager/deployment.yaml
kubectl apply -f manifests/v1alpha2/katib/pv/pv.yaml
kubectl apply -f manifests/v1alpha2/katib/pv/pvc.yaml
kubectl apply -f manifests/v1alpha2/katib/db/secret.yaml
kubectl apply -f manifests/v1alpha2/katib/db/deployment.yaml
kubectl apply -f manifests/v1alpha2/katib/db/service.yaml
cd - > /dev/null
