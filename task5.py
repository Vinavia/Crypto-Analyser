"""
-----------------------------
CP460 (Fall 2020)
Name: Matthew Chiarelli
ID:   150798950
Final Exam
-----------------------------
"""
DICT_FILE = 'engmix.txt'
PAD = 'q'
BLOCK_MAX_SIZE = 20

import math
import string
import mod
import matrix
import utilities


"""
----------------------------------------------------
Parameters:   start (str): an ASCII character
              size (int) number of rows & columns in square
Return:       square (str): A string representing a Polybius square
Description:  Creates a string that begins with 'start' character and 
              contains consecutive ASCII characters that are good to fill
              the given size of a polybius square
Asserts:      start is a single character string
              size is an integer >= 2
---------------------------------------------------
"""
def get_polybius_square(start,size):
    
    if ord(start) > 126 or ord(start) < 32:
        start = ' '
        
    if size < 2:
        size = 2
        
    space_needed = size * size
    polybius_square = ""
      
    if space_needed > 126 - ord(start):
        return polybius_square
    
    
    increment = 0
    for r in range(size):    
        for c in range(size):
            polybius_square += chr(ord(start) + increment)
            increment += 1
            
   
    return polybius_square

"""--------------------------------------------------------------
Parameters:   plaintext (str)
              key (tuple(str,int))
Return:       ciphertext (str)
Description:  Encryption using Polybius Square
Asserts:      plaintext is a string
              key is a tuple containing a single character and an integer
--------------------------------------------------------------
"""
def e_polybius(plaintext, key):
    ciphertext = ""
    pbs = get_polybius_square(key[0], key[1])
    
    if pbs == "":
        print('Error(e_polybius): invalid polybius square')
        return ciphertext
    
    for plainchar in plaintext:
        
        try:  
            ndx = pbs.index(plainchar)
        except ValueError:
            ndx = None
            
        if ndx == None:
            ciphertext += plainchar
        else:
            row_num = math.floor(ndx / key[1]) + 1
            col_num = (ndx % key[1]) + 1
            ciphertext += str(row_num) + str(col_num)
            
            
    return ciphertext

"""
-------------------------------------------------------
Parameters:   ciphertext(str)
              key (tuple(str,int))
Return:       plaintext (str)
Description:  Decryption using Polybius Square
Asserts:      ciphertext is a string
              key is a tuple containing a single character and an integer
-------------------------------------------------------
"""
def d_polybius(ciphertext, key):
    plaintext = ""
    pbs = get_polybius_square(key[0], key[1])
    currentchar = 0
    if pbs == "":
        print('Error(e_polybius): invalid polybius square')
        return plaintext
    pbs_arr = [[None] * key[1] for i in range(key[1])]
    
    for r in range(key[1]):    
        for c in range(key[1]):
            pbs_arr[r][c] = pbs[0]
            pbs = pbs[1:]
        
    for cipherchar in ciphertext:
        
        if currentchar >= 0:
            "I ADDED THE AND~~~~ part"
            if cipherchar.isnumeric() and ciphertext[currentchar + 1].isnumeric():#it is encrypted, read two
                #print(ciphertext[currentchar + 1])
                plaintext += pbs_arr[int(cipherchar) - 1][int(ciphertext[currentchar + 1]) - 1]
                currentchar += 2
                currentchar *= -1
            else:
                plaintext += cipherchar
                currentchar += 1
        else:
            currentchar *= -1
            #print("skipped")
                

    return plaintext

"""
----------------------------------------------------
Parameters:   key (b,r): tuple(int,int)
Return:       updated_key (b,r): tuple(int,int)
Description:  Private helper function for block rotate cipher
              Update the key to smallest positive value
              if an invalid key return (0,0)
Asserts:      None
---------------------------------------------------
"""
def _adjust_key_block_rotate(key):
    updated_key = (0,0)
    
    if not type(key) is tuple:
        return updated_key
     
    if not type(key[0]) is int or not type(key[1]) is int:
        return updated_key
    
    if key[0] < 1:
        return updated_key
    
    
    updated_key = list(updated_key)
    
    updated_key[0] = key[0]
    updated_key[1] = key[1]
    
    if key[1] < 0: #if negative
        
        #shift size should be smaller then block size 
        if key[0] > (key[1] * -1):
            updated_key[1] = (key[1] * -1)  % key[0]
    else:
        #shift size should be smaller then block size 
        if key[0] < key[1]:
            updated_key[1] = key[1]  % key[0]
            
    updated_key = tuple(updated_key)
    
        
    return updated_key

"""
----------------------------------------------------
Parameters:   plaintext (str)
              key (tuple(int,int))
Return:       ciphertext (str)
Description:  Encryption using Block Rotation Cipher
              Uses left circular rotation + padding
Asserts:      plaintext is a string
Errors:       if invalid key: 
                print: "Error(e_block_rotate): invalid key"
                return empty string
---------------------------------------------------
"""
def e_block_rotate(plaintext,key):
    ciphertext = ""
    e_key = _adjust_key_block_rotate(key)
    
    if e_key == (0,0):
        print("Error(e_block_rotate): invalid key")
        return ciphertext
    
    blocktext = text_to_blocks(plaintext, e_key[0], 1)
    
    for block in blocktext:
        block = shift_string(block,e_key[1],'l')
        ciphertext += block

        
    return ciphertext


