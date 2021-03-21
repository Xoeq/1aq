try:
    import simple_pastebin_parser as spp
except ModuleNotFoundError:
    print("You didn't read the manual!")
    print()
    print("to use this script, you need to install simple_pastebin_parser with: `sudo pip3 install simple_pastebin_parser --no-deps`")
    exit(1)
 
if "/i/" not in spp.KNOWN_PREFIXES:
    spp.KNOWN_PREFIXES.append("/i/")
 
import re,argparse,sys,pickle,hashlib
 
def setunk(strang,unkstr="unknown"):
    if (strang == ""):
        return unkstr
    return strang
 
def contains(strang,search):
    for word in search:
        if word in strang:
            return True
    return False
 
def contains_regex(strang,search):
    for regex in search:
        if re.match(regex,strang):
            return True
    return False
 
class pbPaste:
    def __init__(self,paste):
        self.title = setunk(paste.Title,"Untitled")
        self.author = setunk(paste.Author,"Unknown Author")
        self.date = paste.Date
        self.content = paste.Content.replace("\r\n","\n")
        self.hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        self.id = paste.id
 
def get_one_paste():
    for paste in spp.get_pastes():
        return pbPaste(paste)
 
def main(SEARCH=[""],verbose=True,output="",save=False):
    if output:
        append_write = "w"
        if save:
            append_write = "a"
        outfile = open(output,append_write,newline="\n")
    if (save and output):
        try:
            paste_array = pickle.load(open(output+".pickle","rb"))
        except FileNotFoundError:
            paste_array = []
    else:
        paste_array = []
    try:
        for paste in spp.get_pastes():
            current = pbPaste(paste)
            skip = False
            for prev_paste in paste_array:
                if current.hash == prev_paste:
                    skip = True
                    break
            if (contains_regex(current.title,SEARCH) or contains_regex(current.content,SEARCH)) and (not skip):
                paste_array.append(current.hash)
                title_len = 27+4+len(current.title)
                outstr = ""
                outstr += "="*title_len+"\n"*2
                outstr += "  found corresponding paste: "+current.title+"\n"*2
                outstr += title_len*"-"+"\n"*2
                outstr += current.content+"\n"*2
                outstr += title_len*"="+"\n"*5
                if verbose:
                    print(outstr,end="")
                if output:
                    outfile.write(outstr)
        if output:
            outfile.close()
            print("Human-readable data saved as "+output)
            if save:
                pickle.dump(paste_array,open(output+".pickle","wb"))
                print("Pickles available here: "+output+".pickle")
        return 0
    except KeyboardInterrupt:
        print("\nSearch stopped by user.")
        if output:
            outfile.close()
            print("Human-readable data saved as "+output)
            if save:
                pickle.dump(paste_array,open(output+".pickle","wb"))
                print("Pickles available here: "+output+".pickle")
        return 1
    except:
        if output:
            outfile.close()
            print("Human-readable data saved as "+output)
            if save:
                pickle.dump(paste_array,open(output+".pickle","wb"))
                print("Pickles available here: "+output+".pickle")
        raise
 
 
if __name__ == "__main__":
    print("Started pastebin scraper")
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="display gathered data in terminal", action="store_true")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-r", "--regex", help="regular expression to match")
    parser.add_argument("-p", "--pickle", help="adds a file to save pickled data", action="store_true")
    args = parser.parse_args()
    arg_regex = ""
    if (args.regex):
        arg_regex = args.regex
    exit_value = main(output=args.output,verbose=args.verbose,SEARCH=[arg_regex],save=args.pickle)
    sys.exit(exit_value)
