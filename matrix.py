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


#-----------------------------------------------------------
# Parameters:   A (any input)
# Return:       True/False
# Description:  checks if the given input is a valid vector
#               A valid vector is a list in which all elements are integers
#               An empty list is a valid vector
# Errors:       None
#-----------------------------------------------------------
def is_vector(A):
    
    if not isinstance(A,list):
        return False

    for elem in A:
        #print("yuh: " + str(elem))
        if not isinstance(elem, int):
            return False
    
    return True

#-----------------------------------------------------------
# Parameters:   A (any input)
# Return:       True/False
# Description:  checks if the given input is a valid matrix
#               A matrix is a list in which all elements are valid vectors of equal size
#               Any valid vector is also a valid matrix
# Errors:       None
#-----------------------------------------------------------
def is_matrix(A):
    if not isinstance(A,list):
        #print("Nani")
        return False


    if A == []:
        return True
    if is_vector(A[0]): #Its a 2d list
        size = len(A[0])
        for row in A:
            if not is_vector(row) or size != len(row):
                return False
    else: #its a 1d list
        return is_vector(A)
        
        
    return True
'''
    if len(A) > 0:
        size = len(A)
        if is_vector(A[0]):        
            for elem in A:
                #print(elem)
                if not is_vector(elem) or len(elem) != size:
                    return False
        else:
            if isinstance(A[0], int):
                return True
            else:
                return False
    else:
        if is_vector(A):
            return True
        else:
            return False
''' 

#-----------------------------------------------------------
# Parameters:   A (a matrix)
# Return:       None
# Description:  Prints a given matrix, each row on a separate line
# Errors:       If A not a matrix --> print 'Error (print_matrix): Invalid input'
#-----------------------------------------------------------
def print_matrix(A):
    if not is_matrix(A) or not isinstance(A,list):
        print('Error (print_matrix): Invalid input')
        return
    
    if A == []:
        print("[]")
        return
    
    if is_vector(A[0]):
        for row in A:
            print(row)
    else:
        print(A) 
 
    return

#-----------------------------------------------------------
# Parameters:   A (a matrix)
# Return:       number of rows (int)
# Description:  Returns number of rows in a given matrix
# Examples:     [5,3,2] --> 1
#               [] --> 0
#               [[1,2],[3,4],[5,6]] --> 3
# Errors:       If A not a matrix -->
#                   return 'Error(get_r): invalid input'
#-----------------------------------------------------------
def get_r(A):
    if not is_matrix(A) or not isinstance(A,list):
        return 'Error(get_r): invalid input'
    
    if A == []:
        return 0
    else:
        if is_vector(A[0]):
            return len(A)
        else:
            return 1
        
    return len(A)

#-----------------------------------------------------------
# Parameters:   A (a matrix)
# Return:       number of columns (int)
# Description:  Returns number of columns in a given matrix
# Examples:     [5,3,2] --> 3
#               [] --> 0
#               [[1,2],[3,4],[5,6]] --> 2
# Errors:       If A not a matrix -->
#                   return 'Error(get_c): invalid input'
#-----------------------------------------------------------
def get_c(A):
    if not is_matrix(A) or not isinstance(A,list):
        return 'Error(get_c): invalid input'

    #print(A)
    if A == []:
        return 0
    else:
        if is_vector(A[0]):
            return len(A[0])
        else:
            return len(A)
        
        
    return 0

#-----------------------------------------------------------
# Parameters:   A (a matrix)
# Return:       [number of rows (int), number of columns(int)]
# Description:  Returns number size of matrix [rxc]
# Examples:     [5,3,2] --> [1,3]
#               [] --> [0,0]
#               [[1,2],[3,4],[5,6]] --> [3,2]
# Errors:       If A not a matrix -->
#                   return 'Error(get_size): invalid input'
#-----------------------------------------------------------
def get_size(A):
    if not isinstance(A,list) or not is_matrix(A):
        return 'Error(get_size): invalid input'
    
    r = get_r(A)        
    c = get_c(A)        
    return [r, c]

