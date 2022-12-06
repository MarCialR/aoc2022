from os import path
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from types import SimpleNamespace

from httplib2 import Http

from IPython.display import display_markdown

AOC_URL ="https://adventofcode.com/2022/day/"
PUZZLE_HTML_FILE = "./descriptions/html%d.html"
PUZZLE_MARKDOWN_FILE = "./descriptions/markdown%d.md"
PUZZLE_HTML_2_FILE = "./descriptions/html%d_part2.html"
PUZZLE_MARKDOWN_2_FILE = "./descriptions/markdown%d_part2.md"
PUZZLE_DATA_FILE = "./data/puzzle%d.dat"

dbg_forcereload = True

def get_article(day):
    if path.exists(PUZZLE_HTML_FILE % day):
        with open (PUZZLE_HTML_FILE % day) as f:
            return f.read()
    print("httping")
    http = Http()
    content = http.request(AOC_URL + str(day))
    html_content = content[1].decode()
    soup = BeautifulSoup(html_content, 'html.parser')
    for article in soup.find_all('article'):
        html = article.prettify( formatter="html" )
        with open(PUZZLE_HTML_FILE % day, "w") as f:
            f.write(html)
        return html
    
def get_markdown(day, article):
    if path.exists(PUZZLE_MARKDOWN_FILE % day):
        with open (PUZZLE_MARKDOWN_FILE % day) as f:
            return f.read()
    print("httping")

    # generate markdown 
    parser = AoCParser()
    parser.feed(article)
    print("parsing")
    markdown = parser.out
    with open(PUZZLE_MARKDOWN_FILE % day, "w") as f:
        f.write(markdown)

        
def get_markdown2(puzzle):
    if path.exists(PUZZLE_MARKDOWN_2_FILE % day):
        with open (PUZZLE_MARKDOWN_2_FILE % day) as f:
            return f.read()
    print("httping")

    # check if html is in place
    if not path.exists(PUZZLE_HTML_2_FILE % day):
        print("please place ")
    
    with open (PUZZLE_HTML_2_FILE % day) as f:
        article= f.read()    
    # generate markdown 
    parser = AoCParser()
    parser.feed(article)
    print("parsing")
    markdown = parser.out
    with open(PUZZLE_MARKDOWN_2_FILE % day, "w") as f:
        f.write(markdown)


def get_data(day):
    puzzle_file = PUZZLE_DATA_FILE % day
    if path.exists(puzzle_file):
        with open (puzzle_file) as f:
            return f.read().splitlines()
    else:
        text = """Note: Puzzle inputs differ by user
Place your puzzle in a file %s in the data folder""" % puzzle_file
        print(text)
        return text
  
   
def get_puzzle(day, debug=False):
    
    # article - the html
    # markdown - printable on the Ipython notebook cell
    # data - (Puzzle inputs differ by user) 
    #        place your puzzle in a file named data/puzzle<day>.dat 
    article = get_article(day)
    markdown = get_markdown(day, article)
    data = get_data(day)
    
    return SimpleNamespace (**{'day': day, 'article':article, 'markdown':markdown, "data" : data} )

def show_puzzle(puzzle, debug=False) :
    display_markdown(puzzle.markdown, raw=True)

def show_puzzle_step2(puzzle, debug=False):
    markdown = get_markdown2(day)
    display_markdown(puzzle.markdown, raw=True)
    


class AoCParser(HTMLParser):
    # converts HTML to Markdown according to:
    # https://www.markdownguide.org/basic-syntax/#code

    def __init__(self, debug=False):
        super(AoCParser, self).__init__()
        self.stack = []
        self.out = ""
        self.buffer = ""
        self.codebuffer = ""
        self.dbg = debug
        self.link = ""
        self.multilinecode = False
    
    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        if self.dbg:
            print("Encountered a start tag:", tag)
            print (self.stack)
            print(attrs)
        if tag == "li":
            self.buffer += "+ "
        elif tag == "h2":
            self.buffer += "## "
        elif tag == "code":
            self.codebuffer += "`"
        elif tag == "em":
            if "code" not in self.stack:
                    self.buffer += " **"                   
       
        elif tag == "a":
            self.link = dict(attrs)["href"]
            self.buffer += " [" 

    def handle_endtag(self, tag):
        assert tag == self.stack.pop()
        
        if tag == "h2" or tag == "p" or tag == "pre" :
            self.buffer += "\n\n"
            
        elif tag == "li":
            self.buffer += "\n"
            
        elif tag == "ul":
            self.buffer += "\n"

        elif tag == "code":
            if self.multilinecode:
                # horrible code to fix some issue when the first chars of a code block are numbers
                # not sure about the reason though. this just fixes it
                self.codebuffer="```\n " + "\n ".join(self.codebuffer[1:].splitlines()) + "\n\n```"
                self.multilinecode = False
            else:
                self.codebuffer += "`"    
            self.buffer += self.codebuffer
            self.codebuffer =""

        elif tag == "em":
            if "code" not in self.stack:
                self.buffer += "** "    
            
        elif tag == "a":
            self.buffer += "](" + self.link + ") "
            self.link = ""
            
        if len(self.stack)==1:
            self.out += self.buffer + "\n"
            self.buffer = ""
            
        if self.dbg:
            print("Encountered an end tag :", tag)
            print("Stack :", self.stack)

    def handle_data(self, data):
        if len(self.stack) == 0:
            # we are at root of article
            return

        if self.stack[-1] == "code" and data.find("\n"):
            self.multilinecode =True
            self.codebuffer += data
        else:
            self.buffer += data.strip()

        
        if self.dbg:
            print("last tag: " + self.stack[-1] + "  Encountered some data  :", data)

