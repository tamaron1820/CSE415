def is_multiple_of_5(n):
    """Return True if n is a multiple of 5; False otherwise."""
    if n%5==0:
        return True
    else:
        return False

def last_prime(m):
    """Return the largest prime number p that is less than or equal to m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    prime = 2
    for i in range(2,m+1):
        for j in range(2,i):
            if i%j==0:
                break
        else:
            prime=i
    return prime


def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    qua=(b**2-4*a*c)**(1/2)
    x1=(-b+qua)/(2*a)
    x2=(-b-qua)/(2*a)
    if type(x1) is complex or type(x2) is complex:
        return "complex"
    else:
        return x1,x2

def new_quadratic_function(a, b, c):
    """Create and return a new, anonymous function (for example
    using a lambda expression) that takes one argument x and 
    returns the value of ax^2 + bx + c."""
    return lambda x:a*x**2+b*x+c

def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    Perfect shuffle means splitting a list into two halves and then interleaving
    them. For example, the perfect shuffle of [0, 1, 2, 3, 4, 5, 6, 7] is
    [0, 4, 1, 5, 2, 6, 3, 7]."""
    a = len(even_list)
    half = a//2
    b=even_list[:half]
    c=even_list[half:]
    d=[]
    for i in range(0,half):
        d.append(b[i])
        d.append(c[i])
    return d       