#-----------------------------------------------------------
# Parameters:   A (any input)
# Return:       True/False
# Description:  Checks if given input is a valid square matrix
# Examples:     [] --> True
#               [10] --> True
#               [[1,2],[3,4]] --> True
#               [[1,2],[3,4],[5,6]] --> False
# Errors:       None
#-----------------------------------------------------------
def is_square(A):
    if not is_matrix(A) or not isinstance(A,list):
        print('Error(is_square): invalid input')
        
    dimen = get_size(A)
    if dimen[0] == dimen[1]:
        return True
    
    return False

#-----------------------------------------------------------
# Parameters:   A (a matrix)
#               i (row number)
# Return:       row (list)
# Description:  Returns the ith row of given matrix
# Examples:     ([],0) --> Error
#               ([10],0) --> [10]
#               ([[1,2],[3,4]],0) --> [1,2]
# Errors:       If given matrix is empty or not a valid matrix -->
#                   return 'Error(get_row): invalid input matrix'
#               If i is outside the range [0,#rows -1] -->
#                   return 'Error(get_row): invalid row number'
#-----------------------------------------------------------
def get_row(A,i):
    if not is_matrix(A) or not isinstance(A,list):
        return 'Error(get_row): invalid input matrix'
    
    if A == []:
        return 'Error(get_row): invalid input matrix'
    
    if i >= get_size(A)[0]:
        return 'Error(get_row): invalid row number'
    
    row = []
    if len(A) == 1:
        row.append(A[0])
        return row
    #print(A)
    #print(get_size(A)[0])
    #print("i: " + str(i))
    if isinstance(A[0],list):    
        row = A[i]
    else:
        for num in A:
            row.append(A[num])
    
    
    
    return row

#-----------------------------------------------------------
# Parameters:   A (a matrix)
#               j (column number)
# Return:       column (list)
# Description:  Returns the jth column of given matrix
# Examples:     ([],0) --> Error
#               ([10],0) --> [10]
#               ([[1], [2]],0) --> [[1], [2]]
#               ([[1,2],[3,4]],1) --> [2,4]
# Errors:       If given matrix is empty or not a valid matrix -->
#                   return 'Error (get_column): invalid input matrix'
#               If i is outside the range [0,#rows -1] -->
#                   return 'Error(get_column): invalid column number'
#-----------------------------------------------------------
def get_column(A,j, inner_list=True):
    if not is_matrix(A) or not isinstance(A,list):
        return 'Error(get_column): invalid input matrix'
    
    if A == []:
        return 'Error(get_column): invalid input matrix'
    
    if j >= get_size(A)[1]:
        return 'Error(get_column): invalid column number'
    column = []
    #print(A)
    #print(get_size(A)[1])
    #print("j: " + str(j))
    if len(A) == 1:
        column.append(A[0])
        return column
    
    if inner_list: 
        for c in range(get_size(A)[0]):
            column.append([A[c][j]])
    else:
        for c in range(get_r(A)):
            column.append(A[c][j])
            
    return column

#-----------------------------------------------------------
# Parameters:   A (a matrix)
#               i (row number)
#               j (column number)
# Return:       element
# Description:  Returns element (i,j) of the given matrix
# Errors:       If given matrix is empty or not a valid matrix -->
#                   return 'Error(get_element): invalid input matrix'
#               If i or j is outside matrix range -->
#                   return 'Error(get_element): invalid element position'
#-----------------------------------------------------------
def get_element(A,i,j):
    if not is_matrix(A) or A == []:
        return 'Error(get_element): invalid input matrix'
    
    if i >= get_size(A)[0] or j >= get_size(A)[1]:
        return 'Error(get_element): invalid element position'
    
    
    return A[i][j]

