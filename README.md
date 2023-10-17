# blending_fv3

build each of the four fortan utility codes under blending_fv3/src
    1) chgres_winds - for rotating the winds
    2) raymond      - Raymond filter
    3) remap_dwinds - vertically remap the winds
    4) remap_scalar - vertically remap scalars

There is a make file provided for each of these tools. They are built using f2py3.8 so python version 3.8 is required. I've also built it with 3.9, so I'm sure other will work too. You will also have to provide the path to libiomp5.s for each of the utilities.

Then link the resulting .so file (e.g., chgres_winds.cpython-38-x86_64-linux-gnu.so) to the blending_fv3/. directory.

There is a run.sh driver script which you can follow along with for how to run the tool.

For using as stand alone tool for converting cold2warmstarts, you still need to run da_blending_fv3.py, but you can set blend = False and use_host_EnKF = True.
