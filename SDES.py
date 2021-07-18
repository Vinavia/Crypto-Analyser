"""
-----------------------------
CP460 (Fall 2020)
Name: Matthew Chiarelli
ID:   150798950
Final Exam
-----------------------------
"""

import math
import string
import mod
import utilities



CONFIG_FILE = 'SDES_config.txt'
SBOX1_FILE = 'sbox1.txt'
SBOX2_FILE = 'sbox2.txt'
PRIME_FILE = 'primes.txt'
PAD = 'Q'

#---------------------------------------------
#         Q1: Coding Scheme                  #
#---------------------------------------------

"""
----------------------------------------------------
Parameters:   c (str): a character
              code_type (str)
Return:       b (str): corresponding binary number
Description:  Generic function for encoding
              Current implementation supports only ASCII and B6 encoding
Errors:       If c is not a single character:
                print 'Error(encode): invalid input'
                return empty string
              If unsupported encoding type:
                print 'Error(encode): Unsupported Coding Type'
                return empty string 
---------------------------------------------------
"""
def encode(c,code_type):
    if not isinstance(c,str):
        print('Error(encode): invalid input', end='')
        return ""
    
    if len(c) != 1:
        print('Error(encode): invalid input', end='')
        return ""
    
    if not isinstance(code_type,str):
        print('Error(encode): Unsupported Coding Type', end='')
        return ""
    
    if code_type != 'ASCII' and code_type != 'B6' and code_type != 'CBC' and code_type != 'OFB':
        print('Error(encode): Unsupported Coding Type', end='')
        return ""
    
    b = ''
    if code_type == 'B6':
        base = utilities.get_base('B6')
        bits = 0
        for letter in base:
            if letter == c:
                b = bin(bits)
                b = b.replace('b','')
                while b[0] == '0' and len(b) >= 2:
                    b = b[1:]
                b = b.zfill(6)
                exit
                
            bits += 1
    elif code_type == 'ASCII':
        b = bin(ord(c))
        b = b.replace('b','')
        b = b.zfill(8)        

        
    return b

"""
----------------------------------------------------
Parameters:   b (str): a binary number
              codeType (str)
Return:       c (str): corresponding character
Description:  Generic function for encoding
              Current implementation supports only ASCII and B6 encoding
Errors:       If b is not a binary number:
                print 'Error(decode): invalid input'
                return empty string
              If unsupported encoding type:
                print 'Error(decode): Unsupported Coding Type'
                return empty string
---------------------------------------------------
"""
def decode(b,code_type):
    if not isinstance(b,str):
        print('Error(decode): invalid input', end='')
        return ""
    if b == '':
        print('Error(decode): invalid input', end='')
        return ""        
    
    if not isinstance(code_type,str):
        print('Error(decode): Unsupported Coding Type', end='')
        return ""
    
    if code_type != 'ASCII' and code_type != 'B6' and code_type != 'CBC' and code_type != 'OFB':
        print('Error(decode): Unsupported Coding Type', end='')
        return ""
    
    c = ''
    if code_type == 'B6':
        base = utilities.get_base('B6')
        bits = 0
        for letter in base:
            
            if encode_B6(letter) == b:
                c = letter
                exit
            bits += 1

    elif code_type == 'ASCII':
        c = chr(int(b,2))
        
   
    return c

"""
----------------------------------------------------
Parameters:   c (str): a character
Return:       B6_code (str): 6-digit binary code
Description:  Encodes any given symbol in the B6 Encoding scheme
              If given symbol is one of the 64 symbols
              return binary representation, which is the binary number of the
              decimal value representing the position of the symbol in the B6 base
              If the given symbol is not part of the B6Code --> 
                    return empty string (no error msg)
Error:        If given input is not a single character -->
                  print 'Error(encode_B6): invalid input' 
                  return empty string
---------------------------------------------------
"""
def encode_B6(c):
    if not isinstance(c,str):
        print('Error(encode_B6): invalid input', end = '')
        return ''
    
    if len(c) != 1:
        print('Error(encode_B6): invalid input', end = '')
        return ''
            
    B6_code = encode(c,'B6')
    return B6_code

"""
----------------------------------------------------
Parameters:   b (str): binary number
Return:       c (str): a character
Description:  Decodes any given binary code in the B6 Coding scheme
Errors:       If given input is not a valid 6-bit binary number -->
                  print 'Error(decode_B6): invalid input
                  return empty string
---------------------------------------------------
"""
def decode_B6(b):
    if not isinstance(b,str):
        print('Error(decode_B6): invalid input', end = '')
        return ''
    
    if len(b) != 6:
        print('Error(decode_B6): invalid input', end = '')
        return ''
    
    c = decode(b,'B6')
    return c

#---------------------------------------------
#         Q2: SDES Configuration             #
#---------------------------------------------

"""
----------------------------------------------------
# Parameters:   None
# Return:       paramList (list)
# Description:  Returns a list of parameter names which are used in
#               Configuration of SDES
# Error:        None
---------------------------------------------------
"""
def get_SDES_parameters():
    return ['encoding_type','block_size','key_size','rounds','p','q']

"""
----------------------------------------------------
Parameters:   [optional] config_file (str): file name
Return:       config_list (2D List)
Description:  Returns the current SDES configuration list
              formatted as: [[parameter1,value],[parameter2,value2],...]
              The configurations are read from the configuration file
              If configuration file is empty --> return []
              If no configuration file is given, use default CONFIG_FILE
              parameters are ordered based on their order in config file
---------------------------------------------------
"""
def get_SDES_config(config_file=CONFIG_FILE):
    config_list = []
    f = open(config_file, 'r')
    
    #param = get_SDES_parameters()
    
    for line in f:
        param_name = ''
        value = ''
        
        for c in line:
            if not ':' in param_name:
                param_name = param_name + c
            else:
                value += c
        param_name = param_name.replace(':','')
        param_name = param_name.replace('\n','')
        param_name = param_name.replace(':','')
        value = value.replace('\n','')
        config_list.append([param_name, value])
        
    f.close()
    return config_list

"""
----------------------------------------------------
Parameters:   parameter (str)
              [optional] config_file (str)
Return:       value (str)
Description:  Returns the value of the parameter based on current configuration
              as defined in the given file
Error:        If the parameter is undefined in get_SDES_parameters() -->
                  print 'Error(get_SDES_value): invalid parameter'
                  return empty string
---------------------------------------------------
"""
def get_SDES_value(parameter,config_file = CONFIG_FILE):
    value = ''
    f = open(config_file, 'r')
    if not parameter in get_SDES_parameters():
        print('Error(get_SDES_value): invalid parameter',end='')
        return ""
    for line in f:
        param_name = ''
        value = ''
        for c in line:
            if not ':' in param_name:
                param_name = param_name + c
            else:
                value += c
                
        if param_name.replace(':','') == parameter:
            return value.replace('\n','') 
    
    f.close()
    
    #print('COULD NOT FIND PARAMETER!')
    return ""

