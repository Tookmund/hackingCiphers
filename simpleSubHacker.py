import os, re, copy, pprint, simpleSubCipher, makeWordPatterns

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main()
import wordPatterns

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    print('Hacking...')
    letterMapping = hackSimpleSub(message)

    print('Mapping:')
    pprint.pprint(letterMapping)
    print('\nOriginal ciphertext:')
    print(message+'\n')
    hackedMessage = decryptWithCipherletterMapping(message,letterMapping)
    print(hackedMessage)

def getBlankCipherletterMapping():
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P':
[], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
'Y': [], 'Z': []}

def addLettersToMapping(letterMapping,cipherword,candidate):
# The letterMapping parameter is a "cipherletter mapping" dictionary
# value that the return value of this function starts as a copy of
# The cipherword parameter is a string value of the ciphertext word.
# The candidate parameter is a possible English word that the
# cipherword could decrypt to.

    letterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])
    return letterMapping

def intersectMappings(mapA,mapB):
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:
        # An empty list means "any letter is possible". In this case just copy the other map entirely
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)
    return intersectedMapping

def removeSolvedLettersFromMapping(letterMapping):
    # Cipher letters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other
    # letter. (This is why there is a loop that keeps reducing the map.)
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        loopAgain = False
        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])
        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        loopAgain = True
    return letterMapping

def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('',message.upper()).split()
    for cipherword in cipherwordList:
        newMap = getBlankCipherletterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            # Word is not in dictionary
            continue
        for candidate in wordPatterns.allPatterns[wordPattern]:
            newMap = addLettersToMapping(newMap,cipherword,candidate)

        intersectedMap = intersectMappings(intersectedMap,newMap)

    return removeSolvedLettersFromMapping(intersectedMap)

def decryptWithCipherletterMapping(ciphertext, letterMapping):
    key = ['x']*len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(),'_')
            ciphertext = ciphertext.replace(cipherletter.upper(),'_')
    key = ''.join(key)
    return simpleSubCipher.decryptMessage(key,ciphertext)

if __name__ == '__main__':
    main()
