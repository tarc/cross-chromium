# And I try, and I try...

{
  'variables': {
    # A hook that can be overridden in other repositories to add additional
    # compilation targets to 'All'.
    'app_targets%': [],
    # For Android-specific targets.
    'android_app_targets%': [],
  },
  'targets': [
    {
      'target_name': 'All',
      'type': 'none',
      'xcode_create_dependents_test_runner': 1,
      'dependencies': [
        '<@(app_targets)',
        '<(DEPTH)/build/some.gyp:*',
        '<(DEPTH)/base/base.gyp:*',
#        '<(DEPTH)/components/components.gyp:*',
#				'../third_party/WebKit/public/blink.gyp:blink_minimal'
        ]
    }
  ]
}

