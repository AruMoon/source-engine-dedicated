#! /usr/bin/env python
# encoding: utf-8
# nillerusr

from __future__ import print_function
from waflib import Logs, Context, Configure
import sys
import os

VERSION = '1.0'
APPNAME = 'source-engine'
top = '.'

FT2_CHECK='''extern "C" {
#include <ft2build.h>
#include FT_FREETYPE_H
}

int main() { return FT_Init_FreeType( NULL ); }
'''

FC_CHECK='''extern "C" {
#include <fontconfig/fontconfig.h>
}

int main() { return (int)FcInit(); }
'''

Context.Context.line_just = 55 # should fit for everything on 80x26

projects={
	'game': [
		'appframework',
		'bitmap',
		'choreoobjects',
		'datacache',
		'datamodel',
		'dmxloader',
		'engine',
		'engine/voice_codecs/minimp3',
		'engine/voice_codecs/opus',
		'filesystem',
		'game/client',
		'game/server',
		'gameui',
		'inputsystem',
		'ivp/havana',
		'ivp/havana/havok/hk_base',
		'ivp/havana/havok/hk_math',
		'ivp/ivp_compact_builder',
		'ivp/ivp_physics',
		'launcher',
		'launcher_main',
		'materialsystem',
		'materialsystem/shaderapidx9',
		'materialsystem/shaderlib',
		'materialsystem/stdshaders',
		'mathlib',
		'particles',
		'scenefilecache',
		'serverbrowser',
		'soundemittersystem',
		'studiorender',
		'thirdparty/StubSteamAPI',
		'tier0',
		'tier1',
		'tier2',
		'tier3',
		'vgui2/matsys_controls',
		'vgui2/src',
		'vgui2/vgui_controls',
		'vgui2/vgui_surfacelib',
		'vguimatsurface',
		'video',
		'vphysics',
		'vpklib',
		'vstdlib',
		'vtf'
	],
	'dedicated': [
		'appframework',
		'bitmap',
		'choreoobjects',
		'datacache',
		'dedicated',
		'dedicated_main',
		'dmxloader',
		'engine',
		'game/server',
		'ivp/havana',
		'ivp/havana/havok/hk_base',
		'ivp/havana/havok/hk_math',
		'ivp/ivp_compact_builder',
		'ivp/ivp_physics',
		'materialsystem',
		'mathlib',
		'particles',
		'scenefilecache',
		'materialsystem/shaderapiempty',
		'materialsystem/shaderlib',
		'soundemittersystem',
		'studiorender',
		'tier0',
		'tier1',
		'tier2',
		'tier3',
		'vphysics',
		'vpklib',
		'vstdlib',
		'vtf',
		'thirdparty/StubSteamAPI'
	]
}

@Configure.conf
def check_pkg(conf, package, uselib_store, fragment, *k, **kw):
	errormsg = '{0} not available! Install {0} development package. Also you may need to set PKG_CONFIG_PATH environment variable'.format(package)
	confmsg = 'Checking for \'{0}\' sanity'.format(package)
	errormsg2 = '{0} isn\'t installed correctly. Make sure you installed proper development package for target architecture'.format(package)

	try:
		conf.check_cfg(package=package, args='--cflags --libs', uselib_store=uselib_store, *k, **kw )
	except conf.errors.ConfigurationError:
		conf.fatal(errormsg)

	try:
		conf.check_cxx(fragment=fragment, use=uselib_store, msg=confmsg, *k, **kw)
	except conf.errors.ConfigurationError:
		conf.fatal(errormsg2)

@Configure.conf
def get_taskgen_count(self):
	try: idx = self.tg_idx_count
	except: idx = 0 # don't set tg_idx_count to not increase counter
	return idx

def define_platform(conf):
	conf.env.DEDICATED = conf.options.DEDICATED
	conf.env.TOGLES = conf.options.TOGLES
	conf.env.GL = conf.options.GL

	if conf.options.DEDICATED:
		conf.options.SDL = False