"""
----------------------------------------------------
Parameters:   parameter (str)
              value (str)
              [optional] config_file (str)
Return:       True/False
Description:  Sets an SDES parameter to the given value
              if the configuration file contains previous value for the parameter
              the function overrides it with the new value
              otherwise, the new value is appended to the configuration file
              Function returns True if set value is successful and False otherwise
Error:        If the parameter is undefined in get_SDES_parameters() -->
                  print 'Error(set_SDES_value): invalid parameter'  return False
              If given value is not a string or is an empty string:
                 print 'Error(set_SDES_value): invalid value' return 'False
---------------------------------------------------
"""
def set_SDES_value(parameter,value,config_file=CONFIG_FILE):
    #NOT DONE NOT DONE NOT DONE NOT DONE!

    if not parameter in get_SDES_parameters():
        print('Error(get_SDES_value): invalid parameter',end='')
        return False
    
    if not isinstance(value,str):
        print('Error(set_SDES_value): invalid value',end='')
        return False
    
    if value == '':
        print('Error(set_SDES_value): invalid value',end='')
        return False
    f = open(config_file, 'r+')   
    num_line = 0 
    for line in f:
        
        param_name = ''
        v = ''
        for c in line:
            if not ':' in param_name:
                param_name = param_name + c
            else:
                v += c
                
                
        if param_name.replace(':','') == parameter: #PARAMATER IS FOUND, OVERWRITE
            f.close()
            #f = open(config_file, 'w')
            #f.write(parameter + ":" + value)
            #print("IN: " + parameter + ":" + value)
            replace_line(config_file,num_line,parameter + ":" + value + '\n')
            return True
        #f.write(param_name + v)
        num_line += 1
        
    f.close()
    #if found == False:#VALUE IS NOT FOUND, APPEND TO END
    #print("AFTER: " + parameter + ":" + value)
    #f = open(config_file, 'a')
    #f.write(parameter + ":" + value)
    #f.close()
    with open(config_file,'a') as fl:
        fl.write('\n' + parameter + ":" + value)

    return True

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
    return

#---------------------------------------------
#             Q3: Key Generation             #
#---------------------------------------------

"""
----------------------------------------------------
Parameters:   p (int)
              q (int)
              m (int): number of bits
Return:       bit_stream (str)
Description:  Uses Blum Blum Shub Random Generation Algorithm to generate
              a random stream of bits of size m
              The seed is the nth prime number, where n = p*q
              If the nth prime number is not relatively prime with n,
              the next prime number is selected until a valid one is found
              The prime numbers are read from the file PRIME_FILE (starting n=1)
Error:        If number of bits is not a positive integer -->
                  print 'Error(blum): Invalid value of m',end ='' and return ''
              If p or q is not an integer that is congruent to 3 mod 4:
                  print 'Error(blum): Invalid values of p,q' and return ''
---------------------------------------------------
"""
def blum(p,q,m):
    if not isinstance(m,int):
        print('Error(blum): Invalid value of m',end ='')
        return ''
    if m < 1:
        print('Error(blum): Invalid value of m',end ='')
        return ''
    if not isinstance(p,int) or not isinstance(q,int):
        print('Error(blum): Invalid values of p,q',end ='')
        return ''    
    if not mod.is_congruent(p, 3, 4) or not mod.is_congruent(q, 3, 4):
        print('Error(blum): Invalid values of p,q',end ='')
        return ''   
        
    bit_stream = ''
    
    n = p*q #Max value possible
    num_line = 0
    f = open(PRIME_FILE, 'r')
       
    #Get seed
    for line in f:
        if num_line >= n:
            #print(mod.is_relatively_prime(int(line), n))
            if mod.is_relatively_prime(int(line), n):
                seed = int(line)
                break
        num_line += 1
    f.close()
    #seed = 5
    #Loop until valid
    result = seed
    #result = (result*result) % n
    for i in range(m):
        result = (result * result) % n
        if result % 2 == 1:
            bit_stream += '1'
        else:
            bit_stream += '0'
    ''' 
    for line in f:
        #if num_line >= n:
        print(int(line))
        
        if int(line) >= n:
            print("OVER MAX: " + str(n))
            return""
            
        if mod.is_relatively_prime(int(line), n):
            seed = int(line)
            f.close()
            print("DONE!")
            return ""
            #exit
        #num_line += 1
    f.close()
    '''    
    return bit_stream

"""
----------------------------------------------------
Parameters:   [optional] config_file (str)
Return:       key (str)
Description:  Generates an SDES key based on preconfigured values
              The key size is fetched from the SDES configuration
              If no key size is available, an error message is printed
              Also, the values of p and q are fetched as per SDES configuration
              If no values are found, the default values p = 383 and q = 503 are used
              These values should be updated in the configuration file
              The function calls the blum function to generate the key
Error:        if key size is not defined -->
                  print 'Error(generate_key_SDES):Unknown Key Size' and return ''
---------------------------------------------------
"""
def generate_key_SDES(config_file=CONFIG_FILE):
    key = ''
    
    key_size = get_SDES_value("key_size", config_file)
    
    if key_size == "":
        print('Error(generate_key_SDES):Unknown Key Size', end = '')
        return ""
    
    p = get_SDES_value("p", config_file)
    q = get_SDES_value("q", config_file)
    
    if p == "":
        p = 383
        set_SDES_value('p', 383, config_file)  
    if q == "":
        q = 503
        set_SDES_value('q', 503, config_file)
        
    key = blum(p,q,key_size)
    
    if key == "":
        print('Error(generate_key_SDES):Something went wrong with generating key', end = '')
               
    return key


"""
----------------------------------------------------
Parameters:   key (str)
              i (int)
              [optional] config_file (str)
Return:       subkey (str)
Description:  Generates a subkey for the ith round in SDES
              The sub-key is one character shorter than original key size
              Sub-key is generated by circular shift of key with value 1,
              where i=1 means no shift
              The least significant bit is dropped after the shift
Errors:       if key is not a valid binary number or 
              its length does not match key_size: -->
                  print 'Error(get_subkey): Invalid key' and return ''
              if i is not a positive integer:
                  print 'Error(get_subkey): invalid i' and return ''
---------------------------------------------------
"""
def get_subkey(key,i,config_file=CONFIG_FILE):

    
    if not isinstance(key,str):
        print('Error(get_subkey): Invalid key',end = "")
        return ''
    if not isinstance(i,int):
        print('Error(get_subkey): invalid i',end = "")
        return ''        
    if i <= 0:
        print('Error(get_subkey): invalid i',end = "")
        return ''    
        
    for c in key:
        if c != '0' and c != '1':
            print('Error(get_subkey): Invalid key',end = "")
            return ''
        
    key_size = get_SDES_value('key_size', config_file) #This returns a string, careful
    
    if len(key) != int(key_size):
            print('Error(get_subkey): Invalid key',end = "")
            return ''
    
    #Perform shift
    subkey = key
    if i == 1:
        return subkey[:len(subkey) - 1]
    
    for ndx in range(i - 1):
        subkey = subkey[1:] + subkey[0]
                    
    return subkey[:len(subkey) - 1]


#---------------------------------------------
#            Q4: Fiestel Network             #
#---------------------------------------------

