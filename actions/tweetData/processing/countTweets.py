



def countTweets(fileStream):
    count = 0;
    for line in fileStream:
        count = count + 1

    return count

if __name__ == '__main__':
    fileStream = -1
    try:
        opts, args = getopt.getopt(args, 'hf:',['file='])
    except getopt.GetoptError:
        print 'Usage: $ python getSomeTweets.py -f <num_days_from_start>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: $ python getSomeTweets.py -f <num_days_from_start>'
        elif opt in ('-f', '--days'):
            arg = int(float(arg))
            days = arg
    countTweets