def five_times_list(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 5."""
    length = len(input_list)
    ans_list=[input_list[i]*5 for i in range(length)]
    return ans_list

def triple_vowels(text):
    """Return a new version of text, with all the vowels tripled.
    For example:  "The *BIG BAD* wolf!" => "Theee "BIIIG BAAAD* wooolf!".
    For this exercise assume the vowels are
    the characters A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""
    cha_list= list(text)
    new_list=[]
    vowel_count=0
    for i in range(len(cha_list)):
        if(cha_list[i]=='a'or cha_list[i]=='e'or cha_list[i]=='i'or cha_list[i]=='o'or cha_list[i]=='u'or cha_list[i]=='A'or cha_list[i]=='E'or cha_list[i]=='I'or cha_list[i]=='O'or cha_list[i]=='U'):
            j = i+1
            new_list.insert(2*vowel_count+i,cha_list[i])
            new_list.insert(2*vowel_count+i+1,cha_list[i])
            new_list.insert(2*vowel_count+i+2,cha_list[i])
            vowel_count+=1
        else:
            new_list.insert(2*vowel_count+i,cha_list[i])
    ans_string = "".join(new_list)
    return ans_string
import re
def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', *', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ] { } | : ).
    Convert all the letters to lower-case before the counting."""
    text1 = text.lower()
    tex_list = list(filter(None,re.split("[\\\\ \.,;!?&()\[\]{}\|_><=~\":\\n\`^$ ]",text1)))
    tex_list_length = len(tex_list)
    ans_dictionary={}
    for i in range(len(tex_list)):
        while True:
            if tex_list[i] in ans_dictionary:
                ans_dictionary[tex_list[i]]+=1
                break
            else:
                ans_dictionary[tex_list[i]]=1
                break
        i+=1
    return ans_dictionary

class Polygon:
    """Polygon class."""
    def __init__(self,n_sides,lengths=None,angles=None):
        self.n_sides= n_sides
        self.lengths= lengths
        self.angles= angles 
    
    def is_rectangle(self):
        if self.n_sides!=4:
            return False
        elif self.angles==None:
            return None
        else:
            if self.angles.count(self.angles[0])==4:
                return True
            else:
                return False

    def is_rhombus(self):
        if self.n_sides!=4:
            return False
        if self.angles==None and self.lengths==None:
            return None
        elif self.lengths==None:
            return None
        else:
            if self.lengths.count(self.lengths[0])==4:
                return True
            else:
                return False
    def is_square(self):
        if self.n_sides!=4:
            return False
        elif self.angles==None and self.lengths==None:
            return None
        elif self.angles==None:
            for i in range(len(self.lengths)):
                count = 0
                count = self.lengths.count(self.lengths[i])
                if count==4:
                    return None
                else:
                    continue
            return False
        elif self.lengths==None:
            for i in range(len(self.angles)):
                count = 0
                count = self.angles.count(self.angles[i])
                if count==4:
                    return None
                else:
                    continue
            return False
        else:
            count = 0
            count = self.lengths.count(self.lengths[0])
            if count==4:
                count = 0
                count = self.angles.count(self.angles[0])
                if count==4:
                    return True
                else:
                    return False
            else:
                return False
                    
            
    def is_regular_hexagon(self):
        if self.n_sides!=6:
            return False
        elif self.angles==None and self.lengths==None:
            return False
        else :
            if self.angles==None :
                if self.lengths.count(self.lengths[0])!=6:
                    return False
                return None
            elif self.lengths==None :
                if self.angles.count(self.angles[0])!=6:
                    return False
                return None
            elif self.angles.count(self.angles[0])==6 :
                if self.lengths.count(self.lengths[0])==6:
                    return True
                else:
                    return False       

    def is_isosceles_triangle(self):
        if self.n_sides!=3:
            return False
        elif self.angles==None and self.lengths==None:
            return None
        elif self.angles==None :
            for i in range(len(self.lengths)):
                store=self.lengths[i]
                count = 0
                for j in range(0,len(self.lengths)):
                    if store==self.lengths[j]:
                        count+=1
                    else:
                        continue
                if count>=2:
                    return True
                else:
                    continue
            return False
        elif self.lengths==None:
            for i in range(len(self.angles)):
                store=self.angles[i]
                count = 0
                for j in range(0,len(self.angles)):
                    if store==self.angles[j]:
                        count+=1
                    else:
                        continue
                if count>=2:
                    return True
                else:
                    continue        
            return False
        else:
            for i in range(len(self.angles)):
                store_ang=self.angles[i]
                ang_count = 0
                for j in range(0,len(self.angles)):
                    if store_ang==self.angles[j]:
                        ang_count+=1
                    else:
                        continue
                if ang_count>=2:
                    for k in range(len(self.lengths)):
                        store_len=self.lengths[k]
                        len_count=0
                        for l in range(0,len(self.lengths)):
                            if store_len==self.lengths[l]:
                                return True
                            else:
                                continue
                    return False
                else:
                    continue
            return False
            
    def is_equilateral_triangle(self):
        if self.n_sides!=3:
            return False
        elif self.angles==None and self.lengths==None:
            return None
        elif self.lengths==None:
            count = 0
            count = self.angles.count(self.angles[0])
            if count==3:
                return True
            else:
                return False
        elif self.angles==None :
            count = 0
            count = self.lengths.count(self.lengths[0])
            if count==3:
                return True
            else:
                return False
        else:
            count = 0
            count = self.lengths.count(self.lengths[0])
            if count==3:
                count = 0
                count = self.angles.count(self.angles[0])
                if count==3:
                    return True
                else:
                    return False
            else:
                return False
                
    def is_scalene_triangle(self):
        if self.n_sides!=3:
            return False
        elif self.angles==None and self.lengths==None:
            return None
        elif self.angles==None :
            for i in range(len(self.lengths)):
                store=self.lengths[i]
                count = 0
                for j in range(0,len(self.lengths)):
                    if store==self.lengths[j]:
                        count+=1
                    else:
                        continue
                if count>=2:
                    return False
                else:
                    return True
        elif self.lengths==None:
            for i in range(len(self.angles)):
                store=self.angles[i]
                count = 0
                for j in range(0,len(self.angles)):
                    if store==self.angles[j]:
                        count+=1
                    else:
                        continue
                if count>=2:
                    return False
                else:
                    return True
        else:
            for i in range(len(self.angles)):
                store=self.angles[i]
                count = 0
                for j in range(0,len(self.angles)):
                    if store==self.angles[j]:
                        count+=1
                    else:
                        continue
                if count>=2:
                    return False
                else:
                    return True

        
        