#		conf.options.GL = False
		conf.define('DEDICATED', 1)

	if conf.options.GL:
		conf.env.append_unique('DEFINES', [
			'DX_TO_GL_ABSTRACTION',
			'GL_GLEXT_PROTOTYPES',
			'BINK_VIDEO'
		])

	if conf.options.TOGLES:
		conf.env.append_unique('DEFINES', ['TOGLES'])


	if conf.options.SDL:
		conf.define('USE_SDL', 1)

	if conf.env.DEST_OS == 'linux':
		conf.define('_GLIBCXX_USE_CXX11_ABI',0)
		conf.env.append_unique('DEFINES', [
			'LINUX=1', '_LINUX=1',
			'POSIX=1', '_POSIX=1',
			'GNUC',
			'NO_HOOK_MALLOC',
			'_DLL_EXT=.so'
		])

	if conf.env.DEST_OS == 'android':
		conf.env.append_unique('DEFINES', [
			'ANDROID=1', '_ANDROID=1',
			'LINUX=1', '_LINUX=1',
			'POSIX=1', '_POSIX=1',
			'GNUC',
			'NO_HOOK_MALLOC',
			'_DLL_EXT=.so'
		])

	if conf.options.DEBUG_ENGINE:
		conf.env.append_unique('DEFINES', [
			'DEBUG', '_DEBUG'
		])
	else:
		conf.env.append_unique('DEFINES', [
			'NDEBUG'
		])

def options(opt):
	grp = opt.add_option_group('Common options')

	grp.add_option('-8', '--64bits', action = 'store_true', dest = 'ALLOW64', default = False,
		help = 'allow targetting 64-bit engine(Linux/Windows/OSX x86 only) [default: %default]')

	grp.add_option('-d', '--dedicated', action = 'store_true', dest = 'DEDICATED', default = False,
		help = 'build dedicated server [default: %default]')

	grp.add_option('-D', '--debug-engine', action = 'store_true', dest = 'DEBUG_ENGINE', default = False,
		help = 'build with -DDEBUG [default: %default]')

	grp.add_option('--use-sdl', action = 'store', dest = 'SDL', type = 'int', default = True,
		help = 'build engine with SDL [default: %default]')

	grp.add_option('--use-togl', action = 'store', dest = 'GL', type = 'int', default = True,
		help = 'build engine with ToGL [default: %default]')

	grp.add_option('--build-games', action = 'store', dest = 'GAMES', type = 'string', default = 'hl2',
		help = 'build games [default: %default]')

	grp.add_option('--use-ccache', action = 'store_true', dest = 'CCACHE', default = False,
		help = 'build using ccache [default: %default]')

	grp.add_option('--togles', action = 'store_true', dest = 'TOGLES', default = False,
		help = 'build engine with ToGLES [default: %default]')

	opt.load('compiler_optimizations subproject')

#	opt.add_subproject(projects['game'])

	opt.load('xcompile compiler_cxx compiler_c sdl2 clang_compilation_database strip_on_install waf_unit_test subproject')
	if sys.platform == 'win32':
		opt.load('msvc msdev msvs')
	opt.load('reconfigure')

