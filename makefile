
path:
	echo "export PYTHONPATH=$(shell pwd)/service" >> $(HOME)/.bashrc
	echo "export SIGNER_PATH=$(shell pwd)/service" >> $(HOME)/.bashrc
	echo "export PRIVATE_KEY=$(shell pwd)/private_key_file" >> $(HOME)/.bashrc
	echo "export PUBLIC_KEY=$(shell pwd)/public_key_file" >> $(HOME)/.bashrc
	
install:
	# read exported variables
	#source /root/.bashrc
	# get the dependency
	wget https://files.pythonhosted.org/packages/8c/ee/4022542e0fed77dd6ddade38e1e4dea3299f873b7fd4e6d78319953b0f83/rsa-4.8.tar.gz
	tar -xzf rsa-4.8.tar.gz
	mv rsa-4.8/ rsa/
	sudo apt install python3-setuptools
	sudo python3 rsa/setup.py install
	# setup the signer as service
	sudo cp signer.service /etc/systemd/system/
	sudo cp publish.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable signer
	# create a keypair
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
