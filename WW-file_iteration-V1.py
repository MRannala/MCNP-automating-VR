# -*- coding: utf-8 -*-
"""
@author: J. M. Rannala
README explaination:
This file is generated to take a starting MCNP input file (in the form of a .i file) 
and generating iterartions for a WW VR approach.

The initial file should be named without appended number i.e. File_1_other_options.i
This should also contain its own imp/wwn map (i.e. no initial .e file required).

The first process is to run the initial file which should in turn generate a 
corresponding .e file.

A second .i file will be generated i.e. File_1_other_options-1.i and this will be 
run with the .e file generated in the initial run. This will be repeated based on 
the number of entries in the used specified CTME file. 

--- The CTME file ---

The CTME file is a user generated file (such as a .txt file) whose file name MUST start 
with CTME (upper case) e.g. 
- CTME.txt, 
- CTME-lets_try_this_name.ctme, 
- CTME You_get_what_Im_driving_at_here.n

This file should contain the CTMEs you want for each of the iterations files and these should 
be space deliminated. E.g.
5 10 20 20 40 360

This would lead to the second iteration running for 5 minutes of computer time, 3rd 10mins,
4th and 5th 20 mins, 6th 40 mins, 7th 360mins.

An exception (error) will be returned if more than a single line is used.

A batch file will also be generated which can be used to run, both the initial run and all 
subsequent iterations.

--- Exceptions ---

An exception (an error) will be raised if:
- There is more than one .i in the directory,
- More than one file starting with CTME is present in the directory,
- More than one line is used in the CTME file,
- No .i or file beginning with CTME is found.
- No file starting with CTME is present.

N.B.
It is important that you have a clear understanding and have studied the strategy to be used with
regards to time steps and the weighting regime being used. This script is not intended to replace
good diligent working practices. It is merely intended to overcome the tedium of repeating the same
process for similar models once a strategy has been developed.
"""
import os

def create_array(afile) :
    
    data = []
    
    for line in afile:
        data.append(line)
    
    return data

def get_iterations():
    
    # Specify file type
    filetype = "CTME"
    
    # Get current working directory (cwd)
    cwd = os.getcwd()
    
    iters = []
    
    for file in os.listdir(cwd):
        if file.startswith(filetype):
            afile = open(file, 'r')
    
    # Read ctme iterations to be used
    data = create_array(afile)
        
    if len(data)  > 1:
        print("Warning file length > then single line!")
    elif len(data) == 0:
        print("No iterations found!")
    else:
        iters = data[0].split()
    
    afile.close()
    
    return iters
    

def get_ifile():
    
    filelist = []
    
    # Specify file type
    filetype = ".i"
    
    # Get current working directory (cwd)
    cwd = os.getcwd()
    
    for file in os.listdir(cwd):
        if file.endswith(filetype):
            filelist.append(file)

    if len(filelist) == 0:
        print("No {0} type file found! \nScript terminated!".format(filetype))
        #Quit
    elif len(filelist) > 1:
        print("More than one {0} type file found! \nScript terminated!".format(filetype))
        #Quit
    
    ifile = open(filelist[0],'r')
        
    return ifile, ifile.name
       
def find_X(data, var):
    
    for i in range(len(data)):
        linetext = data[i].split()
        if len(linetext) > 0:
            if linetext[0].lower().startswith(var):
                v_index = i
                
    return v_index
    
def create_batch(filename, number):
    
    # batch file name
    b_name = filename + '.bat'
    
    # create batch file
    bfile = open(b_name,'w')
    
    string = str('@ set MCNPPATH=C:\Apps\MY_MCNP\MCNP_CODE\bin ')
    bfile.write('setlocal enabledelayedexpansion \n')
    bfile.write('@ set MCNPPATH=C:\Apps\MY_MCNP\MCNP_CODE\\bin ')
    bfile.write('@ PATH %MCNPPATH%;%PATH% \n')
    bfile.write('MCNP6 i={0}.i n={0}-0. tasks 11 \n'.format(filename))
    bfile.write('SET filename=' + filename + '-\n')
    bfile.write('FOR /L %%A in (1,1,{0}) DO ( \n'.format(number-1))
    bfile.write('    SET /a "B=%%A-1" \n')
    bfile.write('	MCNP6 i=%filename%%%A.i wwinp=%filename%!B!.e n=%filename%%%A. tasks 11 )')
    
    bfile.close()
    
    
if __name__ == "__main__":
    
    # Get list of Ctme times from external file  starting with CTME-Iteration"
    times = get_iterations()
    
    # find and open .i type file and save filename core
    ifile, f_name = get_ifile()
     
    # import .i file to array
    datarray = create_array(ifile)
     
    # Close ifile
    ifile.close()
    
    #find index of wwp: line
    wwp_line = find_X(datarray, 'wwp')
    
    #find index of CTME line
    t_line = find_X(datarray, 'ctme')
    
    # for each time interval
    for i in range(len(times)):
        
        filename = f_name.rstrip('.i') + '-{0}'.format(i) + '.i'
        
        # change the wwp line to accept .e files
        linetext = datarray[wwp_line].split()
        linetext[5] = -1
        dline = ' '.join(str(x) for x in linetext)
        datarray[wwp_line] = dline + '\n'

        # change the ctme line 
        datarray[t_line] = "ctme {0} \n".format(times[i])
        
        # create new file
        ofile = open(filename, 'w')
        
        # write array to new ofile
        for j in range(len(datarray)):
            ofile.write(datarray[j])
            
        # close ofile    
        ofile.close()        
     
# $$$
    print(len(times))
        
    # Create batch file to run
    create_batch(f_name.rstrip('.i'), len(times))
     