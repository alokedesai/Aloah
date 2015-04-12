from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
import base64
import sys

#Adds any extra required space to the message
#May need to change this since it only adds \0
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt_file(file_name, key):
	with open(file_name, 'rb') as fo:
		plaintext = fo.read()


	inhash = SHA256.new()
	inhash.update(open(file_name).read())
	inhash = inhash.digest()


	message = pad(plaintext)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	enc =  iv + inhash + cipher.encrypt(message)

	with open(file_name + ".enc", 'wb') as fo:
		fo.write(enc)

def decrypt_file(file_name, key):


	with open(file_name, 'rb') as fo:
		ciphertext = fo.read()

	iv = ciphertext[:AES.block_size]
	#The +32 is because the hash is 256 = 32 bytes
	inhash = ciphertext[AES.block_size:(AES.block_size+32)]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintext = cipher.decrypt(ciphertext[(AES.block_size+32):])
	dec =  plaintext.rstrip(b"\0")

	outfile = "decrypted_" + file_name[:-4]

	with open(outfile, 'wb') as fo:
		fo.write(dec)

	outhash = SHA256.new()
	outhash.update(open(outfile).read())
	outhash = outhash.digest()

	if inhash == outhash:
		print "Integrity check passed"
	else:
		print "Integrity check failed"




key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

inputfile = sys.argv[1]

print "Starting encryption and decryption..."
encrypt_file(inputfile, key)
print "Encryption finished"
decrypt_file(inputfile + '.enc', key)
print "Decryption finished"





