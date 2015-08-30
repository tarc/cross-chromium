# cross-chromium 

To checkout instead of just cloning, prefer the following:

    mkdir cross-chromium
    cd cross-chromium
    gclient config --name src https://github.com/tarc/cross-chromium.git@master
    gclient sync --no-history

The `--no-history` options tells `gclient sync` to perform a shallow clone of the required repositories - that is, call `git clone` with `--depth=1`. It's possible aftwards to deepen these clones with:

    git fetch --unshallow
