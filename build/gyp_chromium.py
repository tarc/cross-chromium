#!/usr/bin/env python

# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This script is wrapper for Chromium that adds some support for how GYP
# is invoked by Chromium beyond what can be done in the gclient hooks.

import glob
import os
import re
import shlex
import subprocess
import string
import sys

script_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
chrome_src = os.path.abspath(os.path.join(script_dir, os.pardir))

chrome_src = os.path.join ( chrome_src , 'chromium' )
chrome_script_dir = os.path.join ( chrome_src , 'build' )

sys.path.insert(0, os.path.join(chrome_src, 'tools', 'gyp', 'pylib'))
import gyp

# Assume this file is in a one-level-deep subdirectory of the source root.
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(1, script_dir)
import compiler_version

sys.path.insert(1, os.path.join(chrome_src, 'build'))
import gyp_environment
import vs_toolchain

# Add paths so that pymod_do_main(...) can import files.
sys.path.insert(1, os.path.join(chrome_src, 'build', 'android', 'gyp'))
sys.path.insert(1, os.path.join(chrome_src, 'tools'))
sys.path.insert(1, os.path.join(chrome_src, 'tools', 'generate_shim_headers'))
sys.path.insert(1, os.path.join(chrome_src, 'tools', 'grit'))
sys.path.insert(1, os.path.join(chrome_src, 'chrome', 'tools', 'build'))
sys.path.insert(1, os.path.join(chrome_src, 'chromecast', 'tools', 'build'))
sys.path.insert(1, os.path.join(chrome_src, 'native_client', 'build'))
sys.path.insert(1, os.path.join(chrome_src, 'native_client_sdk', 'src',
    'build_tools'))
sys.path.insert(1, os.path.join(chrome_src, 'remoting', 'tools', 'build'))
sys.path.insert(1, os.path.join(chrome_src, 'third_party', 'liblouis'))
sys.path.insert(1, os.path.join(chrome_src, 'third_party', 'WebKit',
    'Source', 'build', 'scripts'))

# On Windows, Psyco shortens warm runs of build/gyp_chromium by about
# 20 seconds on a z600 machine with 12 GB of RAM, from 90 down to 70
# seconds.  Conversely, memory usage of build/gyp_chromium with Psyco
# maxes out at about 158 MB vs. 132 MB without it.
#
# Psyco uses native libraries, so we need to load a different
# installation depending on which OS we are running under. It has not
# been tested whether using Psyco on our Mac and Linux builds is worth
# it (the GYP running time is a lot shorter, so the JIT startup cost
# may not be worth it).
if sys.platform == 'win32':
  try:
    sys.path.insert(0, os.path.join(chrome_src, 'third_party', 'psyco_win32'))
    import psyco
  except:
    psyco = None
else:
  psyco = None


def GetSupplementalFiles():
  """Returns a list of the supplemental files that are included in all GYP
  sources."""
  return glob.glob(os.path.join(chrome_src, '*', 'supplement.gypi'))


def ProcessGypDefinesItems(items):
  """Converts a list of strings to a list of key-value pairs."""
  result = []
  for item in items:
    tokens = item.split('=', 1)
    # Some GYP variables have hyphens, which we don't support.
    if len(tokens) == 2:
      result += [(tokens[0], tokens[1])]
    else:
      # No value supplied, treat it as a boolean and set it. Note that we
      # use the string '1' here so we have a consistent definition whether
      # you do 'foo=1' or 'foo'.
      result += [(tokens[0], '1')]
  return result