"""
----------------------------------------------------
Parameters:   text (string): input string
              shifts (int): number of shifts
              direction (str): 'l' or 'r'
Return:       update_text (str)
Description:  Shift a given string by given number of shifts (circular shift)
              If shifts is a negative value, direction is changed
              If no direction is given or if it is not 'l' or 'r' set to 'l'
Asserts:      text is a string and shifts is an integer
---------------------------------------------------
"""
def shift_string(text,shifts,direction='l'):
    updated_text = text
    numNewline = 0
    if not direction.isalpha():
        direction = 'l'
        
    if direction != 'r' and direction != 'l':
        direction = 'l'
    
    
    if shifts < 0:
        if direction == 'l':
            direction = 'r'
        elif direction == 'r':
            direction = 'l'
                     
        shifts *= -1
        
    if direction == 'l':
        for i in range(shifts + numNewline):
            updated_text = shift_left(updated_text)
    elif direction == 'r':
        for i in range(shifts + numNewline):
            updated_text = shift_right(updated_text)
        
    return updated_text

"""
----------------------------------------------------
Parameters:   text (string): input string
Return:       update_text (str)
Description:  text will be shifted one space to the left
Asserts:      text is a string
---------------------------------------------------
"""
def shift_left(text):
    updated_text = text
    c = updated_text[0]
    
    updated_text = updated_text[1:] + c
    
    return updated_text

"""
----------------------------------------------------
Parameters:   text (string): input string
Return:       update_text (str)
Description:  text will be shifted one space to the right
Asserts:      text is a string
---------------------------------------------------
"""
def shift_right(text):
    updated_text = text
    c = updated_text[len(updated_text) - 1]
    
    updated_text = c + updated_text[:len(updated_text) - 1]
    
    return updated_text

"""
----------------------------------------------------
Parameters:   text (str)
              block_size (int)
              padding (bool): False/default = no padding, True = padding
              pad (str): default = PAD
Return:       blocks (list)
Description:  Create a list containing strings each of given block size
              if padding flag is set, pad using given padding character
              if no padding character given, use global PAD
Asserts:      text is a string and b_size is a positive integer
---------------------------------------------------
"""
def text_to_blocks(text,b_size,padding = 0,pad =PAD):
    blocks = []
    block = ""
    

    
    for c in text:
        
        block = block + c
        
        if b_size <= len(block):
            
            blocks.append(block)
            block = ""
            
    if block != "":
        blocks.append(block)
    
    if padding:        
        #Pad ending
        while len(blocks[len(blocks) - 1]) < b_size:
            blocks[len(blocks) - 1] += pad
    #print(blocks)     
    return blocks

"""
----------------------------------------------------
Parameters:   text (str)
              base (str)
Return:       positions (2D list)
Description:  Analyzes a given text for any occurrence of base characters
              Returns a 2D list with characters and their respective positions
              format: [[char1,pos1], [char2,pos2],...]
              Example: get_positions('I have 3 cents.','c.h') -->
              [['h',2],['c',9],['.',14]]
              Text and base are not changed
Asserts:      text and base are strings
---------------------------------------------------
"""
def get_positions(text,base):
    
    #word = word if word[0].isalpha() or word[0].isnumeric()  else word[1:]
    #        try:  
    #        ndx = pbs.index(plainchar)
    #    except ValueError:
    #        ndx = None
    positions = []
    matches = True
    ndx = 0
    for c in base:
        #print("checking: " + c)
        while(matches and ndx < len(text)):
            try:
                ndx = text.index(c, ndx)
                #print("Found at: " + str(ndx))
                positions.append([c,ndx])
                ndx += 1
            except ValueError:
                #print("No matches.")
                matches = False

        matches = True
        ndx = 0   
    #Sort list
    positions.sort(key=getSecond)    
    
    return positions
"""
----------------------------------------------------
Parameters:   arr (list)
Return:       arr (list[1])
Description:  returns the second index of a given array
              
Asserts:      arr is an array of at least length 2
---------------------------------------------------
"""
def getSecond(arr):
    return arr[1]
"""
----------------------------------------------------
Parameters:   arr (list)
Return:       arr (list[0])
Description:  returns the first index of a given array
              
Asserts:      arr is an array of at least length 2
---------------------------------------------------
"""
def getFirst(arr):
    return arr[0]
"""
----------------------------------------------------
Parameters:   ciphertext (str)
              key (tuple(int,int))
Return:       plaintext (str)
Description:  Decryption using Block Rotation Cipher
              Removes padding if it exist
Asserts:      ciphertext is a string
Errors:       if invalid key: 
                print: "Error(d_block_rotate): invalid key" 
                return empty string
---------------------------------------------------
"""
def d_block_rotate(ciphertext,key):
    plaintext = ""
    e_key = _adjust_key_block_rotate(key)
    
   

    
    if e_key == (0,0):
        print("Error(e_block_rotate): invalid key")
        return plaintext
    
    newlinePos = get_positions(ciphertext, "\n") #track newlien positions
    #print(newlinePos)
    blocktext = text_to_blocks(ciphertext.replace("\n", ""), e_key[0], 1) #give text as removed newlines 
    #print(e_key[1])


    for block in blocktext:
        
        block = shift_string(block, e_key[1], 'r')
        plaintext += block

    while plaintext[len(plaintext) - 1] == PAD:
        plaintext = plaintext[:len(plaintext) - 1]
        
    #add back newlines
    plaintext = insert_positions(plaintext,newlinePos)   
    
    return plaintext
"""
----------------------------------------------------
Parameters:   text (str)
              positions (lsit): [[char1,pos1],[char2,pos2],...]]
Return:       updated_text (str)
Description:  Inserts all characters in the positions 2D list into their respective
Asserts:      text is a string and positions is a list
---------------------------------------------------
"""
def insert_positions(text, positions):
    updated_text = text
    
    for c in positions:
        updated_text = updated_text[0:c[1]] + c[0] + updated_text[c[1]:]  
    
    return updated_text

