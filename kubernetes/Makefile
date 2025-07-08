NAME=world-headlines
NAMESPACE=rst0070
HELM_CHART=./helm

install:
	helm install $(NAME) $(HELM_CHART) \
	--namespace $(NAMESPACE) \
	--debug

upgrade:
	helm upgrade $(NAME) $(HELM_CHART) \
	--namespace $(NAMESPACE) \
	--debug 
