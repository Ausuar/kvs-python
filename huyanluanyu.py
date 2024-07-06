       def next_number(n):
         next=0
         while n>0:
            yushu=n%10
            n=n//10
            next+=yushu**2
         return yushu
       seen = []
       while n!=1 and n not in seen:
          seen.append(n)
          n=next_number(n)
       return n==1