"""
-----------------------------
CP460 (Fall 2020)
Name: Matthew Chiarelli
ID:   150798950
Final Exam
-----------------------------
"""
#-----------------------------------------------------------
# Parameters:   mod (int)
# Return:       r_list (list)
# Description:  Returns list of numbers in the given mod
#               which are residues of all other numbers
# Example:      residue_list(5) --> [0,1,2,3,4]
# Errors:       If mode is not a positive integer:
#                   return 'Error(residue_list): Invalid mod'
#-----------------------------------------------------------
def residue_list(mod):
    if not isinstance(mod, int):
        return 'Error(residue_list): Invalid mod'
    if mod < 1:
        return 'Error(residue_list): Invalid mod' 
    r_list = []
   
    for i in range(mod):
        r_list.append(i)
   
    return r_list

#-----------------------------------------------------------
# Parameters:   num (int)
#               mod (int)
# Return:       residue (int)
# Description:  Returns the smallest positive integer that is
#               congruent to num mod m
# Example:      residue 16 mod 5 --> 1
# Errors:       mod has to be positive integer
#                   return 'Error(residue): Invalid mod'
#               num should be integer
#                   return 'Error(residue): Invalid num'
#-----------------------------------------------------------
def residue(num,mod):
    if not isinstance(num, int):
        return 'Error(residue): Invalid num'
    if mod < 1:
        return 'Error(residue): Invalid mod' 
   
    residue = num % mod
    
    return residue

#-----------------------------------------------------------
# Parameters:   a (int)
#               b (int)
#               m (int)
# Return:       True/False
# Description:  Returns True if a is congruent b mod m
#               return False otherwise
# Example:      is_congruent(22,33,11) --> True
#               is_congruent(7,9,3) --> False
# Errors:       if mod is not a positive integer
#                   return 'Error(is_congruent): Invalid mod'
#               a and b should be integer
#                   return 'Error(is_congruent): Invalid input num'
#-----------------------------------------------------------
def is_congruent(a,b,m):
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error(is_congruent): Invalid input num'
    if m < 1:
        return 'Error(is_congruent): Invalid mod'
   
    if residue(a,m) == residue(b,m):
        return True
    
    
    return False

#-----------------------------------------------------------
# Parameters:   a (int)
#               b (int)
#               m (int)
# Return:       result (integer)
# Description:  Returns (a + b) mod m
#               result is an integer in residue_list mod m
# Example:      11 + 3 mod 5 = 4
# Errors:       If a or b is not an integer
#                   return 'Error(add): Invalid input num'
#               m should be positive integer
#                   return 'Error(add): Invalid mod'
#-----------------------------------------------------------
def add(a,b,m):
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error(add): Invalid input num'
    if m < 1:
        return 'Error(add): Invalid mod'
    
    result =  residue(a + b,m)
    return result

#-----------------------------------------------------------
# Parameters:   a (int)
#               b (int)
#               m (int)
# Return:       result (int)
# Description:  Returns (a - b) mod m
#               result is an integer in residue_list mod m
# Example:      sub(11,2,5) = 4
# Errors:       a and b should be integers
#                   return 'Error(sub): Invalid input num'
#               m should be positive integer
#                   return 'Error(sub): Invalid mod'
#-----------------------------------------------------------
def sub(a,b,m):
    if not isinstance(a, int) or not isinstance(b, int):
        return 'Error(sub): Invalid input num'
    if m < 1:
        return 'Error(sub): Invalid mod'
    
    result =  residue(a - b,m)
    return result

#-----------------------------------------------------------
# Parameters:   a (int)
#               m (int)
# Return:       result (int)
# Description:  Returns additive inverse of a mod m
#               result is an integer in residue_list mod m
# Example:      additive inverse of 3 mod 5 is 2
# Errors:       if a or b is not an integer
#                   return 'Error(add_inv): Invalid input num'
#               if m is not a positive integer
#                   return 'Error(add_inv): Invalid mod'
#-----------------------------------------------------------
def add_inv(a,m):
    if not isinstance(a, int):
        return 'Error(add_inv): Invalid input num'
    if m < 1:
        return 'Error(add_inv): Invalid mod'
   
    r_list = residue_list(m)
    for i in r_list:
        if residue(a + i,m) == 0:
            result = i
            exit
    return result

#-----------------------------------------------------------
# Parameters:   m (int)
# Return:       table (2D List)
# Description:  Returns addition table mod m
#               element [r][c] represent r+c mod m
# Example:      add_table(2) --> [[0,1],[1,0]]
# Errors:       if m is not a positive integer
#                   return 'Error(add_table): Invalid mod'
#-----------------------------------------------------------
def add_table(m):
    if m < 1:
        return 'Error(add_table): Invalid mod'
    
    table = []
    
    for row in range(m):
        table.append([])
        for col in range(m):
            table[row].append(residue(row + col,m))
            
    return table