def configure(conf):
	conf.load('fwgslib reconfigure')

	# Force XP compability, all build targets should add
	# subsystem=bld.env.MSVC_SUBSYSTEM
	# TODO: wrapper around bld.stlib, bld.shlib and so on?
	conf.env.MSVC_SUBSYSTEM = 'WINDOWS,5.01'
	conf.env.MSVC_TARGETS = ['x86'] # explicitly request x86 target for MSVC
	if sys.platform == 'win32':
		conf.load('msvc msvc_pdb msdev msvs')
	conf.load('subproject xcompile compiler_c compiler_cxx gitversion clang_compilation_database strip_on_install waf_unit_test enforce_pic')

	define_platform(conf)

	if conf.env.TOGLES:
		projects['game'] += ['togles']
	elif conf.env.GL:
		projects['game'] += ['togl']


	if conf.env.DEST_OS in ['win32', 'linux', 'darwin'] and conf.env.DEST_CPU == 'x86_64':
		conf.env.BIT32_MANDATORY = not conf.options.ALLOW64
		if conf.env.BIT32_MANDATORY:
			Logs.info('WARNING: will build engine for 32-bit target')
	else:
		conf.env.BIT32_MANDATORY = False

	conf.load('force_32bit')

	compiler_optional_flags = [
		'-pipe',
		'-Wall',
		'-fdiagnostics-color=always',
		'-Wcast-align',
		'-Wuninitialized',
		'-Winit-self',
		'-Wstrict-aliasing',
		'-faligned-new'
 #		'-Werror=strict-aliasing'
	]

	c_compiler_optional_flags = [
		'-fnonconst-initializers' # owcc
	]

	cflags, linkflags = conf.get_optimization_flags()

	flags = ['-fPIC'] #, '-fsanitize=undefined']

	if conf.env.DEST_OS == 'android':
		flags += [
			'-L'+os.path.abspath('.')+'/lib/android/armeabi-v7a/',
			'-I'+os.path.abspath('.')+'/thirdparty/curl/include',
			'-I'+os.path.abspath('.')+'/thirdparty/SDL',
			'-I'+os.path.abspath('.')+'/thirdparty/openal-soft/include/',
			'-I'+os.path.abspath('.')+'/thirdparty/fontconfig',
			'-I'+os.path.abspath('.')+'/thirdparty/freetype/include',
			'-llog',
			'-lz'
		]

	if conf.env.DEST_CPU == 'arm':
		flags += ['-fsigned-char']

		if conf.env.DEST_OS != 'android':
			flags += ['-march=native', '-mtune=native']
	else:
		flags += ['-march=native','-mtune=native','-mfpmath=sse', '-msse', '-msse2']


	cflags += flags
	linkflags += flags

	# And here C++ flags starts to be treated separately
	cxxflags = list(cflags) + ['-std=c++11','-fpermissive']

	if conf.env.COMPILER_CC == 'gcc':
#		wrapfunctions = ['freopen','creat','access','__xstat','stat','lstat','fopen64','open64',
#			'opendir','__lxstat','chmod','chown','lchown','symlink','link','__lxstat64','mknod',
#			'utimes','unlink','rename','utime','__xstat64','mount','mkdir','rmdir','scandir','realpath','mkfifo']

#		for func in wrapfunctions:
#			linkflags += ['-Wl,--wrap='+func]


		conf.define('COMPILER_GCC', 1)


	if conf.env.COMPILER_CC != 'msvc':
		conf.check_cc(cflags=cflags, linkflags=linkflags, msg='Checking for required C flags')
		conf.check_cxx(cxxflags=cxxflags, linkflags=linkflags, msg='Checking for required C++ flags')

		linkflags += ['-pthread']
		conf.env.append_unique('CFLAGS', cflags)
		conf.env.append_unique('CXXFLAGS', cxxflags)
		conf.env.append_unique('LINKFLAGS', linkflags)

		cxxflags += conf.filter_cxxflags(compiler_optional_flags, cflags)
		cflags += conf.filter_cflags(compiler_optional_flags + c_compiler_optional_flags, cflags)

	conf.env.append_unique('CFLAGS', cflags)
	conf.env.append_unique('CXXFLAGS', cxxflags)
	conf.env.append_unique('LINKFLAGS', linkflags)
	conf.env.append_unique('INCLUDES', [os.path.abspath('common/')])

	if conf.env.DEST_OS != 'android':
		if conf.options.SDL:
			conf.check_cfg(package='sdl2', uselib_store='SDL2', args=['--cflags', '--libs'])
		if conf.options.DEDICATED:
			conf.check_cfg(package='libedit', uselib_store='EDIT', args=['--cflags', '--libs'])
		else:
			conf.check_pkg('freetype2', 'FT2', FT2_CHECK)
			conf.check_pkg('fontconfig', 'FC', FC_CHECK)
			conf.check_cfg(package='openal', uselib_store='OPENAL', args=['--cflags', '--libs'])
			conf.check_cfg(package='libjpeg', uselib_store='JPEG', args=['--cflags', '--libs'])
			conf.check_cfg(package='libpng', uselib_store='PNG', args=['--cflags', '--libs'])
			conf.check_cfg(package='libcurl', uselib_store='CURL', args=['--cflags', '--libs'])
		conf.check_cfg(package='zlib', uselib_store='ZLIB', args=['--cflags', '--libs'])
		conf.check_cfg(package='opus', uselib_store='OPUS', args=['--cflags', '--libs'])
