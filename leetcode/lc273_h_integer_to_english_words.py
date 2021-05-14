class Solution:
    def __init__(self):

        self.ones = {
            0: '',
            1: 'One',
            2: 'Two',
            3: 'Three',
            4: 'Four',
            5: 'Five',
            6: 'Six',
            7: 'Seven',
            8: 'Eight',
            9: 'Nine',
            10: 'Ten',
            11: 'Eleven',
            12: 'Twelve',
            13: 'Thirteen',
            14: 'Fourteen',
            15: 'Fifteen',
            16: 'Sixteen',
            17: 'Seventeen',
            18: 'Eighteen',
            19: 'Nineteen'
        }

        self.tens = {
            20: 'Twenty',
            30: 'Thirty',
            40: 'Forty',
            50: 'Fifty',
            60: 'Sixty',
            70: 'Seventy',
            80: 'Eighty',
            90: 'Ninety'                        
        }
        
        self.powers = ['', 'Thousand', 'Million', 'Billion']
        
    def t2(self, s):
        """
        Transcribe two digit number
        """
        if s in self.ones:
            return self.ones[s]
        
        if s in self.tens:
            return self.tens[s]
        
        res = []
        t = self.tens[10 * (s // 10)]
        u = self.ones[s % 10]
        return f'{t} {u}'
            
    def t3(self, s):
        """
        Transcribe three digit number
        """
        if s == 0:
            return ''

        if s < 100:
            return self.t2(s)
        
        h = self.ones[s//100].strip()
        t2 = self.t2(s % 100).strip()
        return f'{h} Hundred {t2}'.strip()
            
    def numberToWords(self, num: int) -> str:  
        if num == 0:
            return 'Zero'
        
        res = '' 
        p = 0
        
        # Loop through the number in groups of 3 digits
        while num > 0:
            d3 = num % 1000      
            t = self.t3(d3)
            if t:
                c = f'{t} {self.powers[p]}'
                res = c + ' ' + res
                
            num //= 1000
            p += 1
            
        return res.strip()