#-----------------------------------------------------------
# Parameters:   m (int)
# Return:       table (2D List)
# Description:  Returns subtraction table mod m
#               element [r][c] represent r-c mod m
# Example:      sub_table(3) --> [[[0,2,1],[1,0,2],[2,1,0]]
# Errors:       if m is not a positive integer
#                   return 'Error(sub_table): Invalid mod'
#-----------------------------------------------------------
def sub_table(m):
    if not isinstance(m,int):
        return 'Error(sub_table): Invalid mod'
    
    if m < 1:
        return 'Error(sub_table): Invalid mod'
    
    table = []
    
    for row in range(m):
        table.append([])
        for col in range(m):
            table[row].append(residue(row - col,m))
            
    return table

#-----------------------------------------------------------
# Parameters:   m (int)
# Return:       table (2D List)
# Description:  Returns additive Inverse table mode m
#               Top row is num, bottom row is additive inverse
# Example:      add_inv_table(5) --> [[0,1,2,3,4],[0,4,3,2,1]]
# Errors:       if m is not a positive integer
#                   return 'Error(add_inv_table): Invalid mod'
#-----------------------------------------------------------
def add_inv_table(m):
    if m < 1 or not isinstance(m,int):
        return 'Error(add_inv_table): Invalid mod'
    
    table = []
    
    table.append(residue_list(m))
    
    inverse = []
    for i in table[0]:
        inverse.append(add_inv(i, m))
        
    table.append(inverse)
            
    return table

#-----------------------------------------------------------
# Parameters:   a (int)
#               b (int)
#               m (int)
# Return:       result (int)
# Description:  Returns (a * b) mod m
#               result is an integer in residue_list mod m
# Example:      mul(11,2,5) = 2
# Errors:       a and b should be integers
#                   return 'Error(mul): Invalid input num'
#               m should be positive integer
#                   return 'Error(mul): Invalid mod'
#-----------------------------------------------------------
def mul(a,b,m):
    if not isinstance(a,int) or not isinstance(b,int):
        return 'Error(mul): Invalid input num'
    
    if m < 1:
        return 'Error(mul): Invalid mod'
    
    
    result = residue(a * b, m)
    
    return result

#-----------------------------------------------------------
# Parameters:   m (int)
# Return:       table (2D List)
# Description:  Returns multiplication table mod m
#               element [r][c] represent r*c mod m
# Example:      mul table for mod 4 -->
#                       [0, 0, 0, 0]
#                       [0, 1, 2, 3]
#                       [0, 2, 0, 2]
#                       [0, 3, 2, 1]
# Errors:       if m is not a positive integer
#                   return 'Error(mul_table): Invalid mod'
#-----------------------------------------------------------
def mul_table(m):
    if m < 1 or not isinstance(m,int):
        return 'Error(mul_table): Invalid mod'
    
    
    table = []
    
    for row in range(m):
        table.append([])
        for col in range(m):
            table[row].append(residue(row * col,m))
            
    return table

#-----------------------------------------------------------
# Parameters:   n (an integer)
# Return:       True/False
# Description:  Returns True if n is a prime
#               False otherwise
#               (Note: Search online for an efficient implementation)
# Errors        None
#-----------------------------------------------------------
def is_prime(n):
    if not isinstance(n,int):
        return False
    
    if n <= 1:
        return False
    if n <= 3:
        return True
    if residue(n,2) == 0 or residue(n,3) == 0:
        return False
    i = 5
    while(i * i <= n) :
        if (residue(n,i) == 0 or residue(n,(i + 2)) == 0) :
            return False
        i = i + 6
    
    return True

#-----------------------------------------------------------
# Parameters:   a (int)
#               b (int)
# Return:       gcd of a and b (int)
# Description:  Returns greatest common divider using standard
#               Euclidean Algorithm
#               Implementation can be recursive or iterative
# Errors:       If a or b is not a non-zero integer: 
#                   return 'Error(gcd): Invalid input num'
#-----------------------------------------------------------
def gcd(a,b):
    if not isinstance(a,int) or not isinstance(b,int):
        return 'Error(gcd): Invalid input num'
    if a == 0 or b == 0:
        return 'Error(gcd): Invalid input num'
    
    a1 = a
    b1 = b
    if a < 1:
        a1 = a * -1
    if b < 1:
        b1 = b * -1
    #print(a)
    #print(b)
    d1 = calc_divisors(a1)
    d2 = calc_divisors(b1)
    divisors = []
    divisors.append(d1)
    divisors.append(d2)
    divisors = get_common_numbers(divisors)
    result = get_largest(divisors)
    if result == None:
        #print("No common divisor.")
        return 1
    return result
#returns all divsors of a given number in an array
def calc_divisors(num):
    cd = []
    for i in range(2,num):
        if num % i == 0:
            cd.append(i)
    cd.append(num)
    return cd 

"""
----------------------------------------------------
Parameters:   list (list2d): list of integers
              
Return:       common_nums (list)
Description:  removes all numbers which do not show up in all lists within the 2d list
---------------------------------------------------
"""
def get_common_numbers(list):
    common_nums = []
    #used_vals = []
    for i in list:
        for j in i:
            common_nums.append(j)
 
    #print(common_nums)            
    for i in common_nums:
        if common_nums.count(i) != len(list):
            common_nums = remove_all(common_nums,i)        
    #print(common_nums)        
                
    return common_nums