"""
----------------------------------------------------
Parameters:   R (str): binary number of size (block_size/2)
Return:       R_exp (str): output of expand function
Description:  Expand the input binary number by adding two digits
              The input binary number should be an even number >= 6
              Expansion works as the following:
              If the index of the two middle elements is i and i+1
                  indices 0 up to i-1: same order
                  middle becomes: R(i+1)R(i)R(i+1)R(i)
                  indices R(i+2) to the end: same order
              No need to validate that R is of size block_size/2
Errors:       if R not a valid binary number or if it has an odd length
              or is of length is smaller than 6
                  print 'Error(expand): invalid input' and return ''
---------------------------------------------------
"""
def expand(R):
    
    
    if not isinstance(R,str):
        print('Error(expand): invalid input',end = '')
        return ''
    
    for c in R:
        if c != '0' and c != '1':
            print('Error(expand): invalid input',end = "")
            return ''
    
    if len(R) % 2 == 1 or len(R) < 6:
        print('Error(expand): invalid input',end = "")
        return ''
    R_exp = R[:]
    
    mid = int(len(R_exp)/2)
    R_exp = R_exp[:mid-1] + R_exp[mid] + R_exp[mid - 1] + R_exp[mid] + R_exp[mid - 1] + R_exp[mid + 1:]
            
    
    return R_exp

"""
----------------------------------------------------
Parameters:   R (str): binary number of size (block_size//4)
              [optional] sbox1_file (str): filename
Return:       output (str): binary number
Description:  Validates that R is of size block_size//4 + 1
              Retrieves relevant structure of sbox1 from given sbox1 file
              Most significant bit of R is row number, other bits are column number
Errors:       if undefined block_size:
                  print 'Error(sbox1): undefined block size' and return ''
              if invalid R:
                  print 'Error(sbox1): invalid input' and return ''
              if no sbox1 structure exist:
                  print 'Error(sbox1): undefined sbox1'and return ''
---------------------------------------------------
"""
def sbox1(R,sbox1_file=SBOX1_FILE):
    output = ''
    
    block_size = get_SDES_value("block_size", CONFIG_FILE)
    
    if not isinstance(R,str):
        print('Error(sbox1): invalid input',end='')
        return ''
    
    if block_size == "":
        print('Error(sbox1): undefined block size',end='')
        return ''
    
    block_size = int(block_size)
    r_size = len(R)
    
    if r_size !=  int(block_size/4) + 1:
        print('Error(sbox1): invalid input',end='')
        return ''  
    
    f = open(sbox1_file,"r")
    required_line = ""
    for line in f:
        if len(line) > 0:
            if int(line[0]) == r_size:
                required_line = line[:]
    
    f.close()
    
    if required_line == "":
        print('Error(sbox1): undefined sbox1',end = '')
        return ''
    
    required_line = required_line[2:].replace('\n', '')
    
    values = required_line.split(',')
    num_val = len(values)
    ndx = 0
    box_values = [[],[]]
    #populate box_values first with raw values, then mappings
    for v in values:
        if ndx >= num_val/2:
            box_values[1].append(v)
        else:
            box_values[0].append(v) 
        ndx += 1
    ndx = 0

    #grab from box_values
    if R[0] == "0":
        output = box_values[0][int(R[1:],2)]
    elif R[0] == "1":
        output = box_values[1][int(R[1:],2)]
        
    return output

"""
----------------------------------------------------
Parameters:   R (str): binary number of size (block_size//4)
              [optional] sbox2_file (str): filename
Return:       output (str): binary number
Description:  Validates that R is of size block_size//4 + 1
              Retrieves relevant structure of sbox2 from given sbox2 file
              Most significant bit of R is row number, other bits are column number
Errors:       if undefined block_size:
                  print 'Error(sbox2): undefined block size' and return ''
              if invalid R:
                  print 'Error(sbox2): invalid input' and return ''
              if no sbox2 structure exist:
                  print 'Error(sbox2): undefined sbox2'and return ''
---------------------------------------------------
"""
def sbox2(R,sbox2_file=SBOX2_FILE):
    output = ''
    
    block_size = get_SDES_value("block_size", CONFIG_FILE)
    
    if not isinstance(R,str):
        print('Error(sbox2): invalid input',end='')
        return ''
    
    if block_size == "":
        print('Error(sbox2): undefined block size',end='')
        return ''
    
    block_size = int(block_size)
    r_size = len(R)
    
    if r_size !=  int(block_size/4) + 1:
        print('Error(sbox2): invalid input',end='')
        return ''  
    
    f = open(sbox2_file,"r")
    required_line = ""
    for line in f:
        if len(line) > 0:
            if int(line[0]) == r_size:
                required_line = line[:]
    
    f.close()
    
    if required_line == "":
        print('Error(sbox2): undefined sbox2',end='')
        return ''
    
    required_line = required_line[2:].replace('\n', '')
    
    values = required_line.split(',')
    num_val = len(values)
    ndx = 0
    box_values = [[],[]]
    #populate box_values first with raw values, then mappings
    for v in values:
        if ndx >= num_val/2:
            box_values[1].append(v)
        else:
            box_values[0].append(v) 
        ndx += 1
    ndx = 0

    #grab from box_values
    if R[0] == "0":
        output = box_values[0][int(R[1:],2)]
    elif R[0] == "1":
        output = box_values[1][int(R[1:],2)]
        
    return output


"""
----------------------------------------------------
Parameters:   Ri (str): block of binary numbers
              ki (str): binary number representing subkey
              [optional] files (list): [config_file,sbox1_file,sbox2_file]
Return:       Ri2 (str): block of binary numbers
Description:  Performs the following five tasks:
              1- Pass the Ri block to the expander function
              2- Xor the output of [1] with ki
              3- Divide the output of [2] into two equal sub-blocks
              4- Pass the most significant bits of [3] to Sbox1
                 and least significant bits to sbox2
              5- Concatenate the output of [4] as [sbox1][sbox2]
Errors:       if ki is an invalid binary number:
                  print 'Error(F): invalid key' and return ''
              if invalid Ri:
                  print 'Error(F): invalid input' and return ''
---------------------------------------------------
"""
def F(Ri,ki, files=[CONFIG_FILE,SBOX1_FILE,SBOX2_FILE]):
    Ri2 = ''
    
    if not isinstance(Ri,str):
        print('Error(F): invalid input',end='')
        return ''
    if not isinstance(ki,str):
        print('Error(F): invalid key',end='')
        return ''
        
    ex_R = expand(Ri)
    
    if ex_R == "":
        print('Error(F): invalid input',end='')
        return ''
    for c in ki:
        if (c != '0' and c !='1'):
            print('Error(F): invalid key',end='')
            return '' 
        
    if ki == '':
        print('Error(F): invalid key',end='')
        return ''
    

             
    #XOR output
    ndx = 0
    xor_R = ''
    while ndx < len(ex_R):
        if ndx >= len(ex_R) or ndx >= len(ki):  #Watch this closely
            print('Error(F): invalid key',end='')
            return ''
            
        if (ex_R[ndx] == '0' and ki[ndx] == '0') or (ex_R[ndx] == '1' and ki[ndx] == '1'):
            xor_R += '0'
        else:
            xor_R += '1'
        ndx += 1
    #Divide into two sub-blocks
    
    sblock1 = []
    sblock2 = []
    mid = int(len(xor_R)/2)
    sblock1.append(xor_R[:mid])
    sblock2.append(xor_R[mid:])
    '''
    #print(xor_R)
    print(sblock1)
    print(sblock2)
    
    mid = int(mid/2)
    most_sig = sblock1[0][:mid] + sblock2[0][:mid]
    least_sig = sblock1[0][-1 * mid:] + sblock2[0][-1 * mid:]
    print("YEET "  + most_sig)
    print(least_sig)
    '''
    out1 = sbox1(sblock1[0],files[1])
    out2 = sbox2(sblock2[0],files[2])
    
    Ri2 = out1 + out2
    return Ri2
