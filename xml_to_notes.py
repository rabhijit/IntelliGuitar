import xml.etree.ElementTree as ET

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
                            this_note.append(note_duration_staff1)
                        else:
                            this_note.append(note_duration_staff2)
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

print(xml_to_notes("ruicong's song.xml"))
            

