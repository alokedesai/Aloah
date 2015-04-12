from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
import sys
import os

#Adds any extra required space to the message
#May need to change this since it only adds \0
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt_file(filename, key):

	contentsize = 64*1024
	filesize = os.path.getsize(filename)

	inhash = SHA256.new()
	inhash.update(open(filename).read())
	inhash = inhash.digest()

	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	#enc =  iv + inhash + cipher.encrypt(message)
	outfilename = filename + ".enc"

	with open(outfilename, 'wb') as outfile:
		outfile.write(str(filesize).zfill(16))
		outfile.write(iv)
		outfile.write(inhash)

		with open(filename, 'rb') as infile:
			while True:
				content = infile.read(contentsize)
				if len(content) == 0:   
					break  # End of content.
				elif (len(content) % 16) != 0:
					content = pad(content) # Content requires padding.
				outfile.write(cipher.encrypt(content))
		infile.close()
	outfile.close()

def decrypt_file(filename, key):
	contentsize = 64*1024

	outfilename = "decrypted_" + filename[:-4]

	with open(filename, 'rb') as infile:
	    filesize = long(infile.read(16))
	    iv = infile.read(16)
	    inhash = infile.read(32)


	    cipher = AES.new(key, AES.MODE_CBC, iv)

	    with open(outfilename, 'wb') as outfile:
	        while True:
	            content = infile.read(contentsize)

	            if len(content) == 0:
	                # End of content.
	                break

	            outfile.write(cipher.decrypt(content))
	        outfile.truncate(filesize)
	    outfile.close()
	infile.close()

	outhash = SHA256.new()
	with open(outfilename, 'rb') as outfile:
		outhash.update(outfile.read())
	outfile.close()
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