"""
----------------------------------------------------
Parameters:   bi1 (str)
              bi2 (str)
Return:       xor_R (str)
Description:  XOR's the two given binary strings
---------------------------------------------------
"""
def xor(bi1,bi2):
    #XOR output
    ndx = 0
    xor_R = ''
    while ndx < len(bi1):
        if ndx >= len(bi1) or ndx >= len(bi2):  #Watch this closely
            print('Error(xor): invalid input',end='')
            return ''
            
        if (bi1[ndx] == '0' and bi2[ndx] == '0') or (bi1[ndx] == '1' and bi2[ndx] == '1'):
            xor_R += '0'
        else:
            xor_R += '1'
        ndx += 1
        
    return xor_R

"""
----------------------------------------------------
Parameters:   bin (str)
Return:       swaped_bin (str)
Description:  switches the right hand side of string to left hand side
---------------------------------------------------
"""
def swap(bin):
    swaped_bin = ''
    
    left = bin[:int(len(bin) / 2)]
    right = bin[int(len(bin) / 2):]
      
    swaped_bin = right + left 
    return swaped_bin
    
"""
----------------------------------------------------
Parameters:   bi (str): block of binary numbers
              ki (str): binary number representing subkey
              [optional] files (list): [config_file,sbox1_file,sbox2_file]
Return:       bi2 (str): block of binary numbers
Description:  Applies Fiestel Cipher on a block of binary numbers
              L(current) = R(previous)
              R(current) = L(previous) xor F(R(previous), subkey)
Errors:       if ki is an invalid binary number or of invalid size
                  print 'Error(feistel): Invalid key' and return ''
              if invalid Ri:
                  print 'Error(feistel): Invalid block' and return ''
---------------------------------------------------
"""
def feistel(bi,ki,files=[CONFIG_FILE,SBOX1_FILE,SBOX2_FILE]):
    bi2 = ''
    
    if not isinstance(bi,str):
        print("Error(feistel): invalid binary block", end='')
        return ''
    if not isinstance(ki,str):
        print("Error(feistel): invalid key",end='')
        return ''
    if len(bi) % 2 != 0:
        print("Error(feistel): invalid binary block",end='')
        return ''
        
    #Divide into two halves

    L = bi[:int(len(bi) / 2)]
    R1 = bi[int(len(bi) / 2):]


    f1 = F(R1,ki,files)
    R2 = xor(f1,L)
    L1 = R1

    #print("Left block: " + L + " Right block: " + R1 + " Subkey: " + ki)
    bi2 = L1 + R2
    
    
    return bi2

#---------------------------------------------
#     Q5: SDES Cipher (ECB Mode)             #
#---------------------------------------------

"""
----------------------------------------------------
Parameters:   plaintext (str)
              key (str): binary number
              [optional] files (list): [config_file,sbox1_file,sbox2_file]
Return:       ciphertext (str)
Description:  A dispatcher SDES encryption function
              passes the plaintext/key to the proper function based on given mode
              Defines only ECB mode
Errors:       if undefined mode:
                print 'Error(e_SDES): undefined mode' and return ''
---------------------------------------------------
"""
def e_SDES(plaintext,key,mode,files=[CONFIG_FILE,SBOX1_FILE,SBOX2_FILE]):
    ciphertext = ''
    
    if not isinstance(plaintext,str):
        print('Error(e_SDES): Invalid plaintext',end = '')
        return ''
    if plaintext == '':
        print('Error(e_SDES): Invalid plaintext',end = '')
        return ''
    
    
    if mode.upper() == 'ECB':
        ciphertext = e_SDES_ECB(plaintext, key, files)
    elif mode.upper() == 'CBC':
        ciphertext = e_SDES_CBC(plaintext, key, files)
    elif mode.upper() == 'OFB':
        ciphertext = e_SDES_OFB(plaintext, key, files) 
    else:
        print('Error(e_SDES): undefined mode',end = '')
        return ''
    
    
    return ciphertext

"""
----------------------------------------------------
Parameters:   ciphertext (str)
              key (str): binary number
              [optional] files (list): [config_file,sbox1_file,sbox2_file]
Return:       plaintext (str)
Description:  A dispatcher SDES decryption function
              passes the plaintext/key to the proper function based on given mode
              Defines only ECB mode
Errors:       if undefined mode:
                print 'Error(d_SDES): undefined mode' and return ''
---------------------------------------------------
"""
def d_SDES(ciphertext,key,mode,files=[CONFIG_FILE,SBOX1_FILE,SBOX2_FILE]):
    plaintext = ''
    
    if not isinstance(ciphertext,str):
        print('Error(d_SDES): Invalid ciphertext',end = '')
        return ''
    if ciphertext == '':
        print('Error(d_SDES): Invalid ciphertext',end = '')
        return ''
    
    
    if mode.upper() == 'ECB':
        plaintext = d_SDES_ECB(ciphertext, key, files)
    elif mode.upper() == 'CBC':
        plaintext = d_SDES_CBC(ciphertext, key, files)
    elif mode.upper() == 'OFB':
        plaintext = d_SDES_OFB(ciphertext, key, files)        
    else:
        print('Error(d_SDES): undefined mode',end = '')
        return ''
    return plaintext

