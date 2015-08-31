# The only dependency is chromium source

vars = {
  'chromium_git': 'https://chromium.googlesource.com',
  'tarc_git' : 'https://github.com/tarc',
  'v8_revision': '738e9567a03bc7530d46a8e5025b7f271003fae9',
}

deps = {
  'src/chromium/':
    Var('chromium_git') + '/chromium/src' + '@' + 'master',

  'src/chromium/tools/gyp':
    Var('tarc_git') + '/gyp.git' + '@' + 'master',

  'src/chromium/third_party/icu':
    Var('chromium_git') + '/chromium/deps/icu.git' + '@' + '6b3ce817f8e828c3b7a577d2395f0882eb56ef18',

  'src/chromium/tools/grit':
    Var('chromium_git') + '/external/grit-i18n.git' + '@' + '15d48e32cc9f346245c823ce48c54209d02ea983', # from svn revision 196

  'src/chromium/v8':
    Var('chromium_git') + '/v8/v8.git' + '@' +  Var('v8_revision'),

}

hooks = [
  {
    # A change to a .gyp, .gypi, or to GYP itself should run the generator.
    'name': 'gyp',
    'pattern': '.',
    'action': ['python', 'src/build/gyp_chromium.py'],
  },
]
