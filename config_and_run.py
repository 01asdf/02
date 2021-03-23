import sys, getopt
import adatok
import vezerlo
import teszt

try:
    opts, args = getopt.getopt(sys.argv[1:],'h:d:m:n:c:')
except getopt.GetoptError:
    print('Usage: config_and_run.py -d <dataset> -m <model> -n <number of users> -c <0:dinamic labeling from labeling.py, anything else: use config<number>.txt>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('Usage: config_and_run.py --dataset <dataset> --model <model> -n <number of users> -c <0:dinamic labeling from labeling.py, anything else: use config<number>.txt> ')
        sys.exit()

    elif opt == '-d':
        adatok.data.dataset=arg
    elif opt == '-m':
        adatok.data.model = arg
    elif opt == '-n':
        adatok.data.num_users= int(arg)
    elif opt == '-c':
        adatok.data.config_number = int(arg)
    else:
        continue
vezerlo.main()