"""
----------------------------------------------------
Parameters:   plaintext (str)
              key (str): binary number
              files (list): [config_file,sbox1_file,sbox2_file]
Return:       ciphertext (str)
Description:  Encryption using SDES ECB mode
Errors:       Similar to e_SDES
---------------------------------------------------
"""
def e_SDES_ECB(plaintext,key,files):
    ciphertext = ''
    if not isinstance(plaintext,str):
        print('Error(e_SDES_ECB): Invalid plaintext',end = '')
        return ''
    if plaintext == '':
        print('Error(e_SDES_ECB): Invalid plaintext',end = '')
        return ''
    
    encoding_type = get_SDES_value('encoding_type',files[0])
    if encoding_type == '':
        print('Error(e_SDES_ECB): Invalid configuration, Could not get encoding type ', end='')
        return ''
    
    block_size = get_SDES_value('block_size',files[0])
    if block_size == '':
        print('Error(e_SDES_ECB): Invalid configuration, Could not get block size ', end='')
        return ''
    
    key_size = get_SDES_value('key_size',files[0])
    if key_size == '':
        print('Error(e_SDES_ECB): Invalid configuration, Could not get key_size ', end='')
        return ''
    
    rounds = get_SDES_value('rounds',files[0])
    if rounds == '':
        print('Error(e_SDES_ECB): Invalid configuration, Could not get rounds ', end='')
        return ''
    
    if key == '': #Generate new key
        p = get_SDES_value('p',files[0])
        if p == '':
            print('Error(e_SDES_ECB): Invalid configuration, Could not get p ', end='')
            return ''
        q = get_SDES_value('q',files[0])
        if q == '':
            print('Error(e_SDES_ECB): Invalid configuration, Could not get q ', end='')
            return '' 
        key = generate_key_SDES(files[0])
    #Validate key_size
    #print(len(key))
    if len(key) % 2 == 0: #MAYBE?????
        print('Error(e_SDES_ECB): Invalid key', end='')
        return '' 
    
    
    #Get all undefined characters in text
    undefined = ''
    for c in plaintext:
        if encode(c,encoding_type) == '' and not c in undefined:
            undefined += c
    undefined_pos = utilities.get_positions(plaintext, undefined + '\n')
    cleaned_text = utilities.clean_text(plaintext, undefined) #add newline?
    
    blocks = []
    ndx = 0
    print("YOOOOOOOOOOOOOOOOOOOO" + cleaned_text)
    while ndx < len(cleaned_text) - 1: #Changed from len(cleaned) to len(cleaned - 1
        blocks.append([cleaned_text[ndx] + cleaned_text[ndx + 1]])
        ndx += 2
    if len(cleaned_text) % 2 == 1:
        blocks.append([cleaned_text[len(cleaned_text) - 1] + PAD]) #Added - 1 to here as well
        
    defined_blocks = []
    #print(blocks)
    for b in blocks:
        e_block = []

        lc = encode(b[0][0],encoding_type)
        rc = encode(b[0][1],encoding_type)
        '''
        if lc == '':
            print('lc: NOT IN ENCODIG')
        if rc == '':
            print('rc: NOT IN ENCODIG')
        '''        
        defined_blocks.append([lc + rc])
    '''    
    print("DEFINED_BLOCKS: ",end = '')
    for d in defined_blocks:
        print(d,end = '')
    print()
    '''
    binary_stream = ''    
    for db in defined_blocks:
        binary_stream += db[0]
        
    #print("BINARY_STREAM: " + binary_stream)
    ndx = 0
    f_binary_stream = ''
    
    while ndx < len(binary_stream):
        f_block = ''
        #Get block
        for i in range(int(block_size)):
            f_block += binary_stream[ndx]
            ndx += 1
        #print("Processing this block: " + f_block + " -> ",end='')
        #Run through feistel cipher x times
        for i in range(int(rounds)):
            
            new_key = get_subkey(key,i + 1,files[0])
            f_block = feistel(f_block, new_key, files)
            if i == int(rounds) - 1:
                f_block = swap(f_block)
            
            #if ndx >= len(binary_stream) - 1: #FOR SOME REASON THIS DECODES IT BACK IF SUBKEY IS NOT UPDATED???????
                #f_block = swap(f_block)
                
        #print(f_block)        
        f_binary_stream += f_block
        
    #print("F_BINARY_STREAM: " + f_binary_stream)
    
    #Swap two halves
    #swaped_bin = swap(f_binary_stream)
    swaped_bin = f_binary_stream
    
    #print("SWAPED_BIN: " + swaped_bin)
     
    #translate back
    ndx = 0
    while ndx < len(swaped_bin):
        s_block = ''
        #print(c)
        for i in range(int(int(block_size) / 2)): #It is this size atm since B6 uses 6 bits
            s_block += swaped_bin[ndx]
            ndx += 1
        #print("s_block: " + s_block)
        ciphertext += decode(s_block,encoding_type)
    #print("BEFORE CIPHERTEXT: " + ciphertext)    
    ciphertext = utilities.insert_positions(ciphertext, undefined_pos)
    
    #print("AFTER INSERT CIPHERTEXT: " + ciphertext)        
    return ciphertext
"""
----------------------------------------------------
Parameters:   plaintext (str)
              key (str): binary number
              files (list): [config_file,sbox1_file,sbox2_file]
Return:       ciphertext (str)
Description:  Encryption using SDES CBC mode
Errors:       Similar to e_SDES
---------------------------------------------------
"""
def e_SDES_CBC(plaintext,key,files):
    ciphertext = ''
    if not isinstance(plaintext,str):
        print('Error(e_SDES_CBC): Invalid plaintext',end = '')
        return ''
    if plaintext == '':
        print('Error(e_SDES_CBC): Invalid plaintext',end = '')
        return ''
    
    encoding_type = get_SDES_value('encoding_type',files[0])
    if encoding_type == '':
        print('Error(e_SDES_CBC): Invalid configuration, Could not get encoding type ', end='')
        return ''
    
    block_size = get_SDES_value('block_size',files[0])
    if block_size == '':
        print('Error(e_SDES_CBC): Invalid configuration, Could not get block size ', end='')
        return ''
    
    key_size = get_SDES_value('key_size',files[0])
    if key_size == '':
        print('Error(e_SDES_CBC): Invalid configuration, Could not get key_size ', end='')
        return ''
    
    rounds = get_SDES_value('rounds',files[0])
    if rounds == '':
        print('Error(e_SDES_CBC): Invalid configuration, Could not get rounds ', end='')
        return ''
    
    if key == '': #Generate new key
        p = get_SDES_value('p',files[0])
        if p == '':
            print('Error(e_SDES_CBC): Invalid configuration, Could not get p ', end='')
            return ''
        q = get_SDES_value('q',files[0])
        if q == '':
            print('Error(e_SDES_CBC): Invalid configuration, Could not get q ', end='')
            return '' 
        key = generate_key_SDES(files[0])
    #Validate key_size
    #print(len(key))
    if len(key) % 2 == 0: #MAYBE?????
        print('Error(e_SDES_CBC): Invalid key', end='')
        return '' 
    
    
    #Get all undefined characters in text
    undefined = ''
    for c in plaintext:
        if encode(c,encoding_type) == '' and not c in undefined:
            undefined += c
    undefined_pos = utilities.get_positions(plaintext, undefined + '\n')
    cleaned_text = utilities.clean_text(plaintext, undefined) #add newline?
    
    blocks = []
    ndx = 0

    while ndx < len(cleaned_text) - 1: #Changed from len(cleaned) to len(cleaned - 1
        blocks.append([cleaned_text[ndx] + cleaned_text[ndx + 1]])
        ndx += 2
    if len(cleaned_text) % 2 == 1:
        blocks.append([cleaned_text[len(cleaned_text) - 1] + PAD]) #Added - 1 to here as well
        
    defined_blocks = []
    #print(blocks)
    for b in blocks:
        e_block = []

        lc = encode(b[0][0],encoding_type)
        rc = encode(b[0][1],encoding_type)
        '''
        if lc == '':
            print('lc: NOT IN ENCODIG')
        if rc == '':
            print('rc: NOT IN ENCODIG')
        '''        
        defined_blocks.append([lc + rc])
    '''    
    print("DEFINED_BLOCKS: ",end = '')
    for d in defined_blocks:
        print(d,end = '')
    print()
    '''
    binary_stream = ''    
    for db in defined_blocks:
        binary_stream += db[0]
        
    #print("BINARY_STREAM: " + binary_stream)
    ndx = 0
    f_binary_stream = ''
    iv = get_IV()
    while ndx < len(binary_stream):
        
        f_block = ''
        #Get block
        for i in range(int(block_size)):
            f_block += binary_stream[ndx]
            ndx += 1
            
        f_block = xor(iv,f_block)
        #print("Processing this block: " + f_block + " -> ",end='')
        #Run through feistel cipher x times
        for i in range(int(rounds)):
            
            new_key = get_subkey(key,i + 1,files[0])
            
            f_block = feistel(f_block, new_key, files)
            if i == int(rounds) - 1:
                f_block = swap(f_block)
                
            iv = f_block    
        #print(f_block)        
        f_binary_stream += f_block
        
    #print("F_BINARY_STREAM: " + f_binary_stream)
    
    #Swap two halves
    #swaped_bin = swap(f_binary_stream)
    swaped_bin = f_binary_stream
    
    #print("SWAPED_BIN: " + swaped_bin)
     
    #translate back
    ndx = 0
    while ndx < len(swaped_bin):
        s_block = ''
        #print(c)
        for i in range(int(int(block_size) / 2)): #It is this size atm since B6 uses 6 bits
            s_block += swaped_bin[ndx]
            ndx += 1
        #print("s_block: " + s_block)
        ciphertext += decode(s_block,encoding_type)
    #print("BEFORE CIPHERTEXT: " + ciphertext)    
    ciphertext = utilities.insert_positions(ciphertext, undefined_pos)
    
    #print("AFTER INSERT CIPHERTEXT: " + ciphertext)      
    return ciphertext