"""
----------------------------------------------------
Parameters:   ciphertext (string)
              arguments (list): [b0,bn,r] default = [0,0,0]
                          b0: minimum block size
                          bn: maximum block size
                          r: rotations
Return:       key,plaintext
Description:  Cryptanalysis of Block Rotate Cipher
              Returns plaintext and key (r,b)
              Attempts block sizes from b1 to b2 (inclusive)
              If bn is invalid or unspecified use BLOCK_MAX_SIZE
              Minimum valid value for b0 is 1
---------------------------------------------------
"""
def cryptanalysis_block_rotate(ciphertext, arguments=[0,0,0]):
    
    key = ''
    plaintext = ''
    b0 = arguments[0]
    bn = arguments[1]
    r = arguments[2]
    #print(arguments)

        
    dict_list = utilities.load_dictionary(DICT_FILE) 
    

    
    if b0 == 0 and bn == 0 and r == 0: # Unknown everything
        #print("Everythign unknown")
        bn = BLOCK_MAX_SIZE
        b0 = 2
        for i in range(b0, bn + 1):
            for rot in range(i):
                attempt = (i, rot)
                attempt_text = d_block_rotate(ciphertext, attempt)
                
                if utilities.is_plaintext(attempt_text, dict_list,0.40):

                    plaintext = attempt_text
                    key = attempt
                    plaintext.rstrip("q")
                    return key, plaintext         
    elif r > 0:
        if bn == 0:
            bn = BLOCK_MAX_SIZE
        #print("Rotations known")
        for i in range(1, BLOCK_MAX_SIZE):
            attempt = (i, r)
            attempt_text = d_block_rotate(ciphertext, attempt)
            print(attempt_text)
            if utilities.is_plaintext(attempt_text, dict_list,0.4):
                #print(plaintext)
                plaintext = attempt_text
                key = attempt 
                plaintext.rstrip("q")
                return key, plaintext   
    else:
        if bn == 0:
            bn = BLOCK_MAX_SIZE
        #print("Rotations NOT known")
        for i in range(b0, bn + 1):
            for rot in range(i):
                attempt = (i, rot)
                attempt_text = d_block_rotate(ciphertext, attempt)
                print(attempt_text)
                #if i == 8 and rot == 5:
                    #print(attempt_text)
                    #print(d_block_rotate(ciphertext, attempt))
                if utilities.is_plaintext(attempt_text, dict_list,0.4):
                    #print(plaintext)
                    plaintext = attempt_text
                    key = attempt
                    plaintext.rstrip("q")
                    return key, plaintext   

    return key,plaintext
"""
----------------------------------------------------
Parameters:   letters (str)
              l (str)
Return:       order (int)
Description:  Returns order in which the character appears in the given string
              If letter not in letters --> return None
              
Asserts:      None
----------------------------------------------------
"""
def _get_letter_order(l, letters):
    order = None
    ndx = 0
    
    for c in letters:
        if c == l:
            order = ndx
            return order
        
        ndx += 1
        
    return order

"""
----------------------------------------------------
Parameters:   key (str)           
Return:       key_order (list)
Description:  Returns key order, e.g. [face] --> [1,2,3,0]
              If invalid key --> return []
              Applies to all ASCII characters from space to ~
Asserts:      None
----------------------------------------------------
"""
def _get_order_ct(key):
    key_order = []
    order_values = []
    order_string = ""
    collapsed_key = ""
    order_ndx = 0
    used_values = ""
    base_string = ' ' + utilities.get_base('all')
    if len(key) < 1 or not isinstance(key, str):
        return key_order
    
    for c in key:
        if c not in base_string:
            return key_order
        
        if c not in used_values:
            
            order_values.append([c, _get_letter_order(c, base_string)])
            used_values += c

    for i in order_values:
        collapsed_key += i[0]
         
    used_values = ""
        
    order_values.sort(key=getSecond)
    
    
    
    for i in order_values:
        i[1] = order_ndx
        order_string += i[0]
        order_ndx += 1
        
    for c in order_string:
        if c not in used_values:
            for i in order_values:
                if c == i[0]:      
                    key_order.append(_get_letter_order(c, collapsed_key))
                    used_values += c
      
    return key_order
"""
----------------------------------------------------
Parameters:   r: #rows (int)
              c: #columns (int)
              fill (str,int,double)
Return:       empty matrix (2D List)
Description:  Create an empty matrix of size r x c
              All elements initialized to fill
---------------------------------------------------
"""
def new_matrix(r,c,fill):
    r = r if r >= 2 else 2
    c = c if c>=2 else 2
    return [[fill] * c for i in range(r)]
"""
----------------------------------------------------
# Parameters:   marix (2D List)
# Return:       text (string)
# Description:  convert a 2D list of characters to a string
#               left to right, then top to bottom
#               Assumes given matrix is a valid 2D character list
---------------------------------------------------
"""
def matrix_to_string(matrix):
    text = ""
    
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] != None:
                text += matrix[row][col]
            
    return text