#-----------------------------------------------------------
# Parameters:   r: #rows (int)
#               c: #columns (int)
#               num (int)
# Return:       matrix
# Description:  Create an empty matrix of size r x c
#               All elements are initialized to integer num
# Error:        r and c should be positive integers
#               (except the following which is valid 0x0 --> [])
#                   return 'Error(new_matrix): invalid size'
#               pad should be an integer
#                   return 'Error(new_matrix): invalid num'
#-----------------------------------------------------------
def new_matrix(r,c,num,inner_list=True):
    if r == 0 and c == 0:
        return []
    
    if not isinstance(r,int) or not isinstance(c,int) or r <= 0 or c <= 0:
        return 'Error(new_matrix): invalid size'
    
    if not isinstance(num, int):
        return 'Error(new_matrix): invalid num'
    if inner_list == False:
        nm=[]
        for i in range(c):
            nm.append(num)
        return nm
    else:
        return [[num] * c for i in range(r)] 
    
    

#-----------------------------------------------------------
# Parameters:   size (int)
# Return:       square matrix (identity matrix)
# Description:  returns the identity matrix of size: [size x size]
# Examples:     0 --> Error
#               1 --> [1]
#               2 --> [[1,0],[0,1]]
# Errors        size should be a positive integer
#                   return 'Error(get_I): invalid size'
#-----------------------------------------------------------
def get_I(size):
    if not isinstance(size,int) or size <= 0:
        return 'Error(get_I): invalid size'
    
    if size == 1:
        return [1]
    
    sm = new_matrix(size,size,0)
    diag = 0
    for i in range(size):
        sm[i][diag] = 1
        diag += 1
    
    return sm

#-----------------------------------------------------------
# Parameters:   A (any input)
# Return:       True/False
# Description:  Checks if given input is a valid identity matrix
#-----------------------------------------------------------
def is_identity(A):
    if A == get_I(len(A)):
        return True
    
    return False

#-----------------------------------------------------------
# Parameters:   c (int)
#               A (matrix)
# Return:       a new matrix which is the result of cA
# Description:  Performs scalar multiplication of constant c with matrix A
# Errors:       if A is empty or not a valid matrix or c is not an integer:
#                   return 'Error(scalar_mul): invalid input'
#-----------------------------------------------------------
def scalar_mul(c,A):
    if not isinstance(c, int) or not is_matrix(A) or A == []:
        return 'Error(scalar_mul): invalid input'
    
    nm = []
    
    for i in range(len(A)):
        row = A[i]
        if isinstance(row,list):
            for j in range(len(row)):
                row[j] *= c
            nm.append(row)
        else:
            nm.append(row * c)    

    return nm

#-----------------------------------------------------------
# Parameters:   A (matrix)
#               B (matrix)
# Return:       a new matrix which is the result of AxB
# Description:  Performs cross multiplication of matrix A and matrix B
# Errors:       if either A or B or both is empty matrix nor not a valid matrix
#                   return 'Error(mul): invalid input'
#               if size mismatch:
#                   return 'Error(mul): size mismatch'
#-----------------------------------------------------------
def mul(A,B):
    if A == [] or B == [] or not is_matrix(A) or not is_matrix(B):
        return 'Error(mul): invalid input'
    if get_c(A) != get_r(B):
        return 'Error(mul): size mismatch'
    
    nm = new_matrix(get_r(A),get_c(B),0)
    
    row = []
    col = []
    #print("MATRIX: " + str(A) + " : "+ str(B) + "col: " + str(get_c(B)))
    for i in range(len(nm)):
        row = get_row(A,i)
        for j in range(len(nm[0])):
            #print("YEET: " + str(B) + " : "+ str(row))
            
            col = get_column(B,j, False)
            #print("YEET: " + str(row) + " : "+ str(col))
            nm[i][j] = dot_product(row,col)
    #print("FIN: " + str(nm))
    
    if isinstance(nm[0],list) and len(nm[0]) == 1: #this is evil and lazy 
        nm = nm[0]
    
    return nm

def dot_product(v1,v2):
    if not isinstance(v1,list) or not isinstance(v2,list):
        return 'Error(dot_product): invalid vectors'
    
    if len(v1) != len(v2):
        return 'Error(dot_product): vectors size mismatch'
    
    result = 0

    for i in range(len(v1)):
        result += v1[i] * v2[i]
        
    return result
