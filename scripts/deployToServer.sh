#!/bin/bash
if [ "$#" -lt 1 ]; then
echo "must pass docker registryImageAddress";
exit 1;
fi;

registryImageAddress=$1;

serviceName="baziChargeWebsite";

docker pull "$registryImageAddress"
if docker service inspect "$serviceName" ; then
    ##just update service image
    docker service update --with-registry-auth --image "$registryImageAddress" "$serviceName";
else
    ##create service and run it!
    docker service create --with-registry-auth --network mysql --replicas 1 --name "$serviceName" --publish 8081:80/tcp "$registryImageAddress";
fi;
