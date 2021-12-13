
deps:
	apt install pip
	pip install rsa
path:
	echo "export PYTHONPATH=$(shell pwd)/service" >> $(HOME)/.bashrc
	echo "export SIGNER_PATH=$(shell pwd)/service" >> $(HOME)/.bashrc
	echo "export PRIVATE_KEY=$(shell pwd)/private_key_file" >> $(HOME)/.bashrc
	echo "export PUBLIC_KEY=$(shell pwd)/public_key_file" >> $(HOME)/.bashrc
install:
	cp signer.service /etc/systemd/system/
	cp publish.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable signer
	# create a keypair
	export SIGNER_PATH=$(shell pwd)/service
	python3 $(SIGNER_PATH)/lib/sign/cryptic.py
run:
	#source /root/.bashrc
	if [ ! $(SIGNER_PATH) ]; then
		export PYTHONPATH=$(shell pwd)
		export SIGNER_PATH=$(shell pwd)/service
		export PRIVATE_KEY=$(shell pwd)/private_key_file
		export PUBLIC_KEY=$(shell pwd)/public_key_file

	#sudo systemctl signer start
	python3 $(SIGNER_PATH)/main.py
	python3 $(SIGNER_PATH)/publish.py
clean:
	rm -rf service/__pycache__/
	rm -rf service/src/__pycache__/
	rm -rf service/lib/__pycache__/
	rm -rf service/lib/send/__pycache__/
	rm -rf service/lib/sign/__pycache__/
	rm -rf service/exceptions/__pycache__/
	#$(shell sed -i /$export/d $(HOME)/bashrc)
	sudo systemctl disable signer
	sudo rm -f /etc/systemd/system/signer.service
