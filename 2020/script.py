import numpy as np
from random import shuffle

filenames = ['a_example', 'b_read_on', 'c_incunabula', 'd_tough_choices', 'e_so_many_books', 'f_libraries_of_the_world']
filenames = ['a_example']
scores = []

debug = False

class Library:
    
    def __init__(self, idx, books_ids, signup_days, books_scan_each_day):
        self.idx = idx
        self.books_ids = books_ids
        self.books_nr = len(self.books_ids)
        self.signup_days = signup_days
        self.books_scan_each_day = books_scan_each_day
        self.library_score = 0
        self.signed_up = False

    def __str__(self):
        baseStr = f'idx: {self.idx} n_b:{self.books_nr} d:{self.signup_days} s:{self.library_score} su:{self.signed_up}'
        return baseStr if not debug else f'books:{self.books_ids} ' + baseStr 
    

class Book:
    
    def __init__(self, book_id, score):
        self.book_id = book_id
        self.score = int(score)
        self.scanned = False
        self.count = 0
        
    def __str__(self):
        return f'{self.book_id} {self.scanned}'


def main():
    
    for fname in filenames:

        print(f'\nSTART {fname}')

        # -- INPUT PARSER
        # B = books number
        with open(f'in/{fname}.txt') as f:
            B, L, D = map(int, f.readline().split())
            books = []
            for i, bs in enumerate(f.readline().split()):
                books.append(Book(i, bs))
            books = np.array(books)
            
            libraries = []
            for i in range(L):
                nbooks, days, books_scan_each_day = map(int, f.readline().split())
                book_idxs = np.array(f.readline().split(), dtype=int)
                for b in books[book_idxs]:
                    b.count += 1
                    #print(b.count, b.score)
                libraries.append(Library(i, book_idxs, days, books_scan_each_day))



        # -- SOLUTION
        for l in libraries:
            l.library_score = sum([b.score for b in books[l.books_ids] if not b.scanned])
        
        
        # max score first
        libraries = sorted(libraries, key=lambda l: l.library_score, reverse=True)
        
        d = 0
        i = 0
        j=0
        loop = True
        signup_another_library = True
        d1 = 0
        score = 0
        lib_list = []
        book_per_library = {}
        for j in range(L):
            book_per_library[j] = []
        while(loop):
            if j % 10 == 0:
                for l in libraries:
                    l.library_score = sum([b.score for b in books[l.books_ids] if not b.scanned])

                libraries = sorted(libraries, key=lambda l: (float(l.library_score) / float(l.signup_days)), reverse=True)
                j = 0
            else:
                j+=1
            for l in libraries:
                if l.signed_up:
                    continue
                else:
                    print('new l')
                    curr_lib = l
                    lib_list.append(curr_lib)
                    break
                        
            if i == len(libraries) or (d + curr_lib.signup_days) > D:
                signup_another_library = False
                d1 = D - d
                loop = False
            
            # 
            
            if signup_another_library:
                d1 = curr_lib.signup_days
                print('signing up library', str(curr_lib), 'score ', curr_lib.library_score)
                d += d1
            
            if debug:
                print(f'\nd:{d} d1:{d1}')
                
            for l in libraries:
                if not l.signed_up:
                    continue
                
                not_scanned_books = [b for b in books[l.books_ids] if not b.scanned]
                library_books = sorted(not_scanned_books, key=lambda b: b.score, reverse=True)
                
                if not library_books:
                    continue
                
                
                max_books_sc = min(l.books_scan_each_day*d1, len(library_books))
                for b in library_books[:max_books_sc]:
                    print(f'Scanning b {b.book_id} of l {l.idx} with score {b.score}, newScore: {score + b.score}')
                    b.scanned = True
                    score += b.score
                book_per_library[l.idx] += [b.book_id for b in library_books[:max_books_sc]] 
                
                if debug:
                    print(str(l) + ' i: ' + str(i))
                    print([str(lb) for lb in library_books])
            

            if i < len(libraries):
                curr_lib.signed_up = True
                i += 1
                
            if d > D:
                loop = False
                
        #print(book_per_library)
        
        # -- OUTPUT
        with open(f'out/{fname}.out', 'w') as f:
            count = 0
            for k, v in book_per_library.items():
                if v:
                    count += 1
            f.write(f'{count}\n')
            for l in lib_list:
                if len(book_per_library[l.idx]) > 0:
                    f.write(f'{l.idx} {len(book_per_library[l.idx])}\n')
                    f.write(' '.join(map(str, book_per_library[l.idx])))
                    f.write('\n')
        print(f'\nEND {fname}')
        print(f'\nSCORE {score}')
        

if __name__ == '__main__':
    main()