
PATH=/usr/local/etc

deps:
	apt install pip
	pip install rsa
	
install:
	$(shell cp -r service/ $(PATH))
	$(shell cp signer.service /etc/systemd/system/)
	$(shell cp publish.service /etc/systemd/system/)
	systemctl daemon-reload
	systemctl enable signer  # maybe better enable after we have the key files
	systemctl enable publish
	# create a keypair
	export PRIVATE_KEY=$(PATH)/private_key_file
	export PUBLIC_KEY=$(PATH)/public_key_file
	python3 $(PATH)/service/lib/sign/cryptic.py
	
run:
	systemctl start signer
	systemctl start publish
	
clean:	
	rm -rf $(PATH)/service/
	#$(shell sed -i /$export/d $(HOME)/bashrc)
	systemctl disable signer
	rm -f /etc/systemd/system/signer.service
	rm -f /etc/systemd/system/publish.service
