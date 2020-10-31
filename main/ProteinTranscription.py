#######################################################################################################################
# Name: Yavier A. Mari Rodriguez
#
#       This Python program transcribes a sequence of DNA to a sequence of amino acids. Additionally, it find the
# amino acids that were more frequent in the file along with the amount of times it was transcribed.
#
#######################################################################################################################
def getDNAInput(DNAInputFile):
    DNALinesList = open(DNAInputFile).readlines()
    return DNALinesList

def codonCount():
    codonTable = open("codonTable.txt")
    proteinTriList = dict()   # trinames/names dictionary

    for j in codonTable:   # start filling the 3 dictionaries with their corresponding information
        if j.startswith("Start"):
            pass
        elif j.startswith("Stop"):
            pass
        else:
            fullAmino = j.split()
            proteinTriList[fullAmino[1]] = fullAmino[0]

    readOutput = open("DNAOutput.txt", "r+")   # begin counting codons
    presentCodons = dict()

    for codonLine in readOutput:   # find valid codons lines(ignore errors lines)
        if not codonLine.startswith("Error"):
            strippedCodonLine = codonLine.rstrip()
            outputLine2 = strippedCodonLine.split(":")
            for t in outputLine2:
                for o,p in proteinTriList.items():
                    if t == o:
                        presentCodons[p] = presentCodons.get(p, 0) + 1

    largest = 0   # find the most repeating codons
    for d,q in presentCodons.items():
        if q > largest:
            largest = q

    bigRepeat = list()
    for key,val in presentCodons.items():  # write most repeated codon names on a list
        if largest == val:
            bigRepeat.append(key)

    readOutput.write("The protein(s) that appeared the most times (" + str(largest) + " times) is(are):\n")
    for largestCodons in bigRepeat:
        readOutput.write(largestCodons + "\n")

    readOutput.close()   # finish writing top count and most repeated

    with open("DNAOutput.txt", "r") as finalOutput:   # print the output file for the user
        print(finalOutput.read())

def transcribe(codonTableFile = "codonTable.txt"):
    class GetOutOfLoop(Exception):
        pass

    DNAOutput = open("DNAOutput.txt", "r+")
    DNAOutput.truncate()

    booleanCodons = dict()    # start/stop codons dictionary
    triNamesList = dict()     # trinames/codons dictionary

    codonTable = open(codonTableFile).readlines()

    for j in codonTable:   # start filling the 3 dictionaries with their corresponding information
        if j.startswith("Start"):
            fullAmino = j.split()
            del fullAmino[:3]
            codons = list()
            for i in fullAmino:
                codons.append(i)
            booleanCodons["Start"] = codons
        elif j.startswith("Stop"):
            fullAmino = j.split()
            del fullAmino[:3]
            codons = list()
            for i in fullAmino:
                codons.append(i)
            booleanCodons["Stop"] = codons
        else:
            fullAmino = j.split()
            fullAminoCopy = j.split()
            del fullAmino[:3]
            codons = list()
            for i in fullAmino:
                codons.append(i)
            triNamesList[fullAminoCopy[1]] = codons

    DNAInput = getDNAInput(DNAInputFile = "DNAInput.txt")

    for inpLine in DNAInput:   # read the file and work on it line by line
        if len(inpLine) == 0:
            continue
        inpLine = inpLine.rstrip()
        outputLine = ""
        condition = True
        startCondition = True
        A = 0
        B = 0
        C = 0

        while condition:
            for i in range(0,(len(inpLine)-1), 3):   # start reading the codons three characters at a time
                readCodon = inpLine[i:i+3]
                if len(outputLine) != 0:
                        if "-" not in outputLine:
                            C = C + 1
                        for z, r in triNamesList.items():
                            try:
                                for m, n in booleanCodons.items():
                                    if m == "Stop":
                                        if readCodon in n:
                                            outputLine = outputLine + "-"
                                            B = B + 1
                                            raise GetOutOfLoop   # stop was found, jump to except condition
                                if readCodon in r:
                                    outputLine = outputLine + z + ":"
                                    break
                            except GetOutOfLoop:
                                break

                while startCondition:   # find start codon, begin transcribing
                    for k,v in booleanCodons.items():
                        if B == 0:
                            if readCodon in v:
                                if k == "Start":
                                    outputLine = outputLine + "+"
                                    A = A + 1
                                    startCondition = False
                    break


            if "-" in outputLine:   # eliminates anything beyond "-" if it already stopped
                stopIndex = outputLine.index("-")
                outputLine = outputLine[:stopIndex+1]
                C = C - 1
                goodCodonTest = outputLine[1:len(outputLine)-2]
                goodCodonTest = goodCodonTest.split(":")
                if len(goodCodonTest) != C:
                    outputLine = "ERROR: Bad codon string"
                    DNAOutput.write(outputLine + "\n")
                    condition = False
                    break

            if A == 1 and B == 1:   # if start/stop was found, proceed
                outputLine = outputLine[1:len(outputLine)-2]
                DNAOutput.write(outputLine + "\n")
                condition = False
            elif A == 1 and B == 0:   # if it started but never ended, proceed
                outputLine = "ERROR: Transcription never stops"
                DNAOutput.write(outputLine + "\n")
                condition = False
            else:
                outputLine = "ERROR: Transcription never starts"
                DNAOutput.write(outputLine + "\n")
                condition = False

    DNAOutput.write("\n")
    DNAOutput.close()   # finish transcription

    codonCount()   # count all the repeating codons in the output and print the most repeated with the count

#######################################################################################################################

transcribe()
