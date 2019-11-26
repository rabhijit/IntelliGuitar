import os

begin = ["e-|","\nB-|","\nG-|","\nD-|","\nA-|","\nE-|"]
next = ["-","-","-","-","-","-"]
new_measure = ["|","|","|","|","|","|"]
filename = "guru99.txt"
f= open(filename,"w+")
def combine(begin, next):
     for i in range(6):
          begin[i] = begin[i] + next[i]
     return begin

def wow(lst):
     string = ""
     for i in lst:
          string += i
     return string
     
#print_list(begin)
#print_list(combine(begin, next))
          
hello = {1:{0:[(3,2)]}}
#dict = {1:{1:[(3,2),(4,0)],2:[(5,0)],3:[(4,2)],4:[(6,0)],5:[(3,0)]},2:{5:[(5,2)]},3:{3:[(1,1),(2,4)]},4:{3:[(1,1),(2,4)]},5:{3:[(1,1),(2,4)]},6:{3:[(1,1),(2,4)]}}
#dict = {1:{1:[(3,2),(4,0)],5:[(5,0)]},2:{5:[(5,2)]},3:{3:[(1,1),(2,4)]},4:{3:[(1,1),(2,4)]}}
dict = {1: {16: (5, 3)}, 2: {7: [(3, 0), (2, 3), (1, 0)], 8: [(5, 3), (2, 1)], 12: [(4, 5), (2, 1)], 16: [(5, 3), (2, 1)], 14: (4, 5)}, 3: {7: [(5, 3), (2, 3)], 13: [(4, 2), (3, 0), (2, 1)], 16: [(4, 5), (2, 1)], 3: (4, 5), 5: (4, 5), 9: [(3, 0), (2, 3), (1, 0)]}}

def list_4(dict):
     list_of_dicts = []
     dic_1 = {}
     for i in dict.keys():
          dic_1[i] = dict[i]
          if len(dic_1) == 4:
               dic_2 = dic_1.copy()
               list_of_dicts.append(dic_1)
               dic_1 = {}
     if dic_1:
          list_of_dicts.append(dic_1)
     return list_of_dicts
#print(list_5(dict))

def print_further(lst):
     print(wow(lst))
def print_space(line):
     print(line)
def compile(begin, next, new_measure, dict):
     lst = list_4(dict)
     for x in lst:
          original = begin.copy() #update the value
          for i in x.values(): #repeat for each measure
               for j in range(1,17):
                    if j in i.keys():
                         new = next
                         for a in i[j]:
                              new = new[:a[0]-1] + [str(a[1])] + new[a[0]:]
                         original = combine(original, new)
                         original = combine(original, next)
                    else:#print updated next
                         original = combine(original, next)
                         original = combine(original, next)
               original = combine(original, new_measure)
          print_further(original)
          print_space(" ")
          f.write("\n" + wow(original))
          f.write("\n ")
compile(begin, next, new_measure, dict)

#print(f.read())
f.close()
#f=open("guru99.txt", "r")
#print(f.read())

os.system("open " + filename)
