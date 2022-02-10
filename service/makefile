
SERVICEPATH=/usr/local/etc

deps:
	apt install python3-rsa
	
install:
	mkdir $(SERVICEPATH)/service 
	# copy service directory
	shell cp -r * $(SERVICEPATH)/service
	# copy service files
	cp signer.service /etc/systemd/system/
	cp publish.service /etc/systemd/system/
	# run systemctl reload and enable
	systemctl daemon-reload
	systemctl enable signer
	systemctl enable publish
	# create a keypair
	$(shell export PRIVATE_KEY=$(SERVICEPATH)/private_key_file && export PUBLIC_KEY=$(SERVICEPATH)/public_key_file && /bin/python3 $(SERVICEPATH)/service/lib/sign/cryptic.py)
	
run:
	systemctl start signer
	systemctl start publish
	
clean:	
	rm -rf $(SERVICEPATH)/service/
	#$(shell sed -i /$export/d $(HOME)/bashrc)
	systemctl disable signer
	rm -f /etc/systemd/system/signer.service
	rm -f /etc/systemd/system/publish.service
