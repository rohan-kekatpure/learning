from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        n = len(words)
        numwords = 0
        lines = []
        i = 0
        line = ''

        while i < n:
            if line == '' and (len(line + words[i]) <= maxWidth):
                line += words[i]
                i += 1
                numwords += 1
                continue
            elif len(line + words[i]) < maxWidth:
                if line == '':
                    line += words[i]
                else:
                    line += ' ' + words[i]

                numwords += 1
                i += 1
                continue

            delta = maxWidth - len(line)
            if numwords == 1:
                line += ' ' * delta
                lines.append(line)
                line = ''
                numwords = 0
                continue

            linelist = line.split(' ')
            j = 0
            while j < delta:
                for k in range(len(linelist) - 1):
                    linelist[k] += ' '
                    j += 1
                    if j == delta:
                        break
            line = ' '.join(linelist)
            lines.append(line)
            line = ''
            numwords = 0

        # Process last line special
        if line:
            delta = maxWidth - len(line)
            line += ' ' * delta
            lines.append(line)
        return lines


