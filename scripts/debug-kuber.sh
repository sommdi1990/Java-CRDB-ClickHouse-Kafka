cat <<'EOF' > k8s-full-debug.sh
#!/bin/bash

OUT="k8s-debug-$(date +%Y%m%d-%H%M%S).log"

echo "===== CLUSTER INFO =====" > $OUT
kubectl cluster-info >> $OUT 2>&1
kubectl version >> $OUT 2>&1

echo -e "\n===== NODES =====" >> $OUT
kubectl get nodes -o wide >> $OUT 2>&1
kubectl describe nodes >> $OUT 2>&1

echo -e "\n===== NAMESPACES =====" >> $OUT
kubectl get ns >> $OUT 2>&1

echo -e "\n===== ALL RESOURCES ALL NAMESPACES =====" >> $OUT
kubectl get all -A -o wide >> $OUT 2>&1

echo -e "\n===== INGRESS =====" >> $OUT
kubectl get ingress -A >> $OUT 2>&1

echo -e "\n===== SERVICES =====" >> $OUT
kubectl get svc -A >> $OUT 2>&1

echo -e "\n===== PVC =====" >> $OUT
kubectl get pvc -A >> $OUT 2>&1

echo -e "\n===== RESOURCE QUOTAS =====" >> $OUT
kubectl get resourcequota -A >> $OUT 2>&1
kubectl describe resourcequota -A >> $OUT 2>&1

echo -e "\n===== EVENTS =====" >> $OUT
kubectl get events -A --sort-by=.metadata.creationTimestamp >> $OUT 2>&1

echo -e "\n===== HELM RELEASES =====" >> $OUT
helm list -A >> $OUT 2>&1

echo -e "\n===== VALIDATING WEBHOOKS =====" >> $OUT
kubectl get validatingwebhookconfigurations >> $OUT 2>&1

echo -e "\n===== INGRESS NGINX STATUS =====" >> $OUT
kubectl get pods -n ingress-nginx -o wide >> $OUT 2>&1
kubectl get svc -n ingress-nginx >> $OUT 2>&1

echo -e "\n===== PROBLEMATIC POD LOGS =====" >> $OUT
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  for pod in $(kubectl get pods -n $ns --field-selector=status.phase!=Running,status.phase!=Succeeded -o jsonpath='{.items[*].metadata.name}'); do
    echo -e "\n--- Logs for $ns/$pod ---" >> $OUT
    kubectl logs -n $ns $pod --all-containers=true --tail=200 >> $OUT 2>&1
  done
done

echo "Debug file created: $OUT"
EOF