"""
----------------------------------------------------
Parameters:   plaintext (str)
              kye (str)
Return:       ciphertext (list)
Description:  Encryption using Columnar Transposition Cipher
              Does not include whitespaces in encryption
              Uses padding
Asserts:      plaintext is a string
Errors:       if key is invalid:
                print: Error(e_ct): invalid key
----------------------------------------------------
"""
def e_ct(plaintext,key):
    ciphertext = ""
    key_order = _get_order_ct(key)
    text_ndx = 0
    temp_col = []
    if key_order == []:
        print("Error(e_ct): invalid key")
        return ciphertext
    
    rows = math.ceil(len(plaintext)/len(key_order))
    tpm = new_matrix(rows, len(key_order), None) 
    new_tpm = new_matrix(rows, len(key_order), None) 
    #insert text into transposition matrix
    for row in range(len(tpm)):
        for col in range(len(tpm[0])):
            
            if len(plaintext) > text_ndx:
                tpm[row][col] = plaintext[text_ndx]
                text_ndx += 1
            else:
               tpm[row][col] = PAD
    text_ndx = 0
    #print(tpm)
    for i in key_order:  
        # get associated column
        for col in range(len(tpm)):
            temp_col.append(tpm[col][i])
            new_tpm[col][text_ndx] = temp_col[col]
              
        text_ndx += 1
        temp_col = []
        
    ciphertext = matrix_to_string(new_tpm)
      
    return ciphertext

"""
----------------------------------------------------
Parameters:   ciphertext (str)
              kye (str)
Return:       plaintext (list)
Description:  Decryption using Columnar Transposition Cipher
Asserts:      ciphertext is a string
Errors:       if key is invalid:
                print: Error(d_ct): invalid key
----------------------------------------------------
"""
def d_ct(ciphertext,key):
    plaintext = ""
    key_order = _get_order_ct(key)
    text_ndx = 0
    c_key = key
    if key_order == []:
        print("Error(d_ct): invalid key")
        return plaintext
    

    rows = math.ceil(len(ciphertext)/len(key_order))
    tpm = new_matrix(rows, len(key_order), None) 
    new_tpm =new_matrix(rows, len(key_order), None)
    
    #insert text into transposition matrix
    for row in range(len(tpm)):
        for col in range(len(tpm[0])):
            
            if len(ciphertext) > text_ndx:
                
                tpm[row][col] = ciphertext[text_ndx]
                text_ndx += 1
            else:
                tpm[row][col] = PAD
               
    text_ndx = 0
    
    for i in key_order:  
        # get associated column
        for col in range(len(tpm)):
            
            new_tpm[col][i] = tpm[col][_get_letter_order(c_key[text_ndx], c_key)]

        c_key = c_key[:_get_letter_order(c_key[text_ndx], c_key)] + "~" + c_key[_get_letter_order(c_key[text_ndx], c_key)+1:] # i know this is lazy AF pls forgive me
        
        text_ndx += 1                
    
    plaintext = matrix_to_string(new_tpm)
    
    #strip padding
    while plaintext[len(plaintext) - 1] == PAD:
        plaintext = plaintext[:len(plaintext) - 1]
            
    return plaintext
"""
----------------------------------------------------
Parameters:   text (str)
Return:       word_list (list)
Description:  Reads a given text
              Returns a list of strings, each pertaining to a word in file
              Words are separated by a white space (space, tab or newline)
              Gets rid of all special characters at the start and at the end
Asserts:      text is a string
---------------------------------------------------
"""
def text_to_words(text):
    
    word_list = []

    for word in text.split():
 
        if any(c.isalpha() for c in word) or any(c.isnumeric() for c in word): # if there is at least one letter or number
        
            while(not word[0].isalpha() and not word[0].isnumeric()): #trim beginning
                word = word if word[0].isalpha() or word[0].isnumeric()  else word[1:]
            

            
            while(not word[len(word) - 1].isalpha() and not word[len(word) - 1].isnumeric()): #trim end
                word = word if word[len(word) - 1].isalpha() or word[len(word) - 1].isnumeric() else word[:len(word) - 1]


        if len(word) > 0:               
            word_list.append(word)
        
    return word_list
"""
----------------------------------------------------
Parameters:   text (str)
              dict_list (list)
Return:       match (int)
              mismatch (int)
Description:  Reads a given text, checks if each word appears in given dictionary
              Returns number of matches and number of mismatches.
              Words are compared in lowercase
              Assumes a proper dict_list
Asserts:      text is a string and dict_list is a string
---------------------------------------------------
"""
def analyze_text(text, dict_list):
    assert type(text) == str and type(dict_list) == list, 'invalid inputs'
    word_list = text_to_words(text)
    alphabet = get_base('lower')
    match = 0
    mismatch = 0
    for w in word_list:
        if w.isalpha():
            list_num = alphabet.index(w[0].lower())
            if w.lower() in dict_list[list_num]:
                match+=1
            else:
                mismatch+=1
        else:
            mismatch+=1
    return match,mismatch
"""
----------------------------------------------------
Parameters:   base_type (str) 
Return:       result (str)
Description:  Return a base string containing a subset of ASCII charactes
              Defined base types:
              lower: lower case characters
              upper: upper case characters
              alpha: upper and lower case characters
              num: numerical characters
              lowernum: lower case and numerical characters
              uppernum: upper case and numerical characters
              alphanum: upper, lower and numerical characters
              nonalpha: all non alphabetical characters
              special: punctuations and special characters (no white space)
              all: upper, lower, numerical and special characters
---------------------------------------------------
"""
def get_base(base_type):
    lower = "".join([chr(ord('a')+i) for i in range(26)])
    upper = lower.upper()
    num = "".join([str(i) for i in range(10)])
    special = ''
    for i in range(ord('!'),127):
        if not chr(i).isalnum():
            special+= chr(i)
            
    result = ''
    if base_type == 'lower':
        result = lower
    elif base_type == 'upper':
        result = upper
    elif base_type == 'alpha':
        result = upper + lower
    elif base_type == 'num':
        result = num
    elif base_type == 'lowernum':
        result = lower + num
    elif base_type == 'uppernum':
        result = upper + num
    elif base_type == 'alphanum':
        result = upper + lower + num
    elif base_type == 'special':
        result = special
    elif base_type == 'nonalpha':
        result = special + num
    elif base_type == 'all':
        result = upper + lower + num + special
    else:
        print('Error(get_base): undefined base type')
        result = ''
    return result

