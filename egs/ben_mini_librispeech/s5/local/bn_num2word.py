

import re
from tqdm import tqdm


class Num2WordBn():
    def __init__(self):
        self.eng_to_bn_dict = {'1' : '১', 
                         '2' : '২', 
                         '3' : '৩', 
                         '4' : '৪', 
                         '5' : '৫',
                         '6' : '৬', 
                         '7' : '৭', 
                         '8' : '৮', 
                         '9' :'৯', 
                         '0' : '০'}
        self.num_to_bd_dict = {'1': 'এক',
                 '10': 'দশ',
                 '11': 'এগার',
                 '12': 'বার',
                 '13': 'তের',
                 '14': 'চৌদ্দ',
                 '15': 'পনের',
                 '16': 'ষোল',
                 '17': 'সতের',
                 '18': 'আঠার',
                 '19': 'ঊনিশ',
                 '2': 'দুই',
                 '20': 'বিশ',
                 '21': 'একুশ',
                 '22': 'বাইশ',
                 '23': 'তেইশ',
                 '24': 'চব্বিশ',
                 '25': 'পঁচিশ',
                 '26': 'ছাব্বিশ',
                 '27': 'সাতাশ',
                 '28': 'আঠাশ',
                 '29': 'ঊনত্রিশ',
                 '3': 'তিন',
                 '30': 'ত্রিশ',
                 '31': 'একত্রিশ',
                 '32': 'বত্রিশ',
                 '33': 'তেত্রিশ',
                 '34': 'চৌত্রিশ',
                 '35': 'পঁয়ত্রিশ',
                 '36': 'ছত্রিশ',
                 '37': 'সাঁইত্রিশ',
                 '38': 'আটত্রিশ',
                 '39': 'ঊনচল্লিশ',
                 '4': 'চার',
                 '40': 'চল্লিশ',
                 '41': 'একচল্লিশ',
                 '42': 'বিয়াল্লিশ',
                 '43': 'তেতাল্লিশ',
                 '44': 'চুয়াল্লিশ',
                 '45': 'পঁয়তাল্লিশ',
                 '46': 'ছেচল্লিশ',
                 '47': 'সাতচল্লিশ',
                 '48': 'আটচল্লিশ',
                 '49': 'ঊনপঞ্চাশ',
                 '5': 'পাঁচ',
                 '50': 'পঞ্চাশ',
                 '51': 'একান্ন',
                 '52': 'বায়ান্ন',
                 '53': 'তিপ্পান্ন',
                 '54': 'চুয়ান্ন',
                 '55': 'পঞ্চান্ন',
                 '56': 'ছাপ্পান্ন',
                 '57': 'সাতান্ন',
                 '58': 'আটান্ন',
                 '59': 'ঊনষাট',
                 '6': 'ছয়',
                 '60': 'ষাট',
                 '61': 'একষট্টি',
                 '62': 'বাষট্টি',
                 '63': 'তেষট্টি',
                 '64': 'চৌষট্টি',
                 '65': 'পঁয়ষট্টি',
                 '66': 'ছেষট্টি',
                 '67': 'সাতষট্টি',
                 '68': 'আটষট্টি',
                 '69': 'ঊনসত্তর',
                 '7': 'সাত',
                 '70': 'সত্তর',
                 '71': 'একাত্তর',
                 '72': 'বাহাত্তর',
                 '73': 'তিয়াত্তর',
                 '74': 'চুয়াত্তর',
                 '75': 'পঁচাত্তর',
                 '76': 'ছিয়াত্তর',
                 '77': 'সাতাত্তর',
                 '78': 'আটাত্তর',
                 '79': 'ঊনআশি',
                 '8': 'আট',
                 '80': 'আশি',
                 '81': 'একাশি',
                 '82': 'বিরাশি',
                 '83': 'তিরাশি',
                 '84': 'চুরাশি',
                 '85': 'পঁচাশি',
                 '86': 'ছিয়াশি',
                 '87': 'সাতাশি',
                 '88': 'আটাশি',
                 '89': 'ঊননব্বই',
                 '9': 'নয়',
                 '90': 'নব্বই',
                 '91': 'একানব্বই',
                 '92': 'বিরানব্বই',
                 '93': 'তিরানব্বই',
                 '94': 'চুরানব্বই',
                 '95': 'পঁচানব্বই',
                 '96': 'ছিয়ানব্বই',
                 '97': 'সাতানব্বই',
                 '98': 'আটানব্বই',
                 '99': 'নিরানব্বই'}
        self.num_to_bn_decimal_dict = {'0':'শূন্য ','1':'এক ','2':'দুই ','3':'তিন ','4':'চার ','5':'পাঁচ ','6':'ছয় ','7':'সাত ','8':'আট ', '9':'নয় '}
        self.hundred_str = 'শ'
        self.thousand_str = 'হাজার'
        self.lakh_str = 'লক্ষ'
        self.crore_str = 'কোটি'
        
        
    
    
    def _translate(str, s, repl):
        pattern = '|'.join(map(re.escape, sorted(repl, key=len, reverse=True)))
        return re.sub(pattern, lambda m: repl[m.group()], s)
    
        
    def eng_to_bn(self, number): 
        return self._translate(number, self.eng_to_bn_dict)
    
    
    def num_to_bn(self, number):
        return self._translate(number, self.num_to_bd_dict)
    
    
    def num_to_bn_decimal(self, number):
        return self._translate(number, self.num_to_bn_decimal_dict)
    
    
    def under_hundred(self, number):
        if int(number) == 0:
