The Katib results can be replicated for MNISt code running the following steps sequentially

ibmcloud login -a https://cloud.ibm.com
ibmcloud ks region-set us-south
ibmcloud ks cluster-config mycluster-nyuclass
export KUBECONFIG=/home/bordia/.bluemix/plugins/container-service/clusters/mycluster-nyuclass/kube-config-hou02-mycluster-nyuclass.yml

kubectl get nodes
kubectl cluster-info
export KUBEFLOW_SRC=~/KubeFlow
mkdir ${KUBEFLOW_SRC}
cd ${KUBEFLOW_SRC}
export KUBEFLOW_TAG=v0.4.1
curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash
ibmcloud plugin update --all -r ‘IBM Cloud’
export KS_VER=0.13.1
export KS_PKG=ks_${KS_VER}_linux_amd64
wget -O /tmp/${KS_PKG}.tar.gz https://github.com/ksonnet/ksonnet/releases/download/v${KS_VER}/${KS_PKG}.tar.gz
mkdir -p ${HOME}/bin
tar -xvf /tmp/$KS_PKG.tar.gz -C ${HOME}/bin
ks_0.13.1_linux_amd64/CHANGELOG.md
ks_0.13.1_linux_amd64/CODE-OF-CONDUCT.md
ks_0.13.1_linux_amd64/CONTRIBUTING.md
ks_0.13.1_linux_amd64/LICENSE
ks_0.13.1_linux_amd64/README.md
ks_0.13.1_linux_amd64/ks
export PATH=$PATH:${HOME}/bin/$KS_PKG
export KFAPP=nyu-kf
${KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform none
cd ${KFAPP}
${KUBEFLOW_SRC}/scripts/kfctl.sh generate k8s
${KUBEFLOW_SRC}/scripts/kfctl.sh apply k8s

kubectl config set-context $(kubectl config current-context) --namespace=kubeflow
cd k8s
kubectl create -f pv-katib.yaml
https://github.com/BordiaS/katib
cd katib/examples/v1alpha1
kubectl create -f bayseopt-mnist.yaml

kubectl -n kubeflow describe studyjobs

kubectl port-forward -n kubeflow `kubectl get pods -n kubeflow --selector=service=ambassador -o jsonpath='{.items[0].metadata.name}'` 8080:80

