"""
----------------------------------------------------
Parameters:   plaintext (str)
              key (str): binary number
              files (list): [config_file,sbox1_file,sbox2_file]
Return:       ciphertext (str)
Description:  Encryption using SDES OFB mode
Errors:       Similar to e_SDES
---------------------------------------------------
"""
def e_SDES_OFB(plaintext,key,files):
    ciphertext = ''
    if not isinstance(plaintext,str):
        print('Error(e_SDES_OFB): Invalid plaintext',end = '')
        return ''
    if plaintext == '':
        print('Error(e_SDES_OFB): Invalid plaintext',end = '')
        return ''
    
    encoding_type = get_SDES_value('encoding_type',files[0])
    if encoding_type == '':
        print('Error(e_SDES_OFB): Invalid configuration, Could not get encoding type ', end='')
        return ''
    
    block_size = get_SDES_value('block_size',files[0])
    if block_size == '':
        print('Error(e_SDES_OFB): Invalid configuration, Could not get block size ', end='')
        return ''
    
    key_size = get_SDES_value('key_size',files[0])
    if key_size == '':
        print('Error(e_SDES_OFB): Invalid configuration, Could not get key_size ', end='')
        return ''
    
    rounds = get_SDES_value('rounds',files[0])
    if rounds == '':
        print('Error(e_SDES_OFB): Invalid configuration, Could not get rounds ', end='')
        return ''
    
    if key == '': #Generate new key
        p = get_SDES_value('p',files[0])
        if p == '':
            print('Error(e_SDES_OFB): Invalid configuration, Could not get p ', end='')
            return ''
        q = get_SDES_value('q',files[0])
        if q == '':
            print('Error(e_SDES_OFB): Invalid configuration, Could not get q ', end='')
            return '' 
        key = generate_key_SDES(files[0])
    #Validate key_size
    #print(len(key))
    if len(key) % 2 == 0: #MAYBE?????
        print('Error(e_SDES_OFB): Invalid key', end='')
        return '' 
    
    
    #Get all undefined characters in text
    undefined = ''
    for c in plaintext:
        if encode(c,encoding_type) == '' and not c in undefined:
            undefined += c
    undefined_pos = utilities.get_positions(plaintext, undefined + '\n')
    cleaned_text = utilities.clean_text(plaintext, undefined) #add newline?
    
    blocks = []
    ndx = 0
 
    while ndx < len(cleaned_text) - 1: #Changed from len(cleaned) to len(cleaned - 1
        blocks.append([cleaned_text[ndx] + cleaned_text[ndx + 1]])
        ndx += 2
    if len(cleaned_text) % 2 == 1:
        blocks.append([cleaned_text[len(cleaned_text) - 1] + PAD]) #Added - 1 to here as well
        
    defined_blocks = []
    #print(blocks)
    for b in blocks:
        e_block = []

        lc = encode(b[0][0],encoding_type)
        rc = encode(b[0][1],encoding_type)
        '''
        if lc == '':
            print('lc: NOT IN ENCODIG')
        if rc == '':
            print('rc: NOT IN ENCODIG')
        '''        
        defined_blocks.append([lc + rc])
    '''    
    print("DEFINED_BLOCKS: ",end = '')
    for d in defined_blocks:
        print(d,end = '')
    print()
    '''
    binary_stream = ''    
    for db in defined_blocks:
        binary_stream += db[0]
        
    #print("BINARY_STREAM: " + binary_stream)
    ndx = 0
    f_binary_stream = ''
    
    while ndx < len(binary_stream):
        f_block = ''
        #Get block
        for i in range(int(block_size)):
            f_block += binary_stream[ndx]
            ndx += 1
        #print("Processing this block: " + f_block + " -> ",end='')
        #Run through feistel cipher x times
        for i in range(int(rounds)):
            
            new_key = get_subkey(key,i + 1,files[0])
            f_block = feistel(f_block, new_key, files)
            if i == int(rounds) - 1:
                f_block = swap(f_block)
            
            #if ndx >= len(binary_stream) - 1: #FOR SOME REASON THIS DECODES IT BACK IF SUBKEY IS NOT UPDATED???????
                #f_block = swap(f_block)
                
        #print(f_block)        
        f_binary_stream += f_block
        
    #print("F_BINARY_STREAM: " + f_binary_stream)
    
    #Swap two halves
    #swaped_bin = swap(f_binary_stream)
    swaped_bin = f_binary_stream
    
    #print("SWAPED_BIN: " + swaped_bin)
     
    #translate back
    ndx = 0
    while ndx < len(swaped_bin):
        s_block = ''
        #print(c)
        for i in range(int(int(block_size) / 2)): #It is this size atm since B6 uses 6 bits
            s_block += swaped_bin[ndx]
            ndx += 1
        #print("s_block: " + s_block)
        ciphertext += decode(s_block,encoding_type)
    #print("BEFORE CIPHERTEXT: " + ciphertext)    
    ciphertext = utilities.insert_positions(ciphertext, undefined_pos)
    
    #print("AFTER INSERT CIPHERTEXT: " + ciphertext)      
    return ciphertext
