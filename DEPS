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

  'src/chromium/third_party/icu':
   Var('chromium_git') + '/chromium/deps/icu52.git' + '@' + '8ac906faf7b66180f2208380c35ae1e07136c5cc', # from svn revision 292317

  'src/chromium/tools/grit':
    Var('chromium_git') + '/external/grit-i18n.git' + '@' + '740badd5e3e44434a9a47b5d16749daac1e8ea80', # from svn revision 176

}

hooks = [
  {
    # A change to a .gyp, .gypi, or to GYP itself should run the generator.
    'name': 'gyp',
    'pattern': '.',
    'action': ['python', 'src/chromium/build/gyp_chromium'],
  },
]