#-----------------------------------------------------------
# Parameters:   A (matrix)
#               m (int)
# Return:       A` (matrix)
# Description:  Returns matrix A such that each element is the 
#               residue value in mode m
# Errors:       if A is empty matrix or not a valid matrix
#                   return 'Error(matrix_mod): invalid input'
#               if m is not a positive integer:
#                   return 'Error(matrix_mod): invalid mod'
#-----------------------------------------------------------
def matrix_mod(A,m):
    if not is_matrix(A) or A == []:
        return 'Error(matrix_mod): invalid input'
    if not isinstance(m,int) or m <= 0:
        return 'Error(matrix_mod): invalid mod'
    
    row = A[0]
    nm = new_matrix(get_r(A),get_c(A),0)
    i = 0
    j = 0
    #print(A)
    #print(nm)
    if isinstance(row,list):        
        for r in A:
            
            for c in r:
                nm[i][j] = mod.residue(c, m)
                j += 1
            j = 0
            i += 1
    else:
        nm = new_matrix(get_r(A),get_c(A),0,False)
        #print(nm)
        for elem in A:
            #print(str(elem) + " " + str(m) + "=" + str(mod.residue(elem,m)))
            nm[i] = mod.residue(elem,m)
            i += 1
    
    return nm

#-----------------------------------------------------------
# Parameters:   A (matrix)
# Return:       determinant of matrix A (int)
# Description:  Returns the determinant of a 2x2 matrix
# Errors:       if A is empty matrix nor not a valid square matrix
#                   return 'Error(det): invalid input'
#               if A is square matrix of size other than 2x2
#                   return 'Error(det): Unsupported matrix size'
#-----------------------------------------------------------
def det(A):
    if A == [] or not is_matrix(A):
        return 'Error(det): invalid input'
    if get_r(A) != 2 or get_c(A) != 2:
        return 'Error(det): Unsupported matrix size'
    
    d = (A[0][0] * A[1][1]) - (A[0][1] * A[1][0])
    
    return d

#-----------------------------------------------------------
# Parameters:   A (matrix)
#               m (int)
# Return:       a new matrix which is the inverse of A mode m
# Description:  Returns the inverse of a 2x2 matrix in mode m
# Errors:       if A is empty matrix or not a valid matrix
#                   return 'Error(inverse): invalid input'
#               if A is not a square matrix or a matrix of 2x2 with no inverse:
#                   return 'Error(inverse): matrix is not invertible'
#               if A is a square matrix of size other than 2x2
#                   return 'Error(inverse): Unsupported matrix size'
#               if m is not a positive integer:
#                   return 'Error(inverse): invalid mod'
#-----------------------------------------------------------
def inverse(A,m):
    #print(A)
    if A == [] or not is_matrix(A):
        return 'Error(inverse): invalid input'
    if not is_square(A):
        return 'Error(inverse): matrix is not invertible'
    if get_r(A) != 2 or get_c(A) != 2:
        return 'Error(inverse): Unsupported matrix size'
    if not isinstance(m,int) or m <= 0:
        return 'Error(inverse): invalid mod'
    
    #nm = [i for i in A]
    nm = A[:]
    nmc = [i for i in A]
    d = det(nm) % m #added % m
    #print(d)
    #Does the determinate have a multiplcative inverse?
    if not mod.has_mul_inv(d, m):
        #print('Error(inverse): matrix is not invertible')
        return 'Error(inverse): matrix is not invertible'
    
    sc = mod.mul_inv(d, m)

    #print(sc)
    #nm = A.copy()
    #print("BEFORE ABJ: " + str(nm))
    temp = nm[0][0]
    nm[0][0] = nm[1][1]
    nm[1][1] = temp
    
    #print(str(nm))
    
    nm[0][1] *= -1
    nm[1][0] *= -1
    
    #print("ABJ: " + str(nm))
    inverse_mat = scalar_mul(sc,nm)

    #reduce
    inverse_mat[0][0] = inverse_mat[0][0] % m
    inverse_mat[0][1] = inverse_mat[0][1] % m
    inverse_mat[1][0] = inverse_mat[1][0] % m
    inverse_mat[1][1] = inverse_mat[1][1] % m
    
    return inverse_mat
