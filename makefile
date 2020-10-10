help:
	$(info Uses playfair cipher to encode / decode user inputted string)
	$(info Input as: make run ARGS="encode/decode ciphertext/plaintext keytext")
	$(info Ciphertext/plaintext can be multiple words, as long as keytext is the final argument given)

run:
	python3 playfair.py $(ARGS)