"""
----------------------------------------------------
Parameters:   text (str)
              dict_list (str): dictionary list
              threshold (float): number between 0 to 1
Return:       True/False
Description:  Check if a given file is a plaintext
              If #matches/#words >= threshold --> True
                  otherwise --> False
              If invalid threshold or not given, default is 0.9
              An empty string should return False
              Assumes a valid dict_list is passed
---------------------------------------------------
"""
def is_plaintext(text, dict_list, threshold=0.9):
    if text == '':
        return False
    result = analyze_text(text, dict_list)
    if (result[0]+result[1]) != 0:
        percentage = result[0]/(result[0]+result[1])
    else:
        return False
    if threshold <= 0 or threshold > 1:
        threshold = 0.9
    if percentage >= threshold:
        return True
    return False

"""
----------------------------------------------------
Parameters:   ciphertext (str)
              size (int)
Return:       key (str)
              plaintext (str)
Description:  Apply brute-force to break polybius cipher
              The size of the polybius square is given
              The square is always located between [' ', '~'] ASCII characters
              Use threshold of 0.93
Asserts:      ciphertext is a string
              size is an integer
---------------------------------------------------
"""
def cryptanalysis_polybius(ciphertext,size):
    plaintext = ""
    key = None
    #max size is 11, min size is 2
    key_range = [50,126]
    #60 - orig 32
    space_required = 0
    #imediately, u can trim away impossible keys due to size of square (to few spaces)
    space_needed = size * size  
    key_range[1] -= space_needed
    ea_key = 0
    dict_list = utilities.load_dictionary(DICT_FILE)
    for i in range(key_range[0],key_range[1]):
        attempt = d_polybius(ciphertext, (chr(i),size))
        
        #EATBASH ATTEMPTS
        #ea_key,attempt = cryptanalysis_eatbash(attempt)
        #Decimation attempts
        #key,attempt,counter = cryptanalysis_decimation(attempt)
        #key_b,attempt = cryptanalysis_block_rotate(attempt, [3,20,5])
        #print("NEXT POLY: " + str(i))
        #print(attempt)
        #q = w
        #p = t
        #y = u
        #i = y
        #y = i
        if is_plaintext(attempt, dict_list, 0.44):
              
            plaintext = attempt
            plaintext = plaintext.replace('q','w')
            plaintext = plaintext.replace('p','t')
            plaintext = plaintext.replace('y','u')
            plaintext = plaintext.replace('i','y')
            #plaintext = plaintext.replace('y','i')
            #print(plaintext)
            key = (chr(i),size)
            #print(str(i) + " FOUND!! " + key[0])
            return key, plaintext
    
    #print("FAILURE AWWWWWW")     
    return key,plaintext

"""
----------------------------------------------------
            Task 2: Extended Atbash Cipher
----------------------------------------------------
"""

"""
----------------------------------------------------
Parameters:     plaintext(str)
                key (int)
Return:         ciphertext (str)
Description:    Encryption using Atbash Cipher
                If key = 0, uses lower case base
                If key = 1, uses upper case base
                If key = 2: uses upper+lower case
                If key = 3: uses upper+lower+num
                If key = 4: uses upper+lower+num+special
Asserts:      plaintext is a string and key is an integer
---------------------------------------------------
"""
def e_eatbash(plaintext, key):
    assert type(plaintext) == str , 'invalid plaintext'
    
    
    if key > 4 or key < 0:
        key = key % 5

    if key == 0:
        alphabet = utilities.get_base('lower')
    elif key == 1:
        alphabet = utilities.get_base('upper')
    elif key == 2:
        alphabet = utilities.get_base('alpha')
    elif key == 3:
        alphabet = utilities.get_base('alphanum')        
    elif key == 4:
        alphabet = utilities.get_base('all')   
         

    ciphertext = ''
   
    if key == 0:#lower
        for plainchar in plaintext:
        
            if plainchar.isalpha(): #if letter and uppercase, flag upper as True
                upper = True if plainchar.isupper() else False

                cipherchar = alphabet[25 - alphabet.index(plainchar.lower())]
                ciphertext += plainchar.upper() if upper else cipherchar #this supposed to be cipherchar??
            else: #ignore encryption of none-letters
                ciphertext += plainchar
                
    elif key == 1:#upper

        for plainchar in plaintext:
            
            if plainchar.isalpha():
                lower = True if plainchar.islower() else False
            
                cipherchar = alphabet[25 - alphabet.index(plainchar.upper())]
                ciphertext += plainchar.lower() if lower else cipherchar
            else: #ignore encryption of none-letters
                ciphertext += plainchar 
                           
    elif key == 2:#alpha
        for plainchar in plaintext:
            if plainchar.isalpha():
                cipherchar = alphabet[51 - alphabet.index(plainchar)]
                ciphertext += cipherchar

            else: #ignore encryption of none-letters
                ciphertext += plainchar      
    elif key == 3:#alphanumn
        for plainchar in plaintext:
            if plainchar.isalpha() or plainchar.isnumeric():
                
                cipherchar = alphabet[61 - alphabet.index(plainchar)]
                ciphertext += cipherchar
            else:
                ciphertext += plainchar 
    elif key == 4:#all NOT DONE
        
        for plainchar in plaintext:

            if plainchar in alphabet:    
                cipherchar = alphabet[(len(alphabet) - 1) - alphabet.index(plainchar)]      
                ciphertext += cipherchar
            else:
                ciphertext += plainchar
            
    return ciphertext