def GetGypVars(supplemental_files):
  """Returns a dictionary of all GYP vars."""
  # Find the .gyp directory in the user's home directory.
  home_dot_gyp = os.environ.get('GYP_CONFIG_DIR', None)
  if home_dot_gyp:
    home_dot_gyp = os.path.expanduser(home_dot_gyp)
  if not home_dot_gyp:
    home_vars = ['HOME']
    if sys.platform in ('cygwin', 'win32'):
      home_vars.append('USERPROFILE')
    for home_var in home_vars:
      home = os.getenv(home_var)
      if home != None:
        home_dot_gyp = os.path.join(home, '.gyp')
        if not os.path.exists(home_dot_gyp):
          home_dot_gyp = None
        else:
          break

  if home_dot_gyp:
    include_gypi = os.path.join(home_dot_gyp, "include.gypi")
    if os.path.exists(include_gypi):
      supplemental_files += [include_gypi]

  # GYP defines from the supplemental.gypi files.
  supp_items = []
  for supplement in supplemental_files:
    with open(supplement, 'r') as f:
      try:
        file_data = eval(f.read(), {'__builtins__': None}, None)
      except SyntaxError, e:
        e.filename = os.path.abspath(supplement)
        raise
      variables = file_data.get('variables', [])
      for v in variables:
        supp_items += [(v, str(variables[v]))]

  # GYP defines from the environment.
  env_items = ProcessGypDefinesItems(
      shlex.split(os.environ.get('GYP_DEFINES', '')))

  # GYP defines from the command line. We can't use optparse since we want
  # to ignore all arguments other than "-D".
  cmdline_input_items = []
  for i in range(len(sys.argv))[1:]:
    if sys.argv[i].startswith('-D'):
      if sys.argv[i] == '-D' and i + 1 < len(sys.argv):
        cmdline_input_items += [sys.argv[i + 1]]
      elif len(sys.argv[i]) > 2:
        cmdline_input_items += [sys.argv[i][2:]]
  cmdline_items = ProcessGypDefinesItems(cmdline_input_items)

  vars_dict = dict(supp_items + env_items + cmdline_items)
  return vars_dict


def GetOutputDirectory():
  """Returns the output directory that GYP will use."""
  # GYP generator flags from the command line. We can't use optparse since we
  # want to ignore all arguments other than "-G".
  needle = '-Goutput_dir='
  cmdline_input_items = []
  for item in sys.argv[1:]:
    if item.startswith(needle):
      return item[len(needle):]

  env_items = shlex.split(os.environ.get('GYP_GENERATOR_FLAGS', ''))
  needle = 'output_dir='
  for item in env_items:
    if item.startswith(needle):
      return item[len(needle):]

  return "out"


def additional_include_files(supplemental_files, args=[]):
  """
  Returns a list of additional (.gypi) files to include, without duplicating
  ones that are already specified on the command line. The list of supplemental
  include files is passed in as an argument.
  """
  # Determine the include files specified on the command line.
  # This doesn't cover all the different option formats you can use,
  # but it's mainly intended to avoid duplicating flags on the automatic
  # makefile regeneration which only uses this format.
  specified_includes = set()
  for arg in args:
    if arg.startswith('-I') and len(arg) > 2:
      specified_includes.add(os.path.realpath(arg[2:]))

  result = []
  def AddInclude(path):
    if os.path.realpath(path) not in specified_includes:
      result.append(path)

  # Always include common.gypi.
  AddInclude(os.path.join(script_dir, 'common.gypi'))

  # Optionally add supplemental .gypi files if present.
  for supplement in supplemental_files:
    AddInclude(supplement)

  return result


