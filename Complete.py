import os
import xml.etree.ElementTree as ET
from math import *
import networkx as nx

audio_file = "Sample Song.m4a"
output_file = "Sample Song.xml"

def wow(lst):
     string = ""
     for i in lst:
          string += i
     return string
    
def mac_space(str):
    lst = []
    for i in str:
        lst.append(i)
    for j in range(len(lst)):
        if lst[j] == " ":
            lst = lst[:j] + ["\ "] + lst[j+1:]
    return wow(lst)

os.system("cd ..")
os.system("/Applications/AnthemScore.app/Contents/MacOS/AnthemScore " + mac_space(audio_file) + " -a -x " + mac_space(output_file))


def xml_to_notes(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    measures = {}
    notes = []
    this_note = []
    note_duration_staff1 = 0
    note_duration_staff2 = 0
    count = 0
    temp = 0
    real_note = False
    is_chord = False

    for child in root.iter():
        if child.tag == 'measure':
            if int(list(child.attrib.values())[0]) != 1:
                measures[int(list(child.attrib.values())[0])-1] = notes
            notes = []
            note_duration_staff1 = 0
            note_duration_staff2 = 0
        if child.tag == 'note':
            for j in child.iter():
                if j.tag == 'chord':
                    is_chord = True
                if j.tag == 'pitch':
                    real_note = True
                if j.tag == 'duration':
                    temp += int(j.text)
                if j.tag == 'staff' and is_chord == False:
                    if j.text == '1':
                        note_duration_staff1 += temp
                    else:
                        note_duration_staff2 += temp
            temp = 0

            for i in child.iter():       
                if (i.tag == 'step' or i.tag == 'alter' or i.tag == 'octave' or i.tag == 'staff') and real_note == True:
                    count += 1
                    if (i.tag != 'staff'):
                        this_note.append(i.text)
                    if i.tag == 'staff':
                        if i.text == '1':
                            this_note.append(note_duration_staff1 / 6)
                        else:
                            this_note.append(note_duration_staff2 / 6)
                    if count == 4:
                        notes.append(this_note)
                        this_note = []
                        count = 0
            real_note= False
            is_chord = False

    # E2 is 12 (lowest note)

    def note_to_number(note, alter, octave):
        keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        # A +2 B +1 C +2 D +2 E +1 F +2 G
        intervals = [2, 1, 2, 2, 1, 2]
        E = 7
        # E1 = 0, E2 = 12
        initial_no = 0
        for i in range(len(keys) - 1):
            if keys[i] == note:
                break
            initial_no += intervals[i]
        initial_no -= E
        initial_no = (octave - 1) * 12 + initial_no
        return initial_no + alter

    new_measures = {}
    new_notes = []

    for measure in measures.keys():
        new_measures[measure] = {}
        for note, alter, octave, timing in measures[measure]:
            new_note = note_to_number(note, int(alter), int(octave))
            if timing not in new_measures[measure] and new_note >= 12: # change for tuning
                new_measures[measure][timing] = [new_note]
            elif timing in new_measures[measure] and new_note >= 12: # change for tuning
                new_measures[measure][timing].append(new_note)

    return new_measures

#print(xml_to_notes(output_file))

def notes_to_frets(test_song):

    notesdic={}

    #test_song = {1: {96: [32]}, 2: {36: [34], 60: [36, 17], 84: [37], 96: [39]}, 3: {30: [37], 54: [36], 72: [34], 96: [32]}, 4: {}, 5: {78: [34], 96: [36]}, 6: {24: [38, 57], 48: [39], 72: [29], 90: [39], 96: [38]}, 7: {42: [36], 90: [34], 96: [34]}, 8: {}, 9: {96: [34, 58, 17], 72: [26]}, 10: {90: [34, 58], 96: [34, 58, 26], 24: [26], 42: [12, 24], 66: [26], 84: [17]}, 11: {90: [34, 58], 96: [34, 58, 26], 36: [14], 54: [26], 78: [17]}, 12: {54: [33], 90: [34], 96: [34], 48: [17]}, 13: {96: [61, 28, 17], 24: [22], 48: [24], 66: [28, 17], 90: [24]}, 14: {36: [24], 60: [24, 28, 17], 78: [24], 96: [28, 19]}, 15: {72: [32], 96: [34, 58, 28], 18: [24], 36: [28], 66: [24]}, 16: {90: [32, 24], 96: [32, 24], 18: [24], 42: [28]}, 17: {}, 18: {84: [31, 43], 96: [29]}, 19: {30: [29], 48: [31], 72: [31], 90: [29], 96: [29]}, 20: {36: [31], 60: [31, 43], 78: [29], 96: [29, 17]}, 21: {30: [31], 54: [31], 72: [29], 96: [29]}, 22: {18: [31], 42: [31], 66: [29, 17], 84: [29, 17], 96: [31, 43]}, 23: {36: [31, 43], 54: [29], 78: [29], 96: [31]}, 24: {24: [31, 47], 48: [29], 72: [29], 96: [31]}}
    #test_song = {1: {96: [32]}, 2: {36: [34], 60: [36, 17], 84: [37], 96: [39]}, 3: {30: [37], 54: [36], 72: [34], 96: [32]}, 4: {}, 5: {78: [34], 96: [36]}, 6: {24: [38], 48: [39], 72: [29], 90: [39], 96: [38]}, 7: {42: [36], 90: [34], 96: [34]}, 8: {}, 9: {96: [34, 17], 72: [26]}, 10: {90: [34], 96: [34, 26], 24: [26], 42: [12, 24], 66: [26], 84: [17]}, 11: {90: [34], 96: [34, 26], 36: [14], 54: [26], 78: [17]}, 12: {54: [33], 90: [34], 96: [34], 48: [17]}, 13: {24: [22], 48: [24], 66: [28, 17], 90: [24], 96: [28, 17]}, 14: {36: [24], 60: [24, 28, 17], 78: [24], 96: [28, 19]}, 15: {72: [32], 96: [34, 28], 18: [24], 36: [28], 66: [24]}, 16: {90: [32, 24], 96: [32, 24], 18: [24], 42: [28]}, 17: {}, 18: {84: [31, 43], 96: [29]}, 19: {30: [29], 48: [31], 72: [31], 90: [29], 96: [29]}, 20: {36: [31], 60: [31, 43], 78: [29], 96: [29, 17]}, 21: {30: [31], 54: [31], 72: [29], 96: [29]}, 22: {18: [31], 42: [31], 66: [29, 17], 84: [29, 17], 96: [31, 43]}, 23: {36: [31, 43], 54: [29], 78: [29], 96: [31]}, 24: {24: [31, 47], 48: [29], 72: [29], 96: [31]}}
    #test_song = {1: {96: [32, 20, 27]}, 2: {42: [36, 34, 27], 48: [32, 20], 72: [32, 27], 96: [32, 20], 84: [27]}, 3: {42: [34, 20], 78: [32, 24, 27], 96: [32, 27], 18: [27], 30: [27], 54: [27]}}

    class string:
        def __init__(self,opennote,number):
            self.opennote=opennote
            self.notes={}
            for i in range(0,23): # last number is 1+number of frets
                self.notes[i]=opennote+i
                if str(opennote+i) not in notesdic:
                    notesdic[str(opennote+i)]=[]
                notesdic[str(opennote+i)].append((number,i))


    e=string(36,1)
    B=string(31,2)
    G=string(27,3)
    D=string(22,4)
    A=string(17,5)
    E=string(12,6)


    def get_position(note):
        lst=notesdic[str(note)]
        return lst

    def trange(thumb):
        thumb_range=list(i for i in range(thumb-1,thumb+4))
        return thumb_range


    def is_far(pos1,pos2):
        if pos1[1]-pos2[1]>4 or pos[1]-pos2[1]<-4:
            return True
        return False

        
    def is_move(note):
        for i in get_position(note):
            if i not in thumb_range and i!=0:
                return True
        else:
            return False

    ##Rules of movement:
    ##    1. prioritise downwards movement over upwards movement(always present the lowest possible neck position)
    ##
    ##    2. if multiple implementations, we compare through:
    ##        next 5 notes, use the one that lasts longest. if multiple, choose the lowest

    '''required input to visualisation module is of the form
       dict = {1:{0:[(3,2),(4,0)],4:[(5,0)]},2:{4:[(5,2)]},3:{2:[(1,1),(2,4)]}} 
    '''
    thumb_range = [0, 1, 2, 3, 4]

    def same_time_sort(notes): ##input is a list of integers sorted from small to large
        def criteria(combi):
            lsta=[]
            lstb=[]
            for i in combi:
                if i[1]!=0:
                    lsta.append(i[1])
            if lsta:
                if max(lsta)-min(lsta)>4:
                    return False
            dica={}
            for i in combi:
                if i[0] not in dica:
                    dica[i[0]]=[]
                dica[i[0]].append(i[1])
            for j in dica:
                if len(dica[j])>1:
                    return False
            return True
        
        def combinations(lst):
            if len(lst)==1:
                note=lst[0]
                combs=[]
                for i in notesdic[str(note)]:
                    comb=[i]
                    combs.append(comb)
                return combs
            else:
                combs=combinations(lst[1:])
                note=lst[0]
                k=notesdic[str(note)]
                newcombs=[]
                for i in k:
                    for j in combs:
                        lster=[i]
                        lster.extend(j)
                        new=lster.copy()
                        newcombs.append(new)
                return newcombs
        def select(combs):
            lst=[]
            for i in combs:
                if criteria(i):
                    lst.append(i)
            return lst
        def best_dis(combs):
            dist=[]
            for i in combs:
                lst=[]
                for j in i:
                    if j[1]!=0:
                        lst.append(j[1])
                if not lst:
                    dis=0
                else:
                    ave=sum(lst)/len(lst)
                    dis=fabs(ave-thumb_range[1])
                dist.append(dis)
            mini=min(dist)
            for i in combs:
                lst=[]
                for j in i:
                    if j[1]!=0:
                        lst.append(j[1])
                if not lst:
                    dis=0
                else:
                    ave=sum(lst)/len(lst)
                    dis=fabs(ave-thumb_range[1])
                if dis==mini:
                    return i
        def stretch(comb):
            lst=[]
            for i in comb:
                if i[1]!=0:
                    lst.append(i[1])
            if not lst:
                return 0
            return max(lst)-min(lst)

        def second_best(combs):
            lst=[]
            lst1=[]
            def newcrit(comb):
                dica={}
                for i in comb:
                    if i[0] not in dica:
                        dica[i[0]]=[]
                    dica[i[0]].append(i[1])
                for j in dica:
                    if len(dica[j])>1:
                        return False
                return True
            for i in combs:
                if newcrit(i):
                    lst1.append(i)
            if not lst1:
                return False
            for i in lst1:
                lst.append(stretch(i))
            mini=min(lst)
            for i in lst1:
                if stretch(i)==mini:
                    return i
        def inrange(comb):
            for i in comb:
                if i[1]!=0:
                    if i[1] not in thumb_range:
                        return False
            return True
        def newthumb(comb):
            lst=[]
            for i in comb:
                if i[1]!=0:
                    lst.append(i[1])
            if not lst:
                return
            else:
                thumbposition=min(lst)+1
                trange(thumbposition)
                return
            
                
        alf=combinations(notes)
        bet=select(alf)
        
        if bet:
            output=best_dis(bet)
            if not inrange(output):
                newthumb(output)
            return best_dis(bet)
        elif second_best(alf):
            newthumb(output)
            return second_best(alf)
        else:
            return (6,0)

    # (string, fret)

    def parser(test_song):
        result = []
        for measure, value in test_song.items():
            #key is measure,value is another dict
            for duration,notes in value.items():
                if len(notes)==1:
                    result.append(notes[0])
                else:
                    result.append(notes)
        return result

    def initial_thumb_range(parsed_song):
        if type(parsed_song[0]) == list:
            return trange(get_position(min(parsed_song[0]))[0][1])
        else:
            return trange(get_position(parsed_song[0])[0][1])

    def get_initial_position(parsed_song):
        if type(parsed_song[0]) == list:
            return get_position(min(parsed_song[0]))[0]
        else:
            return get_position(parsed_song[0])[0]

    parsed_song = parser(test_song)
    thumb_range=initial_thumb_range(parsed_song)
    initial_position = get_initial_position(parsed_song)
    thumb_position = thumb_range[1]
    notes = [[initial_position]]

    # update thumb position with each iteration

    def get_next_position(current_note, next_note):
        positions = get_position(next_note)
        mapped_positions = list(map(lambda x: x[1], positions))
        positions_in_range = []
        for i in mapped_positions:
            if i in thumb_range:
                positions_in_range.append(i)
        if len(positions_in_range) > 0:
            for i in positions:
                if i[1] == min(positions_in_range):
                    return [i]
        else:
            for i in positions:
                if min(mapped_positions) == i[1]:
                    trange(min(mapped_positions))
                    thumb_position = thumb_range[1]
                    return [i]

    def final(parsed_song):
        for i in range(1, len(parsed_song)-1):
            if type(parsed_song[i]) == list:
                parsed_song[i].sort()
                simul = same_time_sort(parsed_song[i])
                notes.append(simul)           
            else:
                next_position = get_next_position(parsed_song[i-1], parsed_song[i])
                notes.append(next_position)
        return notes


    final(parsed_song)
    noted_song = final(parsed_song)

    # dict = {1:{1:[(3,2),(4,0)],5:[(5,0)]},2:{5:[(5,2)]},3:{3:[(1,1),(2,4)]},4:{3:[(1,1),(2,4)]},5:{3:[(1,1),(2,4)]},6:{3:[(1,1),(2,4)]}}

    output_song = {}
    counter = 0

    for key, val in test_song.items():
        output_song[key] = {}
        for i in val.keys():
            output_song[key][i] = noted_song[counter]
            counter += 1

    return output_song

#print(notes_to_frets(test_song = {1: {96: [32, 20, 27]}, 2: {42: [36, 34, 27], 48: [32, 20], 72: [32, 27], 96: [32, 20], 84: [27]}, 3: {42: [34, 20], 78: [32, 24, 27], 96: [32, 27], 18: [27], 30: [27], 54: [27]}}))
#print(notes_to_frets(xml_to_notes(output_file)))
begin = ["e-|","\nB-|","\nG-|","\nD-|","\nA-|","\nE-|"]
next = ["-","-","-","-","-","-"]
new_measure = ["|","|","|","|","|","|"]
filename = "guru99.txt"
f= open(filename,"w+")

def combine(begin, next):
     for i in range(6):
          begin[i] = begin[i] + next[i]
     return begin
 
#print_list(begin)
#print_list(combine(begin, next))
          
hello = {1:{0:[(3,2)]}}
dict = {1:{1:[(3,2),(4,0)],2:[(5,0)],3:[(4,2)],4:[(6,0)],5:[(3,0)]},2:{5:[(5,2)]},3:{3:[(1,1),(2,4)]},4:{3:[(1,1),(2,4)]},5:{3:[(1,1),(2,4)]},6:{3:[(1,1),(2,4)]}}
#dict = {1:{1:[(3,2),(4,0)],5:[(5,0)]},2:{5:[(5,2)]},3:{3:[(1,1),(2,4)]},4:{3:[(1,1),(2,4)]}}
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
#compile(begin, next, new_measure, dict)
compile(begin, next, new_measure, (notes_to_frets(xml_to_notes(output_file))))
#print(f.read())
f.close()
#f=open("guru99.txt", "r")
#print(f.read())

os.system("open " + mac_space(filename))

            