"""
----------------------------------------------------
Parameters:   ciphertext(str)
              key (int)
Return:       plaintext (str)
Description:  Decryption using Atbash Cipher
              There is no key (None)
              Decryption can be achieved by encrypting ciphertext!!
Asserts:      ciphertext is a string and key is an integer
----------------------------------------------------
"""
def d_eatbash(ciphertext, key):
    #iterate through text flagging which characters are used
    plaintext = e_eatbash(ciphertext, key)
    return plaintext
"""
----------------------------------------------------
Parameters:   ciphertext(str)
Return:       key (str)
              plaintext (str)
Description:  Cryptanalysis of Extended Atbash Cipher
              Key is in the range of 0-4
              Uses default dictionary file and threshold of 0.8
Asserts:      ciphertext is a string
----------------------------------------------------
"""
def cryptanalysis_eatbash(ciphertext):
    key = None
    plaintext = ''
    dict_list = utilities.load_dictionary(DICT_FILE)
    for k in range(0,4):
        if is_plaintext(d_eatbash(ciphertext,k),dict_list,0.8):
            plaintext = d_eatbash(ciphertext,k)
            key = k
            exit
    
    
    return key,plaintext

#---------------------------------
#       Q5: Hill Cipher          #
#---------------------------------
#-----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (str)
# Return:       ciphertext (str)
# Description:  Encryption using Hill Cipher, 2x2 (mod 26)
#               key is a string consisting of 4 characters
#                   if key is too short, make it a running key
#                   if key is too long, use first 4 characters
#               Encrypts only alphabet characters
#               Deals with plaintext as lower case, 
#               and produces upper case ciphertext
#               If necessary use default padding
# Errors:       if key is is invalid:
#                   print error msg and return empty string
# Asserts:      plaintext is a non-empty string
#-----------------------------------------------------------
def e_hill(plaintext,key):
    #polygraphic sub cipher
    ciphertext = ''
     
    k_word = key.lower()
    alphabet = utilities.get_base('lower')
    
    if len(k_word) > 4:
        k_word = k_word[:4]
           
    elif len(k_word) < 4:
        
        i = 0
        while len(k_word) < 4:
            #if not alphabet[i] in k_word: to not repeat letters
            k_word = k_word + alphabet[i]
            i += 1
    #print(k_word)        
            
    k_mat = [[0,0],[0,0]]
    
    #insert
    k_mat[0][0] = k_word[0]
    k_mat[0][1] = k_word[1]
    k_mat[1][0] = k_word[2]
    k_mat[1][1] = k_word[3]
    
    #replace with ndx in alphabet
    k_mat[0][0] = utilities._get_elem_ndx_first(alphabet, k_mat[0][0])
    k_mat[0][1] = utilities._get_elem_ndx_first(alphabet, k_mat[0][1])
    k_mat[1][0] = utilities._get_elem_ndx_first(alphabet, k_mat[1][0])
    k_mat[1][1] = utilities._get_elem_ndx_first(alphabet, k_mat[1][1])
    
    #Check if its invertible
    if not mod.has_mul_inv(k_mat,26):
        print("Error(e_hill): key is not invertible")
        return ''
    
    #Split plaintext into diagraphs
    nonbase_pos = utilities.get_positions(plaintext.lower(), utilities.clean_text(utilities.get_base('all'), alphabet) + " " +  '\n')

    cleaned_text = utilities.clean_text(plaintext.lower(), utilities.clean_text(utilities.get_base('all'), alphabet) +" " +  '\n') 
    
    ndx = 0
    diagraphs = []
    while ndx < len(cleaned_text) - 1:
        diagraphs.append([cleaned_text[ndx], cleaned_text[ndx + 1]])
        ndx += 2
        
    #pad if nessesary
    if len(cleaned_text) % 2 == 1:
        diagraphs.append([cleaned_text[len(cleaned_text) - 1],utilities.PAD])
        
    #convert diagraphs into index positions
    i = 0
    j = 0
    for dia in diagraphs:
        
        for c in dia:
            diagraphs[i][j] = utilities._get_elem_ndx_first(alphabet, c)
            j += 1
        j = 0
        i += 1
    i = 0
    j = 0    
    #print(diagraphs)
    # multiply each diagraph with key matrix
    for dia in diagraphs:
        #print(str(k_mat) + " * " + str(dia))
        
        diagraphs[i] = [(k_mat[0][0] * dia[0] + k_mat[0][1] * dia[1]) % 26, (k_mat[1][0] * dia[0] + k_mat[1][1] * dia[1]) % 26]
        i += 1
    i = 0        
    #print(diagraphs)
    
    #Convert back to characters
    for dia in diagraphs:
        
        for c in dia:
            diagraphs[i][j] = alphabet[diagraphs[i][j]]
            j += 1
        j = 0
        i += 1
    j = 0
    i = 0
    
    #Convert to string in ciphertext (with uppercase)
    for dia in diagraphs:
        for c in dia:
            ciphertext += c.upper()
    #Replace non-base characters
    
    ciphertext = utilities.insert_positions(ciphertext, nonbase_pos)
    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str)
