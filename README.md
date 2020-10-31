# Protein Transcription
### Worked while taking CIIC3011 (Intro to Programming) course at UPRM, Spring 2018.

This project consisted of implementing a simple protein transcription processor. The program would have a protein codon table file with names of preexisting codons, and would find the starting and ending codons of the DNA string. After finding the start and end positions, the program then writes in a text file the codons inside those boundaries. If no start and end codon is found in the line, an error is printed (Bad codon string), else if either start or end don't exist in the line, it prints another error (Transcription never starts/ends). After the program finishes, it writes the codons with most repetitions and the amount of repetitions in the output text file.
