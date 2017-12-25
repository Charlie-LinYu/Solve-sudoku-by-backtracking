import numpy as np
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

class sudoku:
    def __init__(self,case):
        case1=[]
        for row in range(9):
            tmp=[]
            for col in range(9):
                tmp.append(int(case[row*9+col]))
            case1.append(tmp)
        self.case=np.asmatrix(case1)
        self.checked=[]
        self.times=0
        self.t=0

    def check(self,i,j,num):
        if self.case[i,j]!=0:
            return False
        elif num in self.case[i,:]:
            return False
        elif num in self.case[:,j]:
            return False
        elif num in self.case[(i//3)*3:(i//3)*3 + 3,(j//3)*3:(j//3)*3 + 3]:
            return False
        else:
            return True

    def find_next(self):
        for row in range(9):
            for col in range(9):
                if self.case[row,col]==0:
                    return row,col
        if row==8 and col==8 and self.case[row,col]!=0:
            return -1,-1

    def solve(self):
        self.times=self.times+1
        if self.times%10000 == 0:
            print(self.times)
        (row,col)=self.find_next()
        if (row!=-1 and col!=-1):
            for num in range(1,10):
                if self.check(row,col,num):
                    self.case[row,col]=num
                    self.checked.append((row,col))
                    next_p=self.find_next()
                    if next_p[0]==-1:
                        return True
                    else:
                        tmp=self.solve()
                        if not tmp:
                            last_p=self.checked.pop()
                            self.case[last_p[0],last_p[1]]=0
                        else:
                            return True
        else:
            return True


if __name__ == '__main__':
    year=input('Year: ')
    month=input('Month: ')
    day=input('Day: ')
    difficulty=input('Difficulty(0-4): ')
    url='http://cn.sudokupuzzle.org/printable.php?nd='+str(difficulty)+ \
        '&y='+str(year)+'&m='+str(month)+'&d='+str(day)

    web=requests.get(url)
    soup=BeautifulSoup(web.text,"html.parser")
    case=re.findall(r"\t\ttmda=\'(.*)\';\n",soup.script.string)[0][0:81]

    problem=sudoku(case)
    t1=datetime.now()
    problem.solve()
    print('Result:')
    print(problem.case)
    t2=datetime.now()
    print('Time consuming: '+str(t2-t1))