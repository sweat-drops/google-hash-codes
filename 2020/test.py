import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

filenames = ['a_example', 'b_read_on', 'c_incunabula', 'd_tough_choices', 'e_so_many_books', 'f_libraries_of_the_world']
filenames = filenames[-2:-1]
scores = []

# B su questo codice da 5822900
# E su questo codice da 4659153

class Library:
    
    def __init__(self, idx, books_ids, signup_days, books_per_day, score):
        self.idx = idx
        self.books_ids = books_ids
        self.signup_days = signup_days
        self.books_per_day = books_per_day
        self.score = score
        self.signed_up = False

    def __str__(self):
        return f'L (idx:{self.idx} sd:{self.signup_days} sc:{self.score} su:{self.signed_up})'
    

class Book:
    
    def __init__(self, idx, score):
        self.idx = idx
        self.score = int(score)
        self.scanned = False
        self.count = 0
        
    def __str__(self):
        return f'B (id:{self.idx} score:{self.score} scanned:{self.scanned})'


def main():
    
    for fname in filenames:

        print(f'\nSTART {fname}')

        # -- INPUT PARSER
        with open(f'in/{fname}.txt') as f:
            B, L, D = map(int, f.readline().split())
            
            books = []
            for i, s in enumerate(f.readline().split()):
                books.append(Book(i, s))
            books = np.array(books)
            
            libraries = []
            books_in_library = {}
            for i in range(L):
                nbooks, signup_days, books_per_day = map(int, f.readline().split())
                lib_score = 0
                books_idxs = np.array(f.readline().split(), dtype=int)
                for b in books[books_idxs]:
                    b.count += 1
                    lib_score += b.score
                
                libraries.append(Library(i, books_idxs, signup_days, books_per_day, lib_score))
                books_in_library[i] = []


        # -- SOLUTION
        libraries = sorted(libraries, key=lambda l: l.score, reverse=True) # max score first

        d = 0 # total elapsed time from start
        d1 = 0
        processed_libs = []
        loop = True
        score = 0
        j = 0
        while(loop):

            logging.debug('')
            if j % 10 == 0:
                for l in libraries:
                    l.score = sum([b.score for b in books[l.books_ids] if not b.scanned])
                libraries = sorted(libraries, key=lambda l: (float(l.score) / float(l.signup_days)), reverse=True)
            else:
                j += 1

            for i in range(len(libraries)):
                l = libraries[i]
                logging.debug(f'Check library {l}')
                
                if not l.signed_up and (d + l.signup_days) <= D:
                    logging.info(f'Signing {l} - d:{d} d1:{l.signup_days} newD:{d + l.signup_days}')
                    l.signed_up = True
                    processed_libs.append(l)
                    new_library = set([l])

                    d1 = l.signup_days
                    d += d1
                    break

                else:
                    continue
            
            
            for l in list(set(libraries) - new_library):
                if not l.signed_up:
                    not_scanned_books = [b for b in books[l.books_ids] if not b.scanned]
                    nsb = sorted(not_scanned_books, key=lambda b: b.score, reverse=True)
                    if not nsb:
                        continue
                    max_books_sc = min(l.books_per_day*d1, len(nsb))
                    print(f'max l scansionabili: {max_books_sc}')
                    for b in nsb[:max_books_sc]:
                        logging.debug(f'Scanning b {b.idx} of l {l.idx} with score {b.score}, newScore: {score + b.score}')
                        b.scanned = True
                        score += b.score
                        books_in_library[l.idx].append(b.idx)

            if i == L-1:
                logging.info(f'\nNo library to sign up, only scanning books for: {D - d}')
                d1 = D - d
                loop = False

        if d1 > 0:
            for l in processed_libs:
                not_scanned_books = [b for b in books[l.books_ids] if not b.scanned]
                nsb = sorted(not_scanned_books, key=lambda b: b.score, reverse=True)
                if not nsb:
                    continue
                
                max_books_sc = min(l.books_per_day*d1, len(nsb))
                for b in nsb[:max_books_sc]:
                    logging.debug(f'Scanning b {b.idx} of l {l.idx} with score {b.score}, newScore: {score + b.score}')
                    b.scanned = True
                    score += b.score
                    books_in_library[l.idx].append(b.idx)

        
        # -- OUTPUT
        with open(f'{fname}_{score}.out', 'w') as f:
            count = 0
            for k, v in books_in_library.items():
                if v:
                    count += 1
            f.write(f'{count}\n')
            
            for l in processed_libs:
                if len(books_in_library[l.idx]) > 0:
                    f.write(f'{l.idx} {len(books_in_library[l.idx])}\n')
                    f.write(' '.join(map(str, books_in_library[l.idx])))
                    f.write('\n')
        print(f'\nEND \'{fname}\' SCORED {score} diff {4653109 - score}')
        

if __name__ == '__main__':
    main()