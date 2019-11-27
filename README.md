# EB - IntelliGuitar
Entry for HacknRoll 2019


### Team Members
Abhijit Ravichandran, 
Hemanshu Gandhi 159,
Lim Kai Yu Bridget Grace, 
Zhu Ruicong 838


### Special Prizes we wish to be considered for
Best Freshman Hack, Most Socially Useful Hack


### Inspiration
Figuring out how to play a song one has heard is a constant struggle faced by guitarists. A good ear for music and experience is needed to decide the best possible way to play a given combination of notes, as the ability to play the same note in multiple ways complicates the task. Tablature for uncommon songs is also difficult to find online, and are manually created, rather than generated using software.


### What it does
Our algorithms utilise a host of criterion to determine the best possible fingering of a song, converting the information into user-friendly visual tablature.


### How we built it 
Our script runs a tool[1] to convert an audio file to musicXML via command line. We wrote an XML parser to retrieve the necessary data from the text file. We then designed our own procedural algorithms to suggest the best possible fingerings for the song. Our priority was to suggest fingerings based on the proximity of the notes that occur consecutively in each measure, how close they are to the head of the guitar (to maximise ease of play for beginners) and whether they minimise movement horizontally across the neck, amongst others.


### Challenges we ran into
Determining the best possible fingerings for a given song on the guitar remains an active area of research due to the numerous possible permutations, hence we were unable to find existing algorithms to aid us. Furthermore, we had to decide on a set of criterion for the basis of the designed algorithm using our own playing experience.


### Accomplishments that we’re proud of
It works 


### Built with
[1] AnthemScore, Python

### Further Plans
The project was developed on a Unix system, and can be further developed to operate on Windows.
