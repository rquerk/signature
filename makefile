
path:
	echo "export PYTHONPATH=$(shell pwd)" >> $(HOME)/.bashrc
	echo "export PRIVATE_KEY=$(shell pwd)/private_key_file" >> $(HOME)/.bashrc
	echo "export PUBLIC_KEY=$(shell pwd)/public_key_file" >> $(HOME)/.bashrc

install:
	wget https://files.pythonhosted.org/packages/8c/ee/4022542e0fed77dd6ddade38e1e4dea3299f873b7fd4e6d78319953b0f83/rsa-4.8.tar.gz
	tar -xzf rsa-4.8.tar.gz
	mv rsa-4.8/ ../rsa/
	apt install python-setuptools
	python3 ../rsa/setup.py install

run:	

	export PYTHONPATH=$(shell pwd)
	export PRIVATE_KEY=$(shell pwd)/private_key_file
	export PUBLIC_KEY=$(shell pwd)/public_key_file
	
	python3 service/lib/sign/cryptic.py
	python3 service/main.py
	python3 service/publish.py

clean:
	rm -rf service/__pycache__/
	rm -rf service/src/__pycache__/
	rm -rf service/lib/__pycache__/
	rm -rf service/lib/send/__pycache__/
	rm -rf service/lib/sign/__pycache__/
	rm -rf service/exceptions/__pycache__/
	#sed -i /$export/d $(HOME)/bashrc
