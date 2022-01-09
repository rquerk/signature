
PATH=/usr/local/etc

deps:
	apt install pip
	pip install rsa
	
install:
	cp -r service/ $(PATH)
	cp signer.service /etc/systemd/system/
	cp publish.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable signer
	systemctl enable publish
	# create a keypair
	export PRIVATE_KEY=$(PATH)/private_key_file
	export PUBLIC_KEY=$(PATH)/public_key_file
	python3 $(PATH)/service/lib/sign/cryptic.py
run:
	#source /root/.bashrc
	if [ ! $(SIGNER_PATH) ]; then
		export PYTHONPATH=$(PATH)/service
		export SIGNER_PATH=$(PATH)/service
		export PRIVATE_KEY=$(PATH)/private_key_file
		export PUBLIC_KEY=$(PATH)/public_key_file

	#sudo systemctl start signer
	python3 $(SIGNER_PATH)/signer.py
	python3 $(SIGNER_PATH)/publish.py
clean:
	rm -rf $(PATH)/service/
	#$(shell sed -i /$export/d $(HOME)/bashrc)
	sudo systemctl disable signer
	rm -f /etc/systemd/system/signer.service
	rm -f /etc/systemd/system/publish.service