"""
----------------------------------------------------
Parameters:   ciphertext (str)
              key (str): binary number
              files (list): [config_file,sbox1_file,sbox2_file]
Return:       plaintext (str)
Description:  Decryption using SDES ECB mode
Errors:       Similar to d_SDES
---------------------------------------------------
"""
def d_SDES_ECB(ciphertext,key,files):
    plaintext = ''
    if not isinstance(ciphertext,str):
        print('Error(d_SDES_ECB): Invalid ciphertext',end = '')
        return ''
    if ciphertext == '':
        print('Error(d_SDES_ECB): Invalid ciphertext',end = '')
        return ''
    
    encoding_type = get_SDES_value('encoding_type',files[0])
    if encoding_type == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get encoding type ', end='')
        return ''
    
    block_size = get_SDES_value('block_size',files[0])
    if block_size == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get block size ', end='')
        return ''
    
    key_size = get_SDES_value('key_size',files[0])
    if key_size == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get key_size ', end='')
        return ''
    
    rounds = get_SDES_value('rounds',files[0])
    if rounds == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get rounds ', end='')
        return ''
    if len(key) % 2 == 0: #MAYBE?????
        print('Error(e_SDES_ECB): Invalid key', end='')
        return '' 
    
    
    #Get all undefined characters in text
    undefined = ''
    for c in ciphertext:
        if encode(c,encoding_type) == '' and not c in undefined:
            undefined += c
    undefined_pos = utilities.get_positions(ciphertext, undefined + '\n')
    cleaned_text = utilities.clean_text(ciphertext, undefined) #add newline?
        
    #print(undefined_pos)
    #print(cleaned_text)
    cleaned_text = ciphertext
    #plaintext = e_SDES_ECB(ciphertext, key[::-1], files)
        
    blocks = []
    ndx = 0
    
    while ndx < len(cleaned_text):
        blocks.append([cleaned_text[ndx] + cleaned_text[ndx + 1]])
        ndx += 2
    if len(cleaned_text) % 2 == 1:
        blocks.append([cleaned_text[len(cleaned_text)] + PAD])
        
    defined_blocks = []
    #print(blocks)
    for b in blocks:
        lc = encode(b[0][0],encoding_type)
        rc = encode(b[0][1],encoding_type)
        '''
        if lc == '':
            print('lc: NOT IN ENCODIG')
        if rc == '':
            print('rc: NOT IN ENCODIG')
        '''        
        defined_blocks.append([lc + rc])
    '''    
    print("DEFINED_BLOCKS: ",end = '')
    for d in defined_blocks:
        print(d,end = '')
    print()
    '''
    binary_stream = ''    
    for db in defined_blocks:
        binary_stream += db[0]
        
    #print("BINARY_STREAM: " + binary_stream)
    ndx = 0
    f_binary_stream = ''
    
    while ndx < len(binary_stream):
        f_block = ''
        #Get block
        for i in range(int(block_size)):
            f_block += binary_stream[ndx]
            ndx += 1
        #print("Processing this block: " + f_block + " -> ",end='')
        #Run through feistel cipher x times
        for i in range(int(rounds)):
            
            new_key = get_subkey(key,int(rounds) - i,files[0])
            f_block = feistel(f_block, new_key, files)
            if i == int(rounds) - 1:
                f_block = swap(f_block)
                
        #print(f_block)        
        f_binary_stream += f_block
        
    #print("F_BINARY_STREAM: " + f_binary_stream)
    
    #Swap two halves
    #swaped_bin = swap(f_binary_stream)
    swaped_bin = f_binary_stream
    
    #print("SWAPED_BIN: " + swaped_bin)
     
    #translate back
    ndx = 0
    while ndx < len(swaped_bin):
        s_block = ''
        #print(c)
        for i in range(int(int(block_size) / 2)): #It is this size atm since B6 uses 6 bits
            s_block += swaped_bin[ndx]
            ndx += 1
        #print("s_block: " + s_block)
        plaintext += decode(s_block,encoding_type)
    #print("BEFORE CIPHERTEXT: " + ciphertext)    
    plaintext = utilities.insert_positions(plaintext, undefined_pos)
    
    return plaintext

"""
----------------------------------------------------
Parameters:   ciphertext (str)
              key (str): binary number
              files (list): [config_file,sbox1_file,sbox2_file]
Return:       plaintext (str)
Description:  Decryption using SDES CBC mode
Errors:       Similar to d_SDES
---------------------------------------------------
"""
def d_SDES_CBC(ciphertext,key,files):
    plaintext = ''
    if not isinstance(ciphertext,str):
        print('Error(d_SDES_ECB): Invalid ciphertext',end = '')
        return ''
    if ciphertext == '':
        print('Error(d_SDES_ECB): Invalid ciphertext',end = '')
        return ''
    
    encoding_type = get_SDES_value('encoding_type',files[0])
    if encoding_type == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get encoding type ', end='')
        return ''
    
    block_size = get_SDES_value('block_size',files[0])
    if block_size == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get block size ', end='')
        return ''
    
    key_size = get_SDES_value('key_size',files[0])
    if key_size == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get key_size ', end='')
        return ''
    
    rounds = get_SDES_value('rounds',files[0])
    if rounds == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get rounds ', end='')
        return ''
    if len(key) % 2 == 0: #MAYBE?????
        print('Error(e_SDES_ECB): Invalid key', end='')
        return '' 
    
    
    #Get all undefined characters in text
    undefined = ''
    for c in ciphertext:
        if encode(c,encoding_type) == '' and not c in undefined:
            undefined += c
    undefined_pos = utilities.get_positions(ciphertext, undefined + '\n')
    cleaned_text = utilities.clean_text(ciphertext, undefined) #add newline?
        

    cleaned_text = ciphertext

        
    blocks = []
    ndx = 0
    
    while ndx < len(cleaned_text):
        blocks.append([cleaned_text[ndx] + cleaned_text[ndx + 1]])
        ndx += 2
    if len(cleaned_text) % 2 == 1:
        blocks.append([cleaned_text[len(cleaned_text)] + PAD])
        
    defined_blocks = []
    #print(blocks)
    for b in blocks:
        lc = encode(b[0][0],encoding_type)
        rc = encode(b[0][1],encoding_type)
    
        defined_blocks.append([lc + rc])

    binary_stream = ''    
    for db in defined_blocks:
        binary_stream += db[0]
        
    #print("BINARY_STREAM: " + binary_stream)
    ndx = 0
    f_binary_stream = ''
    iv = get_IV()
    once_over = True
    while ndx < len(binary_stream):
        f_block = ''
        #Get block
        
        for i in range(int(block_size)):
            f_block += binary_stream[ndx]
            ndx += 1
        
        #print("Processing this block: " + f_block + " -> ",end='')
        #Run through feistel cipher x times
        for i in range(int(rounds)):
            
            new_key = get_subkey(key,int(rounds) - i,files[0])
            f_block = feistel(f_block, new_key, files)
            
            if i == int(rounds) - 1:
                
                f_block = swap(f_block)
                
            

                
        #print(f_block)
        #if once_over == True:
        f_block = xor(iv,f_block)
            
            #once_over = False        
        f_binary_stream += f_block
        
        
    #print("F_BINARY_STREAM: " + f_binary_stream)
    
    #Swap two halves
    #swaped_bin = swap(f_binary_stream)
    swaped_bin = f_binary_stream
    
    #print("SWAPED_BIN: " + swaped_bin)
     
    #translate back
    ndx = 0
    while ndx < len(swaped_bin):
        s_block = ''
        #print(c)
        for i in range(int(int(block_size) / 2)): #It is this size atm since B6 uses 6 bits
            s_block += swaped_bin[ndx]
            ndx += 1
        #print("s_block: " + s_block)
        plaintext += decode(s_block,encoding_type)
    #print("BEFORE CIPHERTEXT: " + ciphertext)    
    plaintext = utilities.insert_positions(plaintext, undefined_pos)
    
    return plaintext