# Return:       plaintext (str)
# Description:  Decryption using Hill Cipher, 2x2 (mod 26)
#               key is a string consisting of 4 characters
#                   if key is too short, make it a running key
#                   if key is too long, use first 4 characters
#               Decrypts only alphabet characters
#               Deals with ciphertext as upper case, 
#               and produces lower case plaintext
#               If necessary remove paddingpadding
# Errors:       if key is is invalid:
#                   print error msg and return empty string
# Asserts:      ciphertext is a non-empty string
#-----------------------------------------------------------
def d_hill(ciphertext,key):
    plaintext = ""
    
         
    k_word = key.upper()
    alphabet = utilities.get_base('upper')
    
    if len(k_word) > 4:
        k_word = k_word[:4]
           
    elif len(k_word) < 4:
        
        i = 0
        while len(k_word) < 4:
            #if not alphabet[i] in k_word: to not repeat letters
            k_word = k_word + alphabet[i]
            i += 1
    #print(k_word)        
            
    k_mat = [[0,0],[0,0]]
    
    #insert
    k_mat[0][0] = k_word[0]
    k_mat[0][1] = k_word[1]
    k_mat[1][0] = k_word[2]
    k_mat[1][1] = k_word[3]
    
    #replace with ndx in alphabet
    k_mat[0][0] = utilities._get_elem_ndx_first(alphabet, k_mat[0][0])
    k_mat[0][1] = utilities._get_elem_ndx_first(alphabet, k_mat[0][1])
    k_mat[1][0] = utilities._get_elem_ndx_first(alphabet, k_mat[1][0])
    k_mat[1][1] = utilities._get_elem_ndx_first(alphabet, k_mat[1][1])
    #print(k_mat)
    #Check if its invertible
    if not mod.has_mul_inv(k_mat,26):
        print("Error(e_hill): key is not invertible")
        return ''
    #print("AFTER:::: " + str(k_mat))
    #Split plaintext into diagraphs
    nonbase_pos = utilities.get_positions(ciphertext.upper(), utilities.clean_text(utilities.get_base('all'), alphabet) + " " +  '\n')

    cleaned_text = utilities.clean_text(ciphertext.upper(), utilities.clean_text(utilities.get_base('all'), alphabet) + " " +  '\n') 
    #print(cleaned_text)
    ndx = 0
    diagraphs = []
    while ndx < len(cleaned_text) - 1:
        diagraphs.append([cleaned_text[ndx], cleaned_text[ndx + 1]])
        ndx += 2
    #print(diagraphs)    
    #pad if nessesary
    #if len(cleaned_text) % 2 == 1:
        #diagraphs.append([cleaned_text[len(cleaned_text) - 1],utilities.PAD])
        
    #convert diagraphs into index positions
    i = 0
    j = 0
    for dia in diagraphs:
        for c in dia:
            diagraphs[i][j] = utilities._get_elem_ndx_first(alphabet, c)
            j += 1
        j = 0
        i += 1
    i = 0
    j = 0    

    
    #GET INVERSE OF KEY
    ki_mat = matrix.inverse(k_mat, 26)

    #ki_mat = k_mat
    # multiply each diagraph with key matrix
    
    for dia in diagraphs:
        #print(str(k_mat) + " * " + str(dia))
        #print(ki_mat)
        if ki_mat != [] and not isinstance(ki_mat,str):
            diagraphs[i] = [(ki_mat[0][0] * dia[0] + ki_mat[0][1] * dia[1]) % 26, (ki_mat[1][0] * dia[0] + ki_mat[1][1] * dia[1]) % 26]
        else:
            diagraphs[i] = [(k_mat[0][0] * dia[0] + k_mat[0][1] * dia[1]) % 26, (k_mat[1][0] * dia[0] + k_mat[1][1] * dia[1]) % 26]
        
        i += 1
    i = 0        
    #print(diagraphs)
    
    #Convert back to characters
    for dia in diagraphs:
        
        for c in dia:
            diagraphs[i][j] = alphabet[diagraphs[i][j]]
            j += 1
        j = 0
        i += 1
    j = 0
    i = 0
    
    #Convert to string in ciphertext (with uppercase)
    for dia in diagraphs:
        for c in dia:
            plaintext += c.lower()
            
    #Remove any padding
    if len(plaintext) != 0:
        while plaintext[len(plaintext) - 1] == utilities.PAD:
            plaintext = plaintext[:len(plaintext) - 1]
            if len(plaintext) == 0:
                exit
            
    #Replace non-base characters
    plaintext = utilities.insert_positions(plaintext, nonbase_pos)
        
    return plaintext
#-----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (tuple): (base(str), k(int))
# Return:       ciphertext (str)
# Description:  Encryption using Decimation Cipher
#               Encrypts only characters defined in the base
#               Case of characters should be preserved (whenever possible)
# Asserts:      plaintext is a string
# Errors:       if invalid key, e.g. has no multiplicative inverse -->
#                   print error msg and return empty string
#-----------------------------------------------------------
def e_decimation(plaintext,key):
    
    if not isinstance(key[0],str) or not isinstance(key[1], int):
        print("Error(e_decimation): invalid key")
        return ""
    #This is a simple substitution cipher
    #Each letter in plaintext is replaced by its position in alphabet (a = 1, b = 2, z = 25). Position values are multiplied by encryption value (k(int)) in mod 26
 
    # key must be an odd int (k) between 3 and base string length(except half of base string length). k must not have a common prime divisor with base string length.
    if (key[1] % 2 == 0 and len(key[0]) > key[1]) or key[1] == 1 or key[1] == 2:
        print("Error(e_decimation): invalid key")
        return ""
    ciphertext = ''
    
    nonbase_pos = utilities.get_positions(plaintext.lower(), utilities.clean_text(utilities.get_base('all'), key[0]) + " " + '\n')

    cleaned_text = utilities.clean_text(plaintext, utilities.clean_text(utilities.get_base('all'), key[0] + key[0].upper()) + " " + '\n')
    base = key[0]
    #Get positions
    pt_positions = []
    for c in cleaned_text:
        if c.isupper():
            pt_positions.append((utilities._get_elem_ndx_first(base.upper(), c),c))
        else:       
            pt_positions.append((utilities._get_elem_ndx_first(base, c),c))
        
    ct_positions = []
    
    for i in pt_positions:
        ct_positions.append(((i[0] * key[1]) % len(base),i[1]))
        
    #print(cleaned_text)
    #print(pt_positions)
    #print(ct_positions)
    
    for c in ct_positions:
        if c[1].isupper():
            ciphertext += base[c[0]].upper()
        else:
            ciphertext += base[c[0]]
    
  
    ciphertext = utilities.insert_positions(ciphertext, nonbase_pos)    
    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (tuple): (base(str), k(int))
