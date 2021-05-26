class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        N = numerator
        D = denominator
        sign = '-' if N * D < 0 else ''
        
        N = abs(N)
        D = abs(D)
        
        int_part = (N // D)
        r = N % D        
        seen = []
        quotients = []
            
        while r > 0 and (not r in seen):
            seen.append(r)
            quotients.append(10 * r // D)            
            r = (10 * r) % D             
    
    
        # No fractional part
        if len(quotients) == 0:
            return f'{sign}{int_part}'
        
        # Non recurring fractional part
        if r == 0:
            frac_part = ''.join(str(f) for f in quotients)    
            return f'{sign}{int_part}.{frac_part}'

        # Recurring fraction
        idx = seen.index(r)
        unique_part = ''.join(str(q) for q in quotients[:idx])
        repeating_part = ''.join(str(q) for q in quotients[idx:])            
        frac_part = f'{unique_part}({repeating_part})'        
        return f'{sign}{int_part}.{frac_part}'