#             return 'শূন্য'
            return ''
        else:
            return self.num_to_bn(number)
        
        
    def hundred(self, number):
        a = int(int(number)/100)
        b = int(number) % 100;
        if a == 0:
            hundred = ''
        else: 
            hundred = self.num_to_bn(str(a)) + '' + self.hundred_str
        return hundred + ' ' + self.under_hundred(str(b))
    
    
    
    def thousand(self, number):
        a = int(int(number)/1000)
        b = int(number) % 1000
        if a == 0:
            thousand = ''
        else:
            thousand = self.num_to_bn(str(a)) + ' ' + self.thousand_str
        return re.sub(r' {2,}',' ',thousand + ' ' + self.hundred(str(b)))
        #return self.under_hundred(str(a)) + 'শ ' + self.under_hundred(str(b))

    
    
    def lakh(self, number): 
        a = int(int(number)/100000)
        b = int(number) % 100000
        if a == 0:
            lakh = ''
        else: 
            lakh = self.num_to_bn(str(a)) + ' ' + self.lakh_str
        return re.sub(r' {2,}',' ',lakh + ' ' + self.thousand(str(b)))
    
    
    def crore(self, number): 
        a = int(int(number)/10000000)
        b = int(number) % 10000000
        if a > 99:
            more_than_crore = self.lakh(str(a))
        else: 
            more_than_crore = self.num_to_bn(str(a))
        return re.sub(r' {2,}',' ',more_than_crore + ' ' + self.crore_str + ' ' + self.lakh(str(b)))
    
    '''
    def _year_19th_century(self, number):
        a = int(int(number)/100)
        b = int(number) % 100
        if a == 0:
            thousand = ''
        else:
            thousand = self.num_to_bn(str(a)) + ' ' + self.thousand_str
        # return thousand + ' ' + self.hundred(str(b))
        return self.under_hundred(str(a)) + 'শ ' + self.under_hundred(str(b))
    '''
        
    def thousand_small(self, number):
        a = int(int(number)/100)
        b = int(number) % 100
        if a == 0:
            thousand = ''
        else:
            thousand = self.num_to_bn(str(a)) + ' ' + self.thousand_str
        # return thousand + ' ' + self.hundred(str(b))
        return self.under_hundred(str(a)) + 'শ ' + self.under_hundred(str(b))
        
        
        
    def num_to_word(self, number):
        #if not number.isdigit():
        #   raise Exception('Not a number')
        p = re.compile('\d+($|(\.\d+)$)')
        if not p.match(number):
            raise Exception('Not a number')
        # check if 19 century date like 1923
        #if re.match('19(\d{2})', number):    
         #   return self._year_19th_century(number)
        if re.match(r'[1-9]0[0-9]{2}$', number):
            # do nothing, continue normal execution flow
            pass
        elif re.match(r'[1-9][0-9]{3}$', number):
            return self.thousand_small(number)

        #if re.match('2(\d{3})', number) and len(number) < 5:    
         #   return self.thousand_small(number)

        #if re.match('3(\d{3})', number) and len(number) < 5:    
         #   return self.thousand_small(number)

        #if re.match('4(\d{3})', number) and len(number) < 5:    
         #   return self.thousand_small(number)

        
        # check if float
        try:
            dummy = float(number)
            dot = number.split('.')
            return self.number_selector(dot[0]) + 'দশমিক ' + self.num_to_bn_decimal(dot[1])
        except:
            # not a float
            
            # remove trailing zeroes if not a float
            if len(number)> 1 and number != '0':
                number = number.lstrip('0')
                if number == '':
                    number = '0'
            return self.number_selector(number)
        
        
    def number_selector(self, number):
        if (int(number) > 9999999):
            return self.crore(number)
        elif (int(number) > 99999):
            return self.lakh(number)
        elif (int(number) > 999):
            return self.thousand(number)
        elif (int(number) > 99) :
            return self.hundred(number)
        else:
            return self.under_hundred(number)
        
        
    


# In[3]:

"""
a = Num2WordBn()
a.num_to_word('111234')


# In[4]:


try:
    a.num_to_word('বার হাজার তিনশত তেত্রিশ ১২৩৩৩')
except:
    print('Not a Number')


# In[ ]:


for line in tqdm(open('corpus.txt', 'r')):
    for word in line.split():
        try:
            res = a.num_to_word(word)
        except:
            res = word
        with open('bn_corpus.txt', 'a') as f:
            f.write(str(res) + ' ')

"""