# Return:       plaintext (str)
# Description:  Decryption using Decimation Cipher
#               Decrypts only characters defined in the base
#               Case of characters should be preserved (whenever possible)
# Asserts:      ciphertext is a string
# Errors:       if invalid key, e.g. has no multiplicative inverse -->
#                   print error msg and return empty string
#-----------------------------------------------------------
def d_decimation(ciphertext,key):
    
    if not isinstance(key[0],str) or not isinstance(key[1], int):
        print("Error(d_decimation): invalid key")
        return ""
    #This is a simple substitution cipher
    #Each letter in plaintext is replaced by its position in alphabet (a = 1, b = 2, z = 25). Position values are multiplied by encryption value (k(int)) in mod 26
 
    # key must be an odd int (k) between 3 and base string length(except half of base string length). k must not have a common prime divisor with base string length.
    if (key[1] % 2 == 0 and len(key[0]) > key[1]) or key[1] == 1 or key[1] == 2:
        print("Error(d_decimation): invalid key")
        return ""    
    plaintext = ''
    
    nonbase_pos = utilities.get_positions(ciphertext.lower(), utilities.clean_text(utilities.get_base('all'), key[0]) + " " + '\n')

    cleaned_text = utilities.clean_text(ciphertext, utilities.clean_text(utilities.get_base('all'), key[0] + key[0].upper()) + " " + '\n')
    base = key[0]
    
    #Get positions
    pt_positions = []
    
    for c in cleaned_text:
        if c.isupper():
            pt_positions.append((utilities._get_elem_ndx_first(base.upper(), c),c))
        else:       
            pt_positions.append((utilities._get_elem_ndx_first(base, c),c))
        
    ct_positions = []
    
    for i in pt_positions:
        m = 0
        mult = i[0]
        while mult % key[1] != 0 and mult < len(base) * 100: #arbitatry num to stop infinite looping if it cannot find
            mult += len(base)
            
            #m += len(base)
        ct_positions.append((math.floor(mult / key[1]),i[1]))
        #ct_positions.append(((i[0] / key[1]) % len(base),i[1]))
        
    #print(cleaned_text)
    #print(pt_positions)
    #print(ct_positions)
    
    
    for c in ct_positions:
        if c[0] > len(base):
            return ""
        if c[1].isupper():
            if c[0] < len(base):
                plaintext += base[c[0]].upper()
            else:
                return ""
        else:
            if c[0] < len(base):
                plaintext += base[c[0]]
            else:
                return ""
    
    
    plaintext = utilities.insert_positions(plaintext, nonbase_pos) 
    return plaintext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
# Return:       key (tuple) (base,k)
#               plaintext (str)
#               counter (int): number of attempted keys
# Description:  Cryptanalysis of Decimation Cipher
#               Assumes subset of get_base('lower) + get_base('nonalpha')
#                 starting at 'a' and holding consecutive characters
#               If it fails, return: '','',0
# Asserts:      ciphertext is a non-empty string
#-----------------------------------------------------------
def cryptanalysis_decimation(ciphertext):
    
    #major_base = utilities.get_base('lower') + utilities.get_base('nonalpha')
    major_base = utilities.get_base('lower')
    # I imagine at first we can narrow down all possible keys to the domain of integers that are Odd, 3 or greater,
    key = ('', 0)
    attempt_key = ['', 0]

    at_key = 3
    plaintext = ''
    attempt_text = ''
    counter = 0
        
    #nonbase_pos = utilities.get_positions(ciphertext.lower(), utilities.clean_text(utilities.get_base('all'), utilities.get_base('lower') + utilities.get_base('nonalpha')) + " " + '\n')

    #cleaned_text = utilities.clean_text(ciphertext, utilities.clean_text(utilities.get_base('all'), utilities.get_base('lower') + utilities.get_base('upper') + utilities.get_base('nonalpha')) + " " + '\n')
    nonbase_pos = utilities.get_positions(ciphertext.lower(), utilities.clean_text(utilities.get_base('all'), utilities.get_base('lower')) + " " + '\n')

    cleaned_text = utilities.clean_text(ciphertext, utilities.clean_text(utilities.get_base('all'), utilities.get_base('lower') + utilities.get_base('upper')) + " " + '\n')

    
    dict = utilities.load_dictionary('engmix.txt')
    
    for i in range(3,len(major_base)):
        #generate base string
        print("NEXT BASE")
        mb = major_base[:i]
        attempt_key = [mb, at_key]

        while at_key < 78:
            #print(at_key)
            #if mod.is_relatively_prime(len(mb), at_key):
            if 1:
                #Attempt all possible keys in base string
                attempt_key[1] = at_key
                attempt_text = d_decimation(ciphertext,(attempt_key[0], attempt_key[1]))
   
                if attempt_text != "":
                    print(attempt_text)
                    if utilities.is_plaintext(attempt_text, dict, 0.5):

                        key = (attempt_key[0],attempt_key[1])
                        plaintext = attempt_text
                        return key, plaintext, counter
                at_key += 2   
                counter += 1
        #Reset for next base string (reset key, increment base
        at_key = 3

            
    return key,plaintext,counter
def test():
    ct = "IOT BJK NBI"
    print(cryptanalysis_eatbash(ct))
    print("Done")

test()