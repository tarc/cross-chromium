# The only dependency is chromium source

vars = {
  'chromium_git': 'https://chromium.googlesource.com',
  'chromium_rev': 'b614f6981808ab7a8ae18795dfcb58f1e6eed8aa', #'d2d9fe0f', 'master'
  'tarc_git' : 'https://github.com/tarc',
  'swarming_revision': 'c28b74ff7a2678b611f4a7ecb3be4f99f15a76fd',
  'v8_revision': 'd766d7d1a1bf33a4b70d194029a8de817135f4ff', # from svn revision 24578
}

deps = {
  'src/chromium/':
    Var('chromium_git') + '/chromium/src' + '@' + Var('chromium_rev'),

  'src/chromium/tools/gyp':
    Var('tarc_git') + '/gyp.git' + '@' + 'master',

  'src/chromium/third_party/icu':
    Var('chromium_git') + '/chromium/deps/icu52.git' + '@' +
      '8ac906faf7b66180f2208380c35ae1e07136c5cc', # from svn revision 292317

  'src/chromium/tools/grit':
    Var('chromium_git') + '/external/grit-i18n.git' + '@' +
      '740badd5e3e44434a9a47b5d16749daac1e8ea80', # from svn revision 176

  'src/chromium/v8':
    Var('chromium_git') + '/v8/v8.git' + '@' +  Var('v8_revision'),

  'src/chromium/testing/gtest':
    Var('chromium_git') + '/external/googletest.git' + '@' +
      '9855a87157778d39b95eccfb201a9dc90f6d61c6', # from svn revision 746

  'src/chromium/testing/gmock':
    Var('chromium_git') + '/external/googlemock.git' + '@' +
      '896ba0e03f520fb9b6ed582bde2bd00847e3c3f2', # from svn revision 485

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
