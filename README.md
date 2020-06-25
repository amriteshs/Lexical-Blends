# Lexical-Blends
There are five project files, of which the dictionary, candidate, and blend files form the central data sources for this Project, although the other files may prove to be of interest in some circumstances. The files are described in more detail below:

**dict.txt**: This is a list of approximately 370K English entries, which should comprise the dictionary for your approximate string search method(s). This dictionary is a   slightly-altered version of the data from: https://github.com/dwyl/english-words. The format of this file is one entry per line, in alphabetical order.

**tweets.txt**: This is a list of the text from 62345 tweets, one tweet per line. (The ordering is random.)

**wordforms.txt**: This is an alphabetically-sorted list of 31763 unique tokens present within the tweets. To construct this list, the tweets were separated based on one (or more) characters of whitespace (\s), and tokens not consisting entirely of English alphabetic characters (^[a-zA-Z]+$) were excluded.

**candidates.txt**: This is the list of 16925 tokens present in wordforms.txt, except that any token appearing in the dictionary has been excluded. One logical framework for the problem of finding lexical blends is that any token not present within the dictionary is potentially a blend.

**blends.txt**: This is a tab-delimited list of tokens appearing in the tweets, which have been manually identified as being lexical blends. Each line takes the form: blend token, tab character, component word, tab character, component word, newline. Some of the blends do not appear in the candidates list, because they have been excluded in the preprocessing stage. Some of the tokens in the tweets may be blends that are not listed in blends.txt.