"""
----------------------------------------------------
Parameters:   ciphertext (str)
              key (str): binary number
              files (list): [config_file,sbox1_file,sbox2_file]
Return:       plaintext (str)
Description:  Decryption using SDES OFB mode
Errors:       Similar to d_SDES
---------------------------------------------------
"""
def d_SDES_OFB(ciphertext,key,files):
    plaintext = ''
    if not isinstance(ciphertext,str):
        print('Error(d_SDES_ECB): Invalid ciphertext',end = '')
        return ''
    if ciphertext == '':
        print('Error(d_SDES_ECB): Invalid ciphertext',end = '')
        return ''
    
    encoding_type = get_SDES_value('encoding_type',files[0])
    if encoding_type == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get encoding type ', end='')
        return ''
    
    block_size = get_SDES_value('block_size',files[0])
    if block_size == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get block size ', end='')
        return ''
    
    key_size = get_SDES_value('key_size',files[0])
    if key_size == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get key_size ', end='')
        return ''
    
    rounds = get_SDES_value('rounds',files[0])
    if rounds == '':
        print('Error(d_SDES_ECB): Invalid configuration, Could not get rounds ', end='')
        return ''
    if len(key) % 2 == 0: #MAYBE?????
        print('Error(e_SDES_ECB): Invalid key', end='')
        return '' 
    
    
    #Get all undefined characters in text
    undefined = ''
    for c in ciphertext:
        if encode(c,encoding_type) == '' and not c in undefined:
            undefined += c
    undefined_pos = utilities.get_positions(ciphertext, undefined + '\n')
    cleaned_text = utilities.clean_text(ciphertext, undefined) #add newline?
        
    #print(undefined_pos)
    #print(cleaned_text)
    cleaned_text = ciphertext
    #plaintext = e_SDES_ECB(ciphertext, key[::-1], files)
        
    blocks = []
    ndx = 0
    
    while ndx < len(cleaned_text):
        if ndx <= len(cleaned_text) - 2:
            blocks.append([cleaned_text[ndx] + cleaned_text[ndx + 1]])
        ndx += 2
    if len(cleaned_text) % 2 == 1:
        #if len(cleaned_text)
        blocks.append([cleaned_text[len(cleaned_text) - 1] + PAD]) #ADD -1
        
    defined_blocks = []
    #print(blocks)
    for b in blocks:
        lc = encode(b[0][0],encoding_type)
        rc = encode(b[0][1],encoding_type)
        '''
        if lc == '':
            print('lc: NOT IN ENCODIG')
        if rc == '':
            print('rc: NOT IN ENCODIG')
        '''        
        defined_blocks.append([lc + rc])
    '''    
    print("DEFINED_BLOCKS: ",end = '')
    for d in defined_blocks:
        print(d,end = '')
    print()
    '''
    binary_stream = ''    
    for db in defined_blocks:
        binary_stream += db[0]
        
    #print("BINARY_STREAM: " + binary_stream)
    ndx = 0
    f_binary_stream = ''
    
    while ndx < len(binary_stream):
        f_block = ''
        #Get block
        for i in range(int(block_size)):
            if ndx < len(binary_stream):
                f_block += binary_stream[ndx]
            ndx += 1
        #print("Processing this block: " + f_block + " -> ",end='')
        #Run through feistel cipher x times
        for i in range(int(rounds)):
            
            new_key = get_subkey(key,int(rounds) - i,files[0])
            f_block = feistel(f_block, new_key, files)
            if i == int(rounds) - 1:
                f_block = swap(f_block)
            
            #if ndx >= len(binary_stream) - 1: #FOR SOME REASON THIS DECODES IT BACK IF SUBKEY IS NOT UPDATED???????
                #f_block = swap(f_block)
                
        #print(f_block)        
        f_binary_stream += f_block
        
    #print("F_BINARY_STREAM: " + f_binary_stream)
    
    #Swap two halves
    #swaped_bin = swap(f_binary_stream)
    swaped_bin = f_binary_stream
    
    #print("SWAPED_BIN: " + swaped_bin)
     
    #translate back
    ndx = 0
    while ndx < len(swaped_bin):
        s_block = ''
        #print(c)
        for i in range(int(int(block_size) / 2)): #It is this size atm since B6 uses 6 bits
            s_block += swaped_bin[ndx]
            ndx += 1
        #print("s_block: " + s_block)
        plaintext += decode(s_block,encoding_type)
    #print("BEFORE CIPHERTEXT: " + ciphertext)    
    plaintext = utilities.insert_positions(plaintext, undefined_pos)
    
    return plaintext

def LFSR(c,IG,bits):
    if not isinstance(bits,int):
        print("Error(LFSR): Invalid bits")
        return ''
    if not isinstance(c,list):
        print("Error(LFSR): Invalid list")
        return ''
    if not isinstance(IG,str):
        print("Error(LFSR): Invalid IG")
        return ''
                
    if bits < 1:
        print("Error(LFSR): Invalid bits")
        return ''        
    num_registers = len(c)
    if len(IG) != num_registers:
        print("Error(LFSR): Invalid IG")
        return ''
    
      
    bit_string = ''
    new_IG = IG[:]    
    #Addition mod 2 is equivelent to XOR
    #bit_string = IG

    ndx = 0       
    for i in range(bits - 1):
        #print(new_IG)
        result = 0
        ndx = 0
        bit_string += new_IG[len(new_IG) - 1]
        for num in c:
            result += int(new_IG[ndx]) * num
            ndx += 1
        result = result % 2

        new_IG = str(result) + new_IG[:len(new_IG) - 1]
        
    #compute last register
    b = 0
    for i in range(len(c)):
        b += c[i] * int(IG[i])
    b = b % 2    
    bit_string += str(b)
    return bit_string

def get_IV():
    rand_bin = ''
    num_bits = int(get_SDES_value('block_size'))
    key_size = int(get_SDES_value('key_size'))
    #num_reg = int(num_bits/key_size)
    num_reg = int(key_size//2)
    #print(num_bits)
    #print(key_size)
    c = [0]
    for i in range(num_reg - 1):
        if c[len(c) - 1] == 0:
            c.append(1)
        elif c[len(c) - 1] == 1:
            c.append(0)
    IG = str(bin(key_size)[1:].replace('b',''))
    #print("IG: " + IG + " Len: " + str(len(IG)) + "  num_reg: " + str(num_reg))
    rand_bin = LFSR(c,IG,num_bits)
    
    return rand_bin

def get_SDES3_key():
    key = '100110100'
    return key