"""
----------------------------------------------------
Parameters:   list (list)
              elem (int): element to remove
Return:       new_list (list)
Description:  removes all occurances of the given element from the list
---------------------------------------------------
"""
def remove_all(list,elem):
    new_list = list.copy()
    
    for i in new_list:
        if i == elem:
            new_list.remove(i)
    return new_list

"""
----------------------------------------------------
Parameters:   list (list): list of ints
              
Return:       largest (int)
Description:  searches and returns the largest value in a given list
---------------------------------------------------
"""
def get_largest(list):

    if len(list) == 0:
        #print("Gave me an empty list")
        return None
    
    largest = list[0]
    for i in list:
        if i > largest:
            largest = i
    return largest

#-----------------------------------------------------------
# Parameters:   a (int)
#               b (int)
# Return:       True/False
# Description:  Checks if two numbers are relatively prime
#               which is when gcd(a,b) equals 1
# Errors:       if a or b is not an integer
#                   return 'Error(is_relatively_prime): Invalid input num'
#-----------------------------------------------------------
def is_relatively_prime(a,b):
    if not isinstance(a,int) or not isinstance(b,int):
        return 'Error(is_relatively_prime): Invalid input num'
    
    if gcd(a,b) == 1:
        return True
    
    return False

#-----------------------------------------------------------
# Parameters:   a (an integer)
#               m (a positive integer)
# Return:       True/False
# Description:  Checks if number 'a' has a multiplicative inverse
#               in mod m. Returns True if such number exist
#               Returns False otherwise
# Errors:       if a is not an integer
#                   return 'Error(has_mul_inv)" Invalid input num'
#               if m is not a positive integer
#                   return 'Error(has_mul_inv): Invalid mod'
#-----------------------------------------------------------
def has_mul_inv(a,m):
    if not isinstance(a,int):
        return 'Error(has_mul_inv)" Invalid input num'
    
    if not isinstance(m,int) or m < 1:
        return 'Error(has_mul_inv): Invalid mod'
    
    r_list = residue_list(m)
    for i in r_list:
        
        if residue(a * i,m) == 1:
            return True
    
    return False

#-----------------------------------------------------------
# Parameters:   a (an integer)
#               b (an integer)
# Return:       result (list): [gcd(a,b) , s , t]
# Description:  Uses Extended Euclidean Algorithm to find
#               gcd of (a,b) and 's' and 't' such that
#               as + bt = gcd(a,b) , i.e. Bezout's Identity
# Errors:       if a or b equals to 0:
#                   return 'Error(eea): Invalid input num'
#-----------------------------------------------------------
def eea(a,b):
    if not isinstance(a,int) or not isinstance(b,int):
        return 'Error(eea): Invalid input num'
    
    if a == 0 or b == 0:
        return 'Error(eea): Invalid input num'
    #print("lol")
    result = []
    g = 0
    #print(a)
    #print(b)
    g = gcd(a,b)
    result.append(g)
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r//r # In Python, // operator performs integer or floored division

        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t
    result.append(old_s)
    result.append(old_t)
    return result


    
#-----------------------------------------------------------
# Parameters:   a (an integer)
#               m (positive integer)
# Return:       mul_v (int or 'NA')
# Description:  Computes multiplicative inverse of 'a' mod m
#               If such number does not exist, the function
#               return 'NA'
# Errors:       if 'a' is not an integer:
#                   return 'Error(mul_inv)" Invalid input num'
#               if m is not a positive integer
#                   return 'Error(mul_inv): Invalid mod
#-----------------------------------------------------------
def mul_inv(a,m):
    
    if not isinstance(a, int):
        return 'Error(mul_inv)" Invalid input num'
    
     
    if not isinstance(m, int):
        return 'Error(mul_inv): Invalid mod'
    
    if m < 1 or not isinstance(m,int):
        return 'Error(mul_inv): Invalid mod'
    mul_v = 'NA'
    
   
    r_list = residue_list(m)
    for i in r_list:
        if residue(a * i,m) == 1:
            mul_v = i
            exit    
    
    
    return mul_v

#-----------------------------------------------------------
# Parameters:   m (int)
# Return:       table (2D list)
# Description:  Returns multiplicative Inverse table mode m
#               Top row is num, bottom row is multiplicative inverse
# Example:      Multiplicative Inverse table mod 5 -->
#                   [[0,1,2,3,4],['NA',1,3,2,4]]
# Errors:       if m is not a positive integer
#                   return 'Error(mul_inv_table): Invalid mod'
#-----------------------------------------------------------
def mul_inv_table(m):
    if m < 1 or not isinstance(m,int):
        return 'Error(mul_inv_table): Invalid mod'
    
    table = []
    table.append(residue_list(m))
    inverse = []
    
    for i in table[0]:
        inverse.append(mul_inv(i,m))
        
    table.append(inverse)
    return table