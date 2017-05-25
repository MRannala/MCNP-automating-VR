# MCNP-automating-VR
Scripts developed to automate MCNP VR approaches 
This file is generated to take a starting input file (in the form of a .i file) 
and generating iterartions for a ww VR approach.

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
- CTME You_get_what_Im_driving_at_here.i

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
- More than one line is used in the CTME file,
- No .i or file beginning with CTME is found.

N.B.
It is important that you have a clear understanding and have studied the strategy to be used with
regards to time steps and the weighting regime being used. This script is not intended to replace
good diligent working practices. It is merely intended to overcome the tedium of repeating the same
process for similar models once a strategy has been developed.
