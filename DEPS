# The only dependency is chromium source

vars = {
  'chromium_git': 'https://chromium.googlesource.com',
  'tarc_git' : 'https://github.com/tarc',
}

deps = {
  'src/chromium/':
    Var('chromium_git') + '/chromium/src' + '@b614f6981808ab7a8ae18795dfcb58f1e6eed8aa'

  'src/chromium/tools/gyp':
    Var('tarc_git') + '/gyp.git' + '@' + 'master',
}

hooks = [
  {
    # A change to a .gyp, .gypi, or to GYP itself should run the generator.
    'name': 'gyp',
    'pattern': '.',
    'action': ['python', 'src/chromium/build/gyp_chromium'],
  },
]
