# The only dependency is chromium source

vars = {
  'chromium_git': 'https://chromium.googlesource.com',
  'tarc_git' : 'https://github.com/tarc',
}

deps = {
  'src/chromium/':
    Var('chromium_git') + '/chromium/src' + '@' + 'master',

  'src/chromium/tools/gyp':
    Var('tarc_git') + '/gyp.git' + '@' + 'master',

  'src/chromium/third_party/icu':
    Var('chromium_git') + '/chromium/deps/icu.git' + '@' + '6b3ce817f8e828c3b7a577d2395f0882eb56ef18',
}

hooks = [
  {
    # A change to a .gyp, .gypi, or to GYP itself should run the generator.
    'name': 'gyp',
    'pattern': '.',
    'action': ['python', 'src/chromium/build/gyp_chromium'],
  },
]
