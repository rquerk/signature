
PATH=/usr/local/etc

deps:
	$(shell apt install python3-rsa)
	
install:
	# copy service directory
	$(shell cp -r service/ $(PATH))
	# copy service files
	$(shell cp signer.service /etc/systemd/system/)
	$(shell cp publish.service /etc/systemd/system/)
	# run systemctl reload and enable
	$(shell systemctl daemon-reload)
	$(shell systemctl enable signer)
	$(shell systemctl enable publish)
	# create a keypair
	$(shell export PRIVATE_KEY=$(PATH)/private_key_file && export PUBLIC_KEY=$(PATH)/public_key_file && /bin/python3 $(PATH)/service/lib/sign/cryptic.py)
	
run:
	systemctl start signer
	systemctl start publish
	
clean:	
	rm -rf $(PATH)/service/
	#$(shell sed -i /$export/d $(HOME)/bashrc)
	systemctl disable signer
	rm -f /etc/systemd/system/signer.service
	rm -f /etc/systemd/system/publish.service
