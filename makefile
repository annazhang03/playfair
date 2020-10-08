help:
	$(info Uses playfair cipher to encode / decode user inputted string)
	$(info Input as: make run ARGS="encode/decode ciphertext/plaintext keytext")

run:
	python3 playfair.py $(ARGS)