if __name__ == '__main__':
  # Disabling garbage collection saves about 1 second out of 16 on a Linux
  # z620 workstation. Since this is a short-lived process it's not a problem to
  # leak a few cyclyc references in order to spare the CPU cycles for
  # scanning the heap.
  import gc
  gc.disable()

  args = sys.argv[1:]

  use_analyzer = len(args) and args[0] == '--analyzer'
  if use_analyzer:
    args.pop(0)
    os.environ['GYP_GENERATORS'] = 'analyzer'
    args.append('-Gconfig_path=' + args.pop(0))
    args.append('-Ganalyzer_output_path=' + args.pop(0))

  if int(os.environ.get('GYP_CHROMIUM_NO_ACTION', 0)):
    print 'Skipping gyp_chromium due to GYP_CHROMIUM_NO_ACTION env var.'
    sys.exit(0)

  # Use the Psyco JIT if available.
  if psyco:
    psyco.profile()
    print "Enabled Psyco JIT."

  # Fall back on hermetic python if we happen to get run under cygwin.
  # TODO(bradnelson): take this out once this issue is fixed:
  #    http://code.google.com/p/gyp/issues/detail?id=177
  if sys.platform == 'cygwin':
    import find_depot_tools
    depot_tools_path = find_depot_tools.add_depot_tools_to_path()
    python_dir = sorted(glob.glob(os.path.join(depot_tools_path,
                                               'python2*_bin')))[-1]
    env = os.environ.copy()
    env['PATH'] = python_dir + os.pathsep + env.get('PATH', '')
    p = subprocess.Popen(
       [os.path.join(python_dir, 'python.exe')] + sys.argv,
       env=env, shell=False)
    p.communicate()
    sys.exit(p.returncode)

  # This could give false positives since it doesn't actually do real option
  # parsing.  Oh well.
  gyp_file_specified = False
  for arg in args:
    if arg.endswith('.gyp'):
      gyp_file_specified = True
      break

  gyp_environment.SetEnvironment()

  # If we didn't get a file, check an env var, and then fall back to
  # assuming 'all.gyp' from the same directory as the script.
  if not gyp_file_specified:
    gyp_file = os.environ.get('CHROMIUM_GYP_FILE')
    if gyp_file:
      # Note that CHROMIUM_GYP_FILE values can't have backslashes as
      # path separators even on Windows due to the use of shlex.split().
      args.extend(shlex.split(gyp_file))
    else:
      args.append(os.path.join(script_dir, 'all.gyp'))

  # There shouldn't be a circular dependency relationship between .gyp files,
  # but in Chromium's .gyp files, on non-Mac platforms, circular relationships
  # currently exist.  The check for circular dependencies is currently
  # bypassed on other platforms, but is left enabled on the Mac, where a
  # violation of the rule causes Xcode to misbehave badly.
  # TODO(mark): Find and kill remaining circular dependencies, and remove this
  # option.  http://crbug.com/35878.
  # TODO(tc): Fix circular dependencies in ChromiumOS then add linux2 to the
  # list.
  if sys.platform not in ('darwin',):
    args.append('--no-circular-check')

  # We explicitly don't support the make gyp generator (crbug.com/348686). Be
  # nice and fail here, rather than choking in gyp.
  if re.search(r'(^|,|\s)make($|,|\s)', os.environ.get('GYP_GENERATORS', '')):
    print 'Error: make gyp generator not supported (check GYP_GENERATORS).'
    sys.exit(1)

  # If CHROMIUM_GYP_SYNTAX_CHECK is set to 1, it will invoke gyp with --check
  # to enfore syntax checking.
  syntax_check = os.environ.get('CHROMIUM_GYP_SYNTAX_CHECK')
  if syntax_check and int(syntax_check):
    args.append('--check')

  supplemental_includes = GetSupplementalFiles()
  gyp_vars_dict = GetGypVars(supplemental_includes)

  # TODO(dmikurube): Remove these checks and messages after a while.
  if ('linux_use_tcmalloc' in gyp_vars_dict or
      'android_use_tcmalloc' in gyp_vars_dict):
    print '*****************************************************************'
    print '"linux_use_tcmalloc" and "android_use_tcmalloc" are deprecated!'
    print '-----------------------------------------------------------------'
    print 'You specify "linux_use_tcmalloc" or "android_use_tcmalloc" in'
    print 'your GYP_DEFINES. Please switch them into "use_allocator" now.'
    print 'See http://crbug.com/345554 for the details.'
    print '*****************************************************************'

  # Automatically turn on crosscompile support for platforms that need it.
  # (The Chrome OS build sets CC_host / CC_target which implicitly enables
  # this mode.)
  if all(('ninja' in os.environ.get('GYP_GENERATORS', ''),
          gyp_vars_dict.get('OS') in ['android', 'ios'],
          'GYP_CROSSCOMPILE' not in os.environ)):
    os.environ['GYP_CROSSCOMPILE'] = '1'
  if gyp_vars_dict.get('OS') == 'android':
    args.append('--check')

  args.extend(
      ['-I' + i for i in additional_include_files(supplemental_includes, args)])

  args.extend(['-D', 'gyp_output_dir=' + GetOutputDirectory()])
#  args.extend(['--debug', 'includes'])
  args.extend(['--depth', chrome_src])
  args.extend(['--no-parallel'])

  if not use_analyzer:
    print 'Updating projects from gyp files...'
    sys.stdout.flush()

  # Off we go...
  gyp_rc = gyp.main(args)

  if not use_analyzer:
    vs2013_runtime_dll_dirs = vs_toolchain.SetEnvironmentAndGetRuntimeDllDirs()
    if vs2013_runtime_dll_dirs:
      x64_runtime, x86_runtime = vs2013_runtime_dll_dirs
      vs_toolchain.CopyVsRuntimeDlls(
        os.path.join(chrome_src, GetOutputDirectory()),
        (x86_runtime, x64_runtime))

  sys.exit(gyp_rc)