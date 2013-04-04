import sys, csv
import binascii, cgi
    
def get_files():
    # TODO: Support mutliple input files when a wildcarded name is suplied.
    
    ouf = None
    inf = None
    if len(sys.argv) > 3:
        print "Unknown options %s" % sys.argv[3:]
        sys.exit()
    if len(sys.argv) >= 3:
        oufname = sys.argv[2]
        ouf = open(oufname,'w')
    if len(sys.argv) >= 2:
        infname = sys.argv[1]
        inf = open(infname)
    if len(sys.argv) <= 1:
        print "Supply an input file."
        print " Usage:  report.py <infile> <outfile>"
        sys.exit()
    return (inf, ouf)

def simplify(text):
    # ignore trailing/leading spaces    
    simp = text.strip()
    # case insensitive
    simp = simp.lower()
    # ignore final period or ! or ?
    while True:
        if len(simp) > 1 and simp[-1] in ['.','?','!']:
            simp = simp[:-1]
        else:
            break
    # common spellings.
    if 'dewali' in simp:
        simp = simp.replace('dewali','diwali')
    if 'Deewali' in simp:
        simp = simp.replace('Deewali','diwali')        
    if 'i love u' in simp:
        simp = simp.replace('i love u','i love you')
    return simp


def translate(row):
    url = row[0]
    pageviews = int(row[1])

    parms = {}
    if '?' in url:
        querystring = url.split('?')[1]
        parms = cgi.parse_qs(querystring)

    text = "Awesome!"
    if 'h' in parms:
        hexstr = parms['h'][0]
        if len(hexstr) % 2 == 1:
            hexstr = hexstr[:-1]
        text = binascii.unhexlify( hexstr )
    elif 't' in parms:
        text = parms['t'][0]

    simple_text = simplify(text)

    return (simple_text, text, url, pageviews)

def main(): 
    inf, ouf = get_files()
    
    cr = csv.reader(inf)
    
    data = {}
    totals = {}
    
    inside_table = False
    for row in cr:
        if inside_table and len(row) >= 2:
            simple_text, text, url, count = translate(row)
            data.setdefault(simple_text,[])
            data[simple_text].append( [text, url, count] )
            totals.setdefault(simple_text, 0)
            totals[simple_text] += count
        
        if len(row) >= 2 and row[0] == "Page" and row[1] == "Pageviews":
            inside_table=True
    
    total_list = totals.items()
    total_list.sort( lambda x,y : cmp(y[1],x[1]))
    
    if ouf is None:
        # No file to write to.
        for simple_text, count in total_list[:100]:
            urls = data[simple_text]
            urls.sort( lambda x,y: cmp(y[2],x[2]) )
            print "%s,%s" % (urls[0][0], count)
    else:
        outcsv = csv.writer(ouf)
        outcsv.writerow(["Text","Count","Variants","Details"])
        for simple_text, count in total_list:
            urls = data[simple_text]
            urls.sort( lambda x,y: cmp(y[2],x[2]) )            
            outcsv.writerow([urls[0][0], count, len(urls), str(urls) ])
        ouf.close()
    
if __name__ == '__main__':
    main()