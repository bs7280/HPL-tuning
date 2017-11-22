#from subprocess import call, check_call
import subprocess
import re
from jinja2 import Environment, FileSystemLoader
import os
import signal
import subprocess
import time
import csv
from gridParams import getParams
import datetime

def createConfigFile(path,Ns_value,NB_value,LD=1,BC=3,PF=2,LF=2,verbose=False):
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template('HPL.template')
    output_from_parsed_template = template.render(
            Ns=str(Ns_value),
            NB=NB_value,
            LD=LD,
            BC=BC,
            PF=PF,
            LF=LF
            )

    if verbose:
        print output_from_parsed_template

    # to save the results
    with open(path+"HPL.dat", "wb") as fh:
        fh.write(output_from_parsed_template)

def run(xhpl_path, parse=False, verbose=False, early_termination=False, thresh=0.5):
	"""xhpl is full path to xhpl executable"""
	starttime = datetime.datetime.now()

        # If using early termination then parsing line by line must also be enabled
        if early_termination == True:
            parse=True

        # Command to run HPL
        hpl_command = ["mpirun","-np","20","./xhpl"]

        # Run command so it can be read by python (else, just run and return output which
        # would effectively make this script a wrapper around HPL using a template for
        # HPL.dat)
        if parse:
            # Run command with location of ./xhpl as path
	    ps = subprocess.Popen(hpl_command,stdout=subprocess.PIPE, cwd=xhpl_path)

            # Used to bundle all lines up back into one string in order to grep the output to get
            # the overall flops
            program_output = []

	    if early_termination:
		    # loop through output of process
		    for l in iter(ps.stdout.readline, b''):
			# String \n
			line = l.rstrip()

			# Add line to program output 
			program_output.append(line)

			if verbose:
			    print line
			
			# Looks only at lines that show progress of linpack run
			if "Gflops=" in line:
			    frac_key = "Fraction="
			    flop_key = "Gflops="

			    # Gets the percent complete as a float
			    fraction = float(line[line.find(frac_key)+len(frac_key):].split("%")[0])

			    # Gets the current gflops as a int
			    gflops = line[line.find(flop_key)+len(flop_key):]
			    gflops = gflops.split("e+")
			    gflops = float(gflops[0]) * (10**int(gflops[1]))

			    #print fraction,gflops

			    if int(fraction) == fraction:
				print fraction,gflops

			    if early_termination and fraction >=thresh:
				# Send sigint to process 
				ps.send_signal(2)

				# prints flops
				print gflops
				
				# get walltime
				wt = (datetime.datetime.now() - starttime).seconds			

				# return None,gflops (None is in place for walltime)
				return wt,gflops


	    out = subprocess.check_output(["grep", "WR03R2R2"], stdin=ps.stdout)
	    ps.wait()

            tmp = re.sub("\s+",",",out.split("\n")[0]).split(",")[5:]

            walltime = tmp[0]
            gflops = tmp[1]
            gflops = gflops.split("e+")
            gflops = float(gflops[0]) * (10**int(gflops[1]))
            results = (float(walltime),gflops)

	    return tuple(results)
        else:
            out = subprocess.check_output(hpl_command,cwd=xhpl_path)
            print out

#hpl_path = "spack/opt/spack/linux-clear_linux_os17920-x86_64/intel-18.0.0/hpl-2.2-2egogfet37vqtbwkd5dqq66hvm366rmi/bin/"
hpl_path = "HPL/"

#def createConfigFile(path,Ns_value,NB_value,LD=1,BC=3,PF=2,LF=2,verbose=False):
#createConfigFile(hpl_path,64000,240)
#walltime,flops = run(hpl_path,parse=True, early_termination=True)


def grid(params,verbose=False):
    results = [["NB","NS","wt","gflops"]]
    ts = time.strftime("%Y%m%d-%H%M%S")

    for p in params:
	NS=p[0]
	nb=p[1]
	try:
		#NS = (ns_exp)*1000
		createConfigFile(hpl_path,NS,nb) #,1,1,2,1)
		walltime,flops = run(hpl_path,parse=True,early_termination=False,verbose=verbose,thresh=10.0)

		print "NB: " + str(nb) + " NS: " + str(NS) + " hpl_results: " + str(flops) + " GFLOPS (walltime " + str(walltime) + "s)"

		results.append((nb,NS,walltime,flops))

		# Sleep for 10 seconds to give OS a chance to clean
		time.sleep(15)
	except:
		# record error
		print "error"+str(NS)+", "+str(nb)
		results.append((nb,NS,False,False))

		# Sleep for 5 minutes to give the OS a change to get it's life together
		time.sleep(60*5)

	# Write to file

	with open("hpl_experiment_basic_"+str(ts),"w") as f:
		writer = csv.writer(f)
		writer.writerows(results)



    # Write results to disk

    print
    print "Best: "
    print list(max(results[1:], key=lambda x: x[-1]))


def second_grid():
    results = [["NB","NS","LD","BC","PF","LF","wt","gflops"]]

    for LD in range(0,3):
        for BC in range(0,6):
            for PF in range(0,3):
                for LF in range(0,3):
                    #time.sleep(10)
                    createConfigFile(hpl_path,196000,240,LD,BC,PF,LF)
                    walltime,flops = run(hpl_path,parse=True,early_termination=True,verbose=False,thresh=10.)

                    terms=list(zip(["NB","NS","LD","BC","PF","LF"],list(map(str,[196000,240,LF,BC,PF,LF]))))

                    print terms
                    print str(terms)[1:-1] +" " + str(flops)+" GFLOPS (walltime " + str(walltime) + "s)"

                    results.append((196000,240,LD,BC,PF,LF,walltime,flops))

    print
    print "Best: "
    print list(max(results[1:], key=lambda x: x[-1]))

    # Write results to disk

    import csv
    with open("hpl_experiment","w") as f:
        writer = csv.writer(f)
        writer.writerows(results)

params = getParams((32000,98000,2000),(64,256,8))
grid(params,verbose=True)
