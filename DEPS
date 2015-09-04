# The only dependency is chromium source

vars = {
  'chromium_git': 'https://chromium.googlesource.com',
  'chromium_rev': 'master', #'b614f6981808ab7a8ae18795dfcb58f1e6eed8aa', #'d2d9fe0f',
  'tarc_git' : 'https://github.com/tarc',
  'swarming_revision': '2866a22530cb65feae5d9f64c83636aed5391d06',
  'v8_revision': '738e9567a03bc7530d46a8e5025b7f271003fae9',
}

deps = {
  'src/chromium/':
    Var('chromium_git') + '/chromium/src' + '@' + Var('chromium_rev'),

  'src/chromium/tools/gyp':
    Var('tarc_git') + '/gyp.git' + '@' + 'master',

  'src/chromium/third_party/icu':
    Var('chromium_git') + '/chromium/deps/icu.git' + '@' +
      '6b3ce817f8e828c3b7a577d2395f0882eb56ef18',

  'src/chromium/tools/grit':
    Var('chromium_git') + '/external/grit-i18n.git' + '@' +
      '15d48e32cc9f346245c823ce48c54209d02ea983', # from svn revision 196

  'src/chromium/v8':
    Var('chromium_git') + '/v8/v8.git' + '@' +  Var('v8_revision'),

  'src/chromium/testing/gtest':
    Var('chromium_git') + '/external/googletest.git' + '@' +
      '9855a87157778d39b95eccfb201a9dc90f6d61c6', # from svn revision 746

  'src/chromium/testing/gmock':
    Var('chromium_git') + '/external/googlemock.git' + '@' +
      '0421b6f358139f02e102c9c332ce19a33faf75be', # from svn revision 566

  'src/chromium/tools/swarming_client':
    Var('chromium_git') + '/external/swarming.client.git' + '@' +
      Var('swarming_revision'),

}

hooks = [
  {
    # A change to a .gyp, .gypi, or to GYP itself should run the generator.
    'name': 'gyp',
    'pattern': '.',
    'action': ['python', 'src/build/gyp_chromium.py'],
  },
]
