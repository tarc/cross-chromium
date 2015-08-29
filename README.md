# cross-chromium 

To checkout, instead of just clonin issue the following:

    mkdir cross-chromium
    cd cross-chromium
    gclient config --name src https://github.com/tarc/cross-chromium.git@master
    gclient sync --no-history
