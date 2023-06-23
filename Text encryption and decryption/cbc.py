# import some basic packages
import codecs
import argparse

"""" This function takes text and turn it into encrypted text by the key and
    the initial vector with block size of 10."""
def Encryption (plain_text, key, iv):
    with codecs.open(plain_text, 'r', 'utf-8') as text:            # Read the plain_text
        data = text.read()
    with codecs.open(key, 'r', 'utf-8') as text_key:               # Read the relevant key
        k = text_key.read().splitlines()
    with codecs.open(iv, 'r', 'utf-8') as initial:                 # Read the relevant initial vector
        initial_v = initial.read()
    file = codecs.open("plainText_encrypted.txt", "w", "utf-8")    # Open new file, that will contain the encrypted text

    chunk_len = 10                                                 # Defining the block's length
    chunks = [data[x:x + chunk_len] for x in range(0, len(data), chunk_len)] # Separate the plain text into blocks of 10

    for i in range(chunk_len - len(chunks[-1])):                   # Adding some padding for the last block
        chunks[-1] += '\0'
    key_dict = {}                                                  # Initialize an empty dictionary
    for j in k:                                                    # Making a dictionary from the key for encryption
        x, y = j.split(' ')
        key_dict[x] = y

    current_v = initial_v                                 # Initialize the initial vector for the start
    for chunk in chunks:                                  # Goes all over the chunks we created for the plain_text
        new_v = ''                                        # Initialize new string for the encrypted text from this block
        for j in range(chunk_len):                        # For each element in the current chunk
            x = chr(ord(chunk[j]) ^ ord(current_v[j]))    # Do XOR action
            if x in key_dict:                             # checking if there is a key for this char
                x = key_dict[x]                           # Change the value of this char
            new_v += x                                    # Adding the value to the new vector
        file.write(new_v)                                 # Write the first encrypted block to the file we created
        current_v = new_v                                 # Update the initial vector to this encrypted block


""" This function takes encrypted text and turn it into decrypted text- the original text by 
    the key and the initial vector (the key is the opposite of the key of the encryption)."""
def Decryption(cipher_text, key, iv):
    with codecs.open(cipher_text, 'r', 'utf-8') as text:        # Read the cipher_text
        data = text.read()
    with codecs.open(key, 'r', 'utf-8') as text_key:            # Read the relevant key
        k = text_key.read().splitlines()
    with codecs.open(iv, 'r', 'utf-8') as initial:              # Read the relevant initial vector
        initial_v = initial.read()
    file = codecs.open("plainText_decrypted.txt", "w", "utf-8") # Open new file, that will contain the encrypted text

    chunk_len = 10                                              # Defining the block's length
    chunks = [data[x:x + chunk_len] for x in range(0, len(data), chunk_len)] # Separate the plain text into blocks of 10
    for i in range(chunk_len - len(chunks[-1])):                       # Adding some padding for the last block
        chunks[-1] += '\0'

    key_dict = {}                                               # Initialize an empty dictionary for the key
    for j in k:                                                 # Making a dictionary from the key for decryption
        x, y = j.split(' ')
        key_dict[y] = x

    current_v = initial_v                                      # Initialize the initial vector for the start
    for chunk in chunks:                                       # Goes all over the chunks we created for the cipher_text
        new_v = ''                                        # Initialize new string for the encrypted text from this block
        for j in range(chunk_len):                             # For each element in the current chunk
            if chunk[j] in key_dict:                           # Checking if there is a key for this element in chunk
                x = key_dict[chunk[j]]                         # Change the value of this char in the chunk
            else:                                              # If there is no a key fot this element in chunk
                x = chunk[j]                                   # Change the value to the element in the chunk
            x = chr(ord(x) ^ ord(current_v[j]))                # Do XOR action
            new_v += x                                         # Adding the value to the new vector
        file.write(new_v)                                      # Write the first encrypted block to the file we created
        current_v = chunk                                      # Update the initial vector to this chunk

"""" Use the argparse package for calling the functions from the command line"""

parser = argparse.ArgumentParser(description="Insert arguments.")
parser.add_argument('command', type=str, help='Insert command (Encryption or Decryption)')
parser.add_argument('text_file', type=str, help='Insert text file name ( plain text file or  cipher message)')
parser.add_argument('key_file', type=str, help='Insert key file')
parser.add_argument('iv_file', type=str, help='Insert iv file')
args = parser.parse_args()

""" Connect the command prompt to our python file"""

if args.command == "Encryption":
    Encryption(args.text_file, args.key_file, args.iv_file)
elif args.command == "Decryption":
    Decryption(args.text_file, args.key_file, args.iv_file)
else:
    print('unsupported command.')