#		conf.check_cfg(package='speex', uselib_store='SPEEX', args=['--cflags', '--libs'])
	else:
		conf.check(lib='SDL2', uselib_store='SDL2')
		conf.check(lib='freetype2', uselib_store='FT2')
		conf.check(lib='openal', uselib_store='OPENAL')
		conf.check(lib='jpeg', uselib_store='JPEG')
		conf.check(lib='png', uselib_store='PNG')
		conf.check(lib='curl', uselib_store='CURL')
		conf.check(lib='z', uselib_store='ZLIB')
		conf.check(lib='crypto', uselib_store='CRYPTO')
		conf.check(lib='ssl', uselib_store='SSL')
		conf.check(lib='expat', uselib_store='EXPAT')
		conf.check(lib='android_support', uselib_store='ANDROID_SUPPORT')
		conf.check(lib='opus', uselib_store='OPUS')
#		conf.check(lib='speex', uselib_store='SPEEX')

	if conf.env.DEST_OS != 'win32':
		conf.check_cc(lib='dl', mandatory=False)
		conf.check_cc(lib='bz2', mandatory=False)
		conf.check_cc(lib='rt', mandatory=False)

		if not conf.env.LIB_M: # HACK: already added in xcompile!
			conf.check_cc(lib='m')
	else:
		# Common Win32 libraries
		# Don't check them more than once, to save time
		# Usually, they are always available
		# but we need them in uselib
		a = map(lambda x: {
			# 'features': 'c',
			# 'message': '...' + x,
			'lib': x,
			# 'uselib_store': x.upper(),
			# 'global_define': False,
		}, [
			'user32',
			'shell32',
			'gdi32',
			'advapi32',
			'dbghelp',
			'psapi',
			'ws2_32'
		])

		for i in a:
			conf.check_cc(**i)

		# conf.multicheck(*a, run_all_tests = True, mandatory = True)

	# indicate if we are packaging for Linux/BSD
	if conf.env.DEST_OS != 'android':
		conf.env.LIBDIR = conf.env.PREFIX+'/bin/'
		conf.env.BINDIR = conf.env.PREFIX
	else:
		conf.env.LIBDIR = conf.env.BINDIR = conf.env.PREFIX

	if conf.options.CCACHE:
		conf.env.CC.insert(0, 'ccache')
		conf.env.CXX.insert(0, 'ccache')
		print( conf.env )

	if conf.options.DEDICATED:
		conf.add_subproject(projects['dedicated'])
	else:
		conf.add_subproject(projects['game'])

def build(bld):
	os.environ["CCACHE_DIR"] = os.path.abspath('.ccache/'+bld.env.COMPILER_CC+'/'+bld.env.DEST_OS+'/'+bld.env.DEST_CPU)

	if bld.env.DEDICATED:
		bld.add_subproject(projects['dedicated'])
	else:
		if bld.env.TOGLES:
			projects['game'] += ['togles']
		elif bld.env.GL:
			projects['game'] += ['togl']

		bld.add_subproject(projects['game'])
