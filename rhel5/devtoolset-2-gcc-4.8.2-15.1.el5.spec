%if 0%{?copr_username:1}  
%global scl %{copr_username}-%{copr_projectname} 
%else  
%global scl_name_prefix devtoolset-2  
%global scl_name_base gcc  
%global scl_name_version 48  
%global scl %{scl_name_prefix}  
%endif  

%{?scl:%scl_package gcc}
%{?scl:%global __strip strip}
%{?scl:%global __objdump objdump}
%global DATE 20140120
%global SVNREV 206854
%global gcc_version 4.8.2
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 15
%global gmp_version 4.3.1
%global mpfr_version 2.4.1
%global mpc_version 0.8.1
%global cloog_version 0.18.0
%global isl_version 0.11.1
%global graphviz_version 2.26.0
%global doxygen_version 1.8.0
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%global build_fortran 1
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 s390 s390x
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 s390 s390x %{arm}
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%global build_cloog 1
%global build_libstdcxx_docs 1
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
%global multilib_32_arch i686
%else
%global multilib_32_arch i386
%endif
%endif
Summary: GCC version 4.8
Name: %{?scl_prefix}gcc
#Name: %{?scl_prefix}gcc%{!?scl:48}

Version: %{gcc_version}
Release: %{gcc_release}.1.lf.0.0%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_8-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: http://www.mpfr.org/mpfr-%{mpfr_version}/mpfr-%{mpfr_version}.tar.bz2
Source2: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Source3: ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-%{cloog_version}.tar.gz
Source4: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
Source5: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{gmp_version}.tar.bz2
Source6: http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-%{graphviz_version}.tar.gz
Source7: ftp://ftp.stack.nl/pub/users/dimitri/doxygen-%{doxygen_version}.src.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
%if 0%{?rhel} >= 6
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.19.51.0.14-33
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
%else
# Don't have binutils which support --build-id >= 2.17.50.0.17-3
# Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
# Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.17.50.0.2-8
%endif
%if 0%{?scl:1}
BuildRequires: %{?scl_prefix}binutils >= 2.22.52.0.1
# For testing
BuildRequires: %{?scl_prefix}gdb >= 7.4.50
%endif
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
BuildRequires: /usr/bin/pod2man
%if 0%{?rhel} >= 7
BuildRequires: texinfo-tex
%endif
#BuildRequires: systemtap-sdt-devel >= 1.3
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
%if 0%{?rhel} >= 6
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%else
BuildRequires: elfutils-devel >= 0.72
%endif
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
%if 0%{?rhel} >= 6
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
Requires: binutils >= 2.19.51.0.14-33
%else
# Don't have binutils which support --build-id >= 2.17.50.0.17-3
# Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
# Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
Requires: binutils >= 2.17.50.0.2-8
%endif
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= 4.1.2-43
Requires: libgomp >= 4.4.4-13
BuildRequires: gmp-devel >= 4.1.2-8
%if 0%{?rhel} >= 6
BuildRequires: mpfr-devel >= 2.2.1
%endif
%if 0%{?rhel} >= 7
BuildRequires: libmpc-devel >= 0.8.1
%endif
%if %{build_libstdcxx_docs}
BuildRequires: libxml2
%if 0%{?rhel} < 6
# graphviz BRs:
BuildRequires: libpng-devel, libjpeg-devel, expat-devel, freetype-devel
BuildRequires: /bin/ksh, m4, flex, tk-devel, tcl-devel, swig
BuildRequires: fontconfig-devel, libtool-ltdl-devel
BuildRequires: libXaw-devel, libSM-devel, libXext-devel
BuildRequires: cairo-devel, pango-devel, gmp-devel
BuildRequires: gtk2-devel, libgnomeui-devel, gd-devel
BuildRequires: urw-fonts
%else
BuildRequires: graphviz
%endif
%if 0%{?rhel} < 7
# doxygen BRs
BuildRequires: perl
%if 0%{?rhel} < 6
BuildRequires: tetex-dvips tetex-latex
%else
BuildRequires: texlive-dvips, texlive-utils, texlive-latex
%endif
BuildRequires: ghostscript
%endif
%if 0%{?rhel} >= 7
BuildRequires: doxygen >= 1.7.1
BuildRequires: dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
%endif
%{?scl:Requires:%scl_runtime}
%{?scl:Provides:gcc = %{version}-%{release}}
AutoReq: true
AutoProv: false
%ifarch sparc64 ppc64 s390x x86_64 ia64
Provides: liblto_plugin.so.0()(64bit)
%else
Provides: liblto_plugin.so.0
%endif
%global oformat %{nil}
%global oformat2 %{nil}
%ifarch %{ix86}
%global oformat OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch x86_64
%global oformat OUTPUT_FORMAT(elf64-x86-64)
%global oformat2 OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch ppc
%global oformat OUTPUT_FORMAT(elf32-powerpc)
%global oformat2 OUTPUT_FORMAT(elf64-powerpc)
%endif
%ifarch ppc64
%global oformat OUTPUT_FORMAT(elf64-powerpc)
%global oformat2 OUTPUT_FORMAT(elf32-powerpc)
%endif
%ifarch s390
%global oformat OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch s390x
%global oformat OUTPUT_FORMAT(elf64-s390)
%global oformat2 OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch ia64
%global oformat OUTPUT_FORMAT(elf64-ia64-little)
%endif

Patch0: gcc48-hack.patch
Patch1: gcc48-java-nomulti.patch
Patch2: gcc48-ppc32-retaddr.patch
Patch3: gcc48-rh330771.patch
Patch4: gcc48-i386-libgomp.patch
Patch5: gcc48-sparc-config-detection.patch
Patch6: gcc48-libgomp-omp_h-multilib.patch
Patch7: gcc48-libtool-no-rpath.patch
Patch8: gcc48-cloog-dl.patch
Patch9: gcc48-cloog-dl2.patch
Patch10: gcc48-pr38757.patch
Patch11: gcc48-libstdc++-docs.patch
Patch12: gcc48-no-add-needed.patch
Patch13: gcc48-pr56564.patch
Patch14: gcc48-pr56493.patch
Patch15: gcc48-color-auto.patch
Patch16: gcc48-pr28865.patch
Patch17: gcc48-libgo-p224.patch
Patch18: gcc48-pr60137.patch
Patch19: gcc48-pr60010.patch
Patch20: gcc48-pr60046.patch

Patch1000: gcc48-libstdc++-compat.patch
Patch1001: gcc48-gnu89-inline-dflt.patch
Patch1002: gcc48-ppc64-ld-workaround.patch
Patch1005: gcc48-gmp-4.0.1-s390.patch
Patch1006: gcc48-libgfortran-compat.patch
Patch1007: gcc48-alt-compat-test.patch
Patch1008: gcc48-libquadmath-compat.patch
Patch1009: gcc48-libstdc++44-xfail.patch
Patch1010: gcc48-rh1118870.patch

Patch1100: isl-%{isl_version}-aarch64-config.patch

Patch2001: doxygen-1.7.1-config.patch
Patch2002: doxygen-1.7.5-timestamp.patch
Patch2003: doxygen-1.8.0-rh856725.patch


# Define Bloomberg specific patches provided by Codethink
Patch3000: 0000-decl.c-variable_decl-Reject-old-style-initialization.patch
Patch3001: 0001-Allow-under-specified-array-references.patch
Patch3002: 0002-Add-an-AUTOMATIC-statement-for-use-with-fno-automati.patch
Patch3003: 0003-Add-tests-for-AUTOMATIC-keyword.patch
Patch3004: 0004-Allow-repeated-compatible-type-specifications.patch
Patch3005: 0005-Add-test-for-duplicate-type-statements.patch
Patch3006: 0006-Correct-internal-fault-in-select_type_9.f90.patch
Patch3007: 0007-Add-test-for-underspecified-array-references.patch
Patch3008: 0008-Fix-warning-message-for-underspecified-arrays.patch
Patch3009: 0009-Add-support-for-the-STRUCTURE-statement-which-is-syn.patch
Patch3010: 0010-Add-std-extra-legacy.patch
Patch3011: 0011-Allow-dot-.-operator-as-structure-member-operator.patch
Patch3012: 0012-Allow-RECORD-statement-with-slash-quoted-names.patch
Patch3013: 0013-Add-test-for-STRUCTURE-and-RECORD.patch
Patch3014: 0014-Support-comparison-between-HOLLERITH-and-CHARACTER-p.patch
Patch3015: 0015-Character-to-integer-assignment-support.patch
Patch3016: 0016-Documentation-for-the-AUTOMATIC-statement.patch
Patch3017: 0017-Correction-to-gfc_add_automatic-fail-if-gfc_notify_s.patch
Patch3018: 0018-Correct-error-in-character2representation.patch
Patch3019: 0019-Pad-character-to-int-conversions-with-spaces-instead.patch
Patch3020: 0020-Promote-int-to-real-when-using-check_a_p.patch
Patch3021: 0021-Pad-character-to-int-conversions-with-spaces-instead.patch
Patch3022: 0022-Fixup-57fd95a-Typo-in-DEFAULT_WIDTH.patch
Patch3023: 0023-Very-hacky-implementation-of-default-widths-for-floa.patch
Patch3024: 0024-Allow-more-than-one-character-as-argument-to-ICHAR.patch
Patch3025: 0025-Allow-non-integer-substring-indexes.patch
Patch3026: 0026-Allow-blank-format-items-in-format-strings.patch
Patch3027: 0027-Convert-integer-arguments-to-logicals-for-logical-op.patch
Patch3028: 0028-Allow-mixed-string-length-and-array-specification-in.patch
Patch3029: 0029-Allow-character-to-int-conversions-in-DATA-statement.patch
Patch3030: 0030-Convert-logicals-to-ints-for-arithmetic-ops-and-vice.patch
Patch3031: 0031-Experimental-Old-style-initializers-in-derived-types.patch
Patch3032: 0032-Allow-per-variable-kind-specification.patch
Patch3033: 0033-Add-support-for-integer-expressions-in-IF-statements.patch
Patch3034: 0034-Allow-continued-include-lines.patch
Patch3035: 0035-Allow-non-logical-expressions-in-basic-form-of-IF-st.patch
Patch3036: 0036-Allow-redefinition-of-types-for-procedures.patch
Patch3037: 0037-Allow-character-to-int-comparisons.patch
Patch3038: 0038-Accept-.xor.-as-an-alias-for-.neqv.patch
Patch3039: 0039-Allow-calls-to-intrinsics-with-smaller-types-than-sp.patch
Patch3040: 0040-Refine-the-promotion-of-smaller-ints-during-a-functi.patch
Patch3041: 0041-Add-the-SEQUENCE-attribute-by-default-if-it-s-not-pr.patch
Patch3042: 0042-More-general-rules-for-use-of-.-as-structure-operato.patch
Patch3043: 0043-Only-allow-redefinition-of-procedure-type-with-std-e.patch
Patch3044: 0044-Correct-warnings-expected-in-hollerith-int-compariso.patch
Patch3045: 0045-Improved-support-for-STRUCTURE-add-_SI-to-the-name-o.patch
Patch3046: 0046-Remove-all-references-to-foracle-support-this-is-now.patch
Patch3047: 0047-Revert-all-previous-support-for-STRUCTURE.patch
Patch3048: 0048-STRUCTURE-UNION-and-MAP-support.patch
Patch3049: 0049-union-fix-for-rhel6.patch


%if 0%{?rhel} >= 7
%global nonsharedver 48
%else
%if 0%{?rhel} == 6
%global nonsharedver 44
%else
%global nonsharedver 41
%endif
%endif

%if 0%{?scl:1}
%global _gnu %{nil}
%else
%global _gnu 7E
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
The %{?scl_prefix}gcc%{!?scl:48} package contains the GNU Compiler Collection version 4.8.

%package c++
Summary: C++ support for GCC version 4.8
Group: Development/Languages
Requires: %{?scl_prefix}gcc%{!?scl:48} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: libstdc++
%else
%if 0%{?rhel} == 6
Requires: libstdc++ >= 4.4.4-13
%else
Requires: libstdc++ = 4.1.2
%endif
%endif
Requires: %{?scl_prefix}libstdc++%{!?scl:48}-devel = %{version}-%{release}
Autoreq: true
Autoprov: true

%description c++
This package adds C++ support to the GNU Compiler Collection
version 4.8.  It includes support for most of the current C++ specification
and a lot of support for the upcoming C++ specification.

%package -n %{?scl_prefix}libstdc++%{!?scl:48}-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
%if 0%{?rhel} >= 7
Requires: libstdc++
%else
%if 0%{?rhel} >= 6
Requires: libstdc++ >= 4.4.4-13
%else
Requires: libstdc++ = 4.1.2
%endif
%endif
Requires: %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6
Autoreq: true
Autoprov: true

%description -n %{?scl_prefix}libstdc++%{!?scl:48}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n %{?scl_prefix}libstdc++%{!?scl:48}-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n %{?scl_prefix}libstdc++%{!?scl:48}-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package gfortran
Summary: Custom fortran support for GCC 4.8
Group: Development/Languages
Requires: %{?scl_prefix}gcc%{!?scl:48} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: libgfortran
%else
%if 0%{?rhel} == 6
Requires: libgfortran >= 4.4.4-13
%else
Requires: libgfortran44 >= 4.4.4-13
Requires: gmp-devel >= 4.1.2-8
Requires: %{?scl_prefix}binutils >= 2.22.52.0.1
%endif
%endif
%if %{build_libquadmath}
%if 0%{!?scl:1}
%if 0%{?rhel} >= 7
Requires: libquadmath
%else
Requires: %{?scl_prefix}libquadmath = %{version}-%{release}
%endif
%else
%if 0%{?rhel} >= 7
Requires: libquadmath
%endif
%endif
Requires: %{?scl_prefix}libquadmath-devel = %{version}-%{release}
%endif
Autoreq: true
Autoprov: true

%description gfortran
The %{?scl_prefix}gcc%{!?scl:48}-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n %{?scl_prefix}libquadmath
Summary: GCC 4.8 __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n %{?scl_prefix}libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n %{?scl_prefix}libquadmath-devel
Summary: GCC 4.8 __float128 support
Group: Development/Libraries
%if 0%{!?scl:1}
Requires: %{?scl_prefix}libquadmath = %{version}-%{release}
%else
%if 0%{?rhel} >= 7
Requires: libquadmath
%endif
%endif
Requires: %{?scl_prefix}gcc%{!?scl:48} = %{version}-%{release}

%description -n %{?scl_prefix}libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n %{?scl_prefix}libitm-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libitm >= 4.7.0-1
Requires: %{?scl_prefix}gcc%{!?scl:48} = %{version}-%{release}

%description -n %{?scl_prefix}libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: %{?scl_prefix}gcc%{!?scl:48} = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8
%if 0%{?rhel} >= 6
Requires: mpfr-devel >= 2.2.1
%endif
%if 0%{?rhel} >= 7
Requires: libmpc-devel >= 0.8.1
%endif

%description plugin-devel
This package contains header files and other support files
for compiling GCC 4.8 plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n %{?scl_prefix}libatomic-devel
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic >= 4.8.0

%description -n %{?scl_prefix}libatomic-devel
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n %{?scl_prefix}libasan-devel
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan >= 4.8.0

%description -n %{?scl_prefix}libasan-devel
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n %{?scl_prefix}libtsan-devel
Summary: The Thread Sanitizer static library
Group: Development/Libraries
Requires: libtsan = %{version}-%{release}

%description -n %{?scl_prefix}libtsan-devel
This package contains Thread Sanitizer static runtime library.

%prep
%if 0%{?rhel} >= 7
%setup -q -n gcc-%{version}-%{DATE} -a 2 -a 3
%else
%if 0%{?rhel} >= 6
%setup -q -n gcc-%{version}-%{DATE} -a 2 -a 3 -a 4 -a 7
%else
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7
%endif
%endif
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch8 -p0 -b .cloog-dl~
%patch9 -p0 -b .cloog-dl2~
%endif
%patch10 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch11 -p0 -b .libstdc++-docs~
%endif
%patch12 -p0 -b .no-add-needed~
%patch13 -p0 -b .pr56564~
%patch14 -p0 -b .pr56493~
%patch15 -p0 -b .color-auto~
%patch16 -p0 -b .pr28865~
%patch17 -p0 -b .libgo-p224~
rm -f libgo/go/crypto/elliptic/p224{,_test}.go
%patch18 -p0 -b .pr60137~
%patch19 -p0 -b .pr60010~
%patch20 -p0 -b .pr60046~

%patch1000 -p0 -b .libstdc++-compat~
%if 0%{?rhel} < 6
%patch1001 -p0 -b .gnu89-inline-dflt~
%patch1002 -p0 -b .ppc64-ld-workaround~
%if %{build_cloog}
%patch1005 -p0 -b .gmp-4.0.1-s390~
%endif
%endif
%patch1006 -p0 -b .libgfortran-compat~
%ifarch %{ix86} x86_64
# On i?86/x86_64 there are some incompatibilities in _Decimal* as well as
# aggregates containing larger vector passing.
%patch1007 -p0 -b .alt-compat-test~
%endif
%if 0%{?rhel} < 7
%patch1008 -p0 -b .libquadmath-compat~
%endif
%if 0%{?rhel} == 6
%patch1009 -p0 -b .libstdc++44-xfail~
%endif
%patch1010 -p0 -b .rh1118870~

%patch1100 -p0 -b .isl-aarch64~

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 7
cd doxygen-%{doxygen_version}
%patch2001 -p1 -b .config~
%patch2002 -p1 -b .timestamp~
%patch2003 -p1 -b .rh856725~
cd ..
%endif
%endif


# Apply Bloomberg specific patches
%patch3000 -p1 -b .blp0000~
%patch3001 -p1 -b .blp0001~
%patch3002 -p1 -b .blp0002~
%patch3003 -p1 -b .blp0003~
%patch3004 -p1 -b .blp0004~
%patch3005 -p1 -b .blp0005~
%patch3006 -p1 -b .blp0006~
%patch3007 -p1 -b .blp0007~
%patch3008 -p1 -b .blp0008~
%patch3009 -p1 -b .blp0009~
%patch3010 -p1 -b .blp0010~
%patch3011 -p1 -b .blp0011~
%patch3012 -p1 -b .blp0012~
%patch3013 -p1 -b .blp0013~
%patch3014 -p1 -b .blp0014~
%patch3015 -p1 -b .blp0015~
%patch3016 -p1 -b .blp0016~
%patch3017 -p1 -b .blp0017~
%patch3018 -p1 -b .blp0018~
%patch3019 -p1 -b .blp0019~
%patch3020 -p1 -b .blp0020~
%patch3021 -p1 -b .blp0021~
%patch3022 -p1 -b .blp0022~
%patch3023 -p1 -b .blp0023~
%patch3024 -p1 -b .blp0024~
%patch3025 -p1 -b .blp0025~
%patch3026 -p1 -b .blp0026~
%patch3027 -p1 -b .blp0027~
%patch3028 -p1 -b .blp0028~
%patch3029 -p1 -b .blp0029~
%patch3030 -p1 -b .blp0030~
%patch3031 -p1 -b .blp0031~
%patch3032 -p1 -b .blp0032~
%patch3033 -p1 -b .blp0033~
%patch3034 -p1 -b .blp0034~
%patch3035 -p1 -b .blp0035~
%patch3036 -p1 -b .blp0036~
%patch3037 -p1 -b .blp0037~
%patch3038 -p1 -b .blp0038~
%patch3039 -p1 -b .blp0039~
%patch3040 -p1 -b .blp0040~
%patch3041 -p1 -b .blp0041~
%patch3042 -p1 -b .blp0042~
%patch3043 -p1 -b .blp0043~
%patch3044 -p1 -b .blp0044~
%patch3045 -p1 -b .blp0045~
%patch3046 -p1 -b .blp0046~
%patch3047 -p1 -b .blp0047~
%patch3048 -p1 -b .blp0048~
%patch3049 -p1 -b .blp0049~

sed -i -e 's/4\.8\.3/4.8.2/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?rhel} == 6
# Default to -gdwarf-3 rather than -gdwarf-4
sed -i '/UInteger Var(dwarf_version)/s/Init(4)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)4\./\13./' gcc/doc/invoke.texi
%endif
%if 0%{?rhel} == 5
# Default to -gdwarf-2 rather than -gdwarf-4
sed -i '/UInteger Var(dwarf_version)/s/Init(4)/Init(2)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)4\./\12./' gcc/doc/invoke.texi
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h
cp -a libstdc++-v3/config/cpu/i{4,3}86/opt

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 6
mkdir graphviz graphviz-install
cd graphviz
find ../../graphviz-%{graphviz_version} -type f '(' \
  -name '*.h' -or -name '*.c' ')' -exec chmod 644 {} ';'
../../graphviz-%{graphviz_version}/configure --with-x --disable-static \
  --disable-dependency-tracking --without-mylibgd --with-ipsepcola \
  --with-pangocairo --with-gdk-pixbuf --disable-sharp \
  --disable-ocaml --without-ming --disable-r --without-devil \
  --disable-perl --disable-java --disable-ruby --disable-php \
  --disable-python --disable-lua --with-expatlibdir=/usr/%{_lib}/ \
  CFLAGS="${CFLAGS:-%optflags} -ffast-math -fno-strict-aliasing" \
  CXXFLAGS="${CXXFLAGS:-%optflags} -ffast-math -fno-strict-aliasing" \
  --prefix=`cd ..; pwd`/graphviz-install
make %{?_smp_mflags}
make install
export LD_LIBRARY_PATH=`cd ..; pwd`/graphviz-install/lib/${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
../graphviz-install/bin/dot -c
export PATH=`cd ..; pwd`/graphviz-install/bin/${PATH:+:${PATH}}
cd ..
%endif

%if 0%{?rhel} < 7
mkdir doxygen-install
pushd ../doxygen-%{doxygen_version}
./configure --prefix `cd ..; pwd`/obj-%{gcc_target_platform}/doxygen-install \
  --shared --release --english-only

make %{?_smp_mflags} all
make install
popd
export PATH=`pwd`/doxygen-install/bin/${PATH:+:${PATH}}
%endif
%endif

%if 0%{?rhel} < 6
mkdir gmp gmp-install
cd gmp
../../gmp-%{gmp_version}/configure --disable-shared \
  --enable-cxx --enable-mpbsd --build=%{_build} --host=%{_host} \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
  --prefix=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..

mkdir mpfr mpfr-install
cd mpfr
../../mpfr-%{mpfr_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
  --prefix=`cd ..; pwd`/mpfr-install --with-gmp=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..
%endif

%if 0%{?rhel} < 7
mkdir mpc mpc-install
cd mpc
../../mpc-%{mpc_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
%if 0%{?rhel} < 6
  --with-gmp=`cd ..; pwd`/gmp-install --with-mpfr=`cd ..; pwd`/mpfr-install \
%endif
  --prefix=`cd ..; pwd`/mpc-install
make %{?_smp_mflags}
make install
cd ..
%endif

%if %{build_cloog}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
../../isl-%{isl_version}/configure --disable-shared \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make install
cd ..

mkdir cloog-build cloog-install
cd cloog-build
cat >> ../../cloog-%{cloog_version}/source/isl/constraints.c << \EOF
#include <isl/flow.h>
static void __attribute__((used)) *s1 = (void *) isl_union_map_compute_flow;
static void __attribute__((used)) *s2 = (void *) isl_map_dump;
EOF
sed -i 's|libcloog|libgcc48privatecloog|g' \
  ../../cloog-%{cloog_version}/{,test/}Makefile.{am,in}
isl_prefix=`cd ../isl-install; pwd` \
../../cloog-%{cloog_version}/configure --with-isl=system \
  --with-isl-prefix=`cd ../isl-install; pwd` \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
   --prefix=`cd ..; pwd`/cloog-install
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make %{?_smp_mflags} install
cd ../cloog-install/lib
rm libgcc48privatecloog-isl.so{,.4}
mv libgcc48privatecloog-isl.so.4.0.0 libcloog-isl.so.4
ln -sf libcloog-isl.so.4 libcloog-isl.so
ln -sf libcloog-isl.so.4 libcloog.so
cd ../..
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
cat > g++64 <<"EOF"
#!/bin/sh
exec /usr/bin/g++ -m64 "$@"
EOF
chmod +x g++64
CXX=`pwd`/g++64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
  cat > g++64 <<"EOF"
#!/bin/sh
exec /usr/bin/g++ -m64 "$@"
EOF
  chmod +x g++64
  CXX=`pwd`/g++64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Werror=format-security / -Wformat -Werror=format-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
%if 0%{?rhel} >= 6
	--enable-gnu-unique-object \
%else
	--disable-gnu-unique-object \
%endif
%if 0%{?rhel} >= 6 || 0%{?scl:1}
	--enable-linker-build-id \
%else
	--disable-linker-build-id \
%endif
%if %{build_fortran}
	--enable-languages=c,c++,fortran,lto \
%else
	--enable-languages=c,c++,lto \
%endif
	--enable-plugin --with-linker-hash-style=gnu \
%if 0%{?scl:1}
	--enable-initfini-array \
%else
%ifnarch ia64
%if 0%{?rhel} >= 7
	--enable-initfini-array \
%else
	--disable-initfini-array \
%endif
%endif
%endif
	--disable-libgcj \
%if %{build_cloog}
	--with-isl=`pwd`/isl-install --with-cloog=`pwd`/cloog-install \
%endif
%if 0%{?rhel} < 6
	--with-gmp=`pwd`/gmp-install --with-mpfr=`pwd`/mpfr-install \
%endif
%if 0%{?rhel} < 7
	--with-mpc=`pwd`/mpc-install \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%if 0%{?rhel} >= 6
%ifarch ppc ppc64
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
%if 0%{?rhel} >= 6
	--with-arch=i686 \
%else
	--with-arch=i586 \
%endif
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
	--with-arch_32=i686 \
%else
	--with-arch_32=i586 \
%endif
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

%ifarch ia64
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,libstdc++-v3,libgomp,libatomic,libsanitizer}

for i in {gcc,gcc/cp,libstdc++-v3,libgomp,libatomic,libsanitizer}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

%if %{build_fortran}
(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%endif

%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif

%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr %{buildroot}

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 6
export LD_LIBRARY_PATH=`pwd`/obj-%{gcc_target_platform}/graphviz-install/lib/${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export PATH=`pwd`/obj-%{gcc_target_platform}/graphviz-install/bin/${PATH:+:${PATH}}
%endif
%if 0%{?rhel} < 7
export PATH=`pwd`/obj-%{gcc_target_platform}/doxygen-install/bin/${PATH:+:${PATH}}
%endif
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/doc/html/api.html

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

%if 0%{?scl:1}
ln -sf ../../../../bin/ar $FULLEPATH/ar
ln -sf ../../../../bin/as $FULLEPATH/as
ln -sf ../../../../bin/ld $FULLEPATH/ld
ln -sf ../../../../bin/nm $FULLEPATH/nm
ln -sf ../../../../bin/ranlib $FULLEPATH/ranlib
ln -sf ../../../../bin/strip $FULLEPATH/strip
%endif

%if %{build_cloog}
cp -a cloog-install/lib/libcloog-isl.so.4 $FULLPATH/
%endif

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/lib
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/lib/cpp
%if %{build_fortran}
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
%endif
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}%{?_gnu}-gcc
%endif
%ifarch ppc ppc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}%{?_gnu}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/libgfortran.spec
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif

rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif

%if %{build_libquadmath}
%if 0%{?scl:1}
%if 0%{?rhel} < 7
cp -a %{gcc_target_platform}/libquadmath/.libs/libquadmathconvenience.a \
  %{buildroot}%{_prefix}/%{_lib}/libquadmath.a
%endif
%endif
%endif

ar cruv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared48.a

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  $FULLLPATH/libstdc++_nonshared.a
%if %{build_fortran}
%if 0%{?rhel} >= 7
ar cruv $FULLPATH/libgfortran_nonshared.a
%ifarch sparcv9 ppc
ar cruv $FULLPATH/64/libgfortran_nonshared.a
%endif
%ifarch %{multilib_64_archs}
ar cruv $FULLPATH/32/libgfortran_nonshared.a
%endif
%else
cp -a %{gcc_target_platform}/libgfortran/.libs/libgfortran_nonshared.a \
  $FULLPATH/libgfortran_nonshared.a
%ifarch sparcv9 ppc
cp -a %{gcc_target_platform}/64/libgfortran/.libs/libgfortran_nonshared.a \
  $FULLPATH/64/libgfortran_nonshared.a
%endif
%ifarch %{multilib_64_archs}
cp -a %{gcc_target_platform}/32/libgfortran/.libs/libgfortran_nonshared.a \
  $FULLPATH/32/libgfortran_nonshared.a
%endif
%endif
%endif

pushd $FULLPATH
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgomp.so.1 )' > libgomp.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' > libstdc++.so
%if %{build_fortran}
rm -f libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( -lgfortran_nonshared %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgfortran.so.3 AS_NEEDED ( -ldl ) )' > libgfortran.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo '/* GNU ld script */
%{oformat}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/%{_lib}/libquadmath.so.0 )' > libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/%{_lib}/libquadmath.so.0 )' > libquadmath.so
%else
INPUT ( libquadmath.a )' > libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f libitm.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libitm.so.1 )' > libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libatomic.so.1 )' > libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libasan.so.0 )' > libasan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libtsan.so.0 )' > libtsan.so
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a .
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan_preinit.o $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLLPATH/
%endif

%ifarch sparcv9 ppc
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libstdc++.so.6 -lstdc++_nonshared )' > 64/libstdc++.so
%if %{build_fortran}
rm -f 64/libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( -lgfortran_nonshared %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libgfortran.so.3 AS_NEEDED ( -ldl ) )' > 64/libgfortran.so
%endif
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libgomp.so.1 )' > 64/libgomp.so
%if %{build_libquadmath}
rm -f 64/libquadmath.so
echo '/* GNU ld script */
%{oformat2}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/lib64/libquadmath.so.0 )' > 64/libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/lib64/libquadmath.so.0 )' > 64/libquadmath.so
%else
INPUT ( libquadmath.a )' > 64/libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f 64/libitm.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libitm.so.1 )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f 64/libatomic.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libatomic.so.1 )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f 64/libasan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libasan.so.0 )' > 64/libasan.so
%endif
mv -f %{buildroot}%{_prefix}/lib64/libsupc++.*a 64/
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/lib64/libgfortran.*a 64/
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/lib64/libquadmath.*a 64/
%endif
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++_nonshared.a libstdc++_nonshared.a
ln -sf ../lib64/libstdc++_nonshared.a 64/libstdc++_nonshared.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
ln -sf lib32/libasan_preinit.o libasan_preinit.o
ln -sf ../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libstdc++.so.6 -lstdc++_nonshared )' > 32/libstdc++.so
%if %{build_fortran}
rm -f 32/libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( -lgfortran_nonshared %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgfortran.so.3 AS_NEEDED ( -ldl ) )' > 32/libgfortran.so
%endif
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgomp.so.1 )' > 32/libgomp.so
%if %{build_libquadmath}
rm -f 32/libquadmath.so
echo '/* GNU ld script */
%{oformat2}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/lib/libquadmath.so.0 )' > 32/libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/lib/libquadmath.so.0 )' > 32/libquadmath.so
%else
INPUT ( libquadmath.a )' > 32/libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f 32/libitm.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libitm.so.1 )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f 32/libatomic.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libatomic.so.1 )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f 32/libasan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libasan.so.0 )' > 32/libasan.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libsupc++.*a 32/
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/lib/libgfortran.*a 32/
%endif
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/lib/libquadmath.*a 32/
%endif
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++_nonshared.a 32/libstdc++_nonshared.a
ln -sf lib64/libstdc++_nonshared.a libstdc++_nonshared.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
ln -sf ../lib32/libasan_preinit.o 32/libasan_preinit.o
ln -sf lib64/libasan_preinit.o libasan_preinit.o
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libstdc++_nonshared.a 32/libstdc++_nonshared.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libasan.a 32/libasan.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libasan_preinit.o 32/libasan_preinit.o
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a  -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a \
		    -o -name libquadmath.a \) -a -type f`
popd
%if %{build_fortran}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
%if %{build_libquadmath}
%if 0%{!?scl:1}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libitm.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
mv %{buildroot}%{_infodir}/libitm.info* %{buildroot}%{_root_infodir}/
%endif
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libasan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cd ..

%if 0%{!?scl:1}
for i in %{buildroot}%{_prefix}/bin/{*gcc,*++,gcov,gfortran,gcc-ar,gcc-nm,gcc-ranlib}; do
  mv -f $i ${i}48
done
%endif

# Remove binaries we will not be including, so that they don't end up in
# gcc48-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a,libmudflap*,libstdc++*,libgfortran*}
%if 0%{?scl:1}
rm -f %{buildroot}%{_prefix}/%{_lib}/{libquadmath*,libitm*,libatomic*,libasan*,libtsan*}
%endif
rm -f %{buildroot}%{_prefix}/%{_lib}/libgomp*
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}/lib/cpp
rm -f %{buildroot}/%{_lib}/libgcc_s*
rm -f %{buildroot}%{_prefix}/bin/{f95,gccbug,gnatgcc*}
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-{gcc-*,gfortran}
%if 0%{!?scl:1}
rm -f %{buildroot}%{_prefix}/bin/{*c++*,cc,cpp}
%endif
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-%{version} || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%endif
%endif

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{arch} > $FULLPATH/rpmver

%check
cd obj-%{gcc_target_platform}

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

# Test against the system libstdc++.so.6 + libstdc++_nonshared.a combo
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6{,.not_here}
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so{,.not_here}
ln -sf %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' \
  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared.a

# run the tests.
make %{?_smp_mflags} -k check RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
rm -rf gcc/testsuite.prev
mv gcc/testsuite{,.prev}
rm -f gcc/site.exp
make %{?_smp_mflags} -C gcc -k check-gcc check-g++ ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}' compat.exp struct-layout-1.exp" || :
mv gcc/testsuite/gcc/gcc.sum{,.sent}
mv gcc/testsuite/g++/g++.sum{,.sent}
( LC_ALL=C ../contrib/test_summary -o -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults2
rm -rf gcc/testsuite.compat
mv gcc/testsuite{,.compat}
mv gcc/testsuite{.prev,}
echo ====================TESTING=========================
cat testresults
echo ===`gcc --version | head -1` compatibility tests====
cat testresults2
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%if 0%{?scl:1}
%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi
%endif

%post -n %{?scl_prefix}libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n %{?scl_prefix}libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n %{?scl_prefix}libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{?scl:%{_root_infodir}}%{!?scl:%{_infodir}} %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{?scl:%{_root_infodir}}%{!?scl:%{_infodir}} %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan -p /sbin/ldconfig

%postun -n libasan -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig

%postun -n libtsan -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_prefix}/bin/gcc%{!?scl:48}
%{_prefix}/bin/gcov%{!?scl:48}
%{_prefix}/bin/gcc-ar%{!?scl:48}
%{_prefix}/bin/gcc-nm%{!?scl:48}
%{_prefix}/bin/gcc-ranlib%{!?scl:48}
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc%{!?scl:48}
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}%{?_gnu}-gcc%{!?scl:48}
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}%{?_gnu}-gcc%{!?scl:48}
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc%{!?scl:48}
%if 0%{?scl:1}
%{_prefix}/bin/cc
%{_prefix}/bin/cpp
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/cpp.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/gcc*
%{_infodir}/cpp*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%if 0%{?scl:1}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ar
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/as
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ld
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/nm
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ranlib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/strip
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%endif
%if %{build_cloog}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcloog-isl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan_preinit.o
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan_preinit.o
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%endif
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-g++%{!?scl:48}
%{_prefix}/bin/g++%{!?scl:48}
%if 0%{?scl:1}
%{_prefix}/bin/%{gcc_target_platform}-c++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++_nonshared.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n %{?scl_prefix}libstdc++%{!?scl:48}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++_nonshared.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++_nonshared.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++_nonshared.a
%endif
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%if %{build_libstdcxx_docs}
%files -n %{?scl_prefix}libstdc++%{!?scl:48}-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_fortran}
%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran%{!?scl:48}
%if 0%{?scl:1}
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran_nonshared.a
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran_nonshared.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran_nonshared.a
%endif
%doc rpm.doc/gfortran/*
%endif

%if %{build_libquadmath}
%if 0%{!?scl:1}
%files -n %{?scl_prefix}libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%doc rpm.doc/libquadmath/COPYING*
%endif

%files -n %{?scl_prefix}libquadmath-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*
%endif

%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libitm.so.1*
%{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info*

%files -n %{?scl_prefix}libitm-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif
%doc rpm.doc/libitm/ChangeLog*
%endif

%if %{build_libatomic}
%files -n libatomic
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libatomic.so.1*

%files -n %{?scl_prefix}libatomic-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libasan.so.0*

%files -n %{?scl_prefix}libasan-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libasan_preinit.o
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libasan_preinit.o
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libtsan.so.0*

%files -n %{?scl_prefix}libtsan-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%changelog
* Mon Mar 21 2016 Jim MacArthur <jim.macarthur@codethink.co.uk> 4.8.2-15.1.lf.0.0
- add legacy Fortran extensions such as AUTOMATIC, STRUCTURE, RECORD,
  continued include lines, .xor. operator, and under-specified arrays
- more lax conversions during assignments and comparisons if
  -std=extra-legacy is specified
- basic support for default field widths in format strings
- UNION and MAP support adapted from Fritz Reese's patches to the
  gfortran mailing list, enabled by -fdec-structure

* Sun Jul 20 2014 Jonathan Wakely <jwakely@redhat.com> 4.8.2-15.1
- add alternative std::condition_variable_any implementation (#1118870)

* Thu Feb 20 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-15
- fix exception spec instantiation ICE (#1067398, PR c++/60046)
- fix pch on aarch64 (#1058991, PR pch/60010)

* Wed Feb 19 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-14
- remove libgo P.224 elliptic curve (#1066539)
- fix -mcpu=power8 ICE (#1064242, PR target/60137)

* Tue Jan 21 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-13
- when removing -Wall from CXXFLAGS, if -Werror=format-security
  is present, add -Wformat to it, so that GCC builds on F21

* Mon Jan 20 2014 Jakub Jelinek <jakub@redhat.com> 4.8.2-12
- update from F21 gcc-4.8.2-12

* Thu Dec 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-7
- update from F21 gcc-4.8.2-7
  - fix PR middle-end/59470 for real

* Wed Dec 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-6
- temporarily revert PR middle-end/58956 to avoid libstdc++
  miscompilation on i?86 (PR middle-end/59470)

* Mon Dec  9 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-5
- update from F21 gcc-4.8.2-5 (#1038301)

* Mon Nov 11 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-4
- update from F21 gcc-4.8.2-4

* Thu Oct 17 2013 Jakub Jelinek <jakub@redhat.com> 4.8.2-1
- update from F21 gcc-4.8.2-1
  - GCC 4.8.2 release
- default to -fdiagnostics-color=auto rather than -fdiagnostics-color=never,
  if GCC_COLORS isn't in the environment; to turn it off by default, set
  GCC_COLORS= in the environment

* Thu Aug 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-4.1
- selected backports from gcc-4.8.1-6.el7 (#997109, #994244)
  - PRs middle-end/58041, rtl-optimization/57459, rtl-optimization/57878,
	sanitizer/56417, target/58067, tree-optimization/57980,
	tree-optimization/58145

* Mon Jul 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-4
- update from F19 gcc-4.8.1-4
  - backport some raw-string literal handling fixes (#981029)

* Thu Jun 13 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-2.1
- link -lgfortran_nonshared before libgfortran.so.3, so that
  #972921 hack works

* Wed Jun 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-2
- update from F19 gcc-4.8.1-2
  - backport backwards compatible alignment ABI fixes (#947197,
    PR target/56564)
- override _gfortran_stop_string, so that STOP alone is silent
  and STOP 'string' doesn't print backtrace (#972921)

* Fri Jun  7 2013 Jakub Jelinek <jakub@redhat.com> 4.8.1-1
- update from F19 gcc-4.8.1-1
  - backport Intel Silvermont enablement and tuning from trunk
  - backport 3 small AMD improvement patches from trunk
  - std::chrono::steady_clock now really steady
  - backport color diagnostics support from trunk, enable with
    -fdiagnostics-color=auto, -fdiagnostics-color=always or
    having non-empty GCC_COLORS variable in environment
  - backport -fstack-protector-strong support from trunk
  
* Fri May 10 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-5
- update from F19 gcc-4.8.0-5

* Fri Apr 19 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-3
- update from F19 gcc-4.8.0-3
- require gmp-devel (and for RHEL6 mpfr-devel) in *plugin-devel packages
  (#908577)

* Fri Apr 12 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-2
- update from F19 gcc-4.8.0-2

* Fri Mar 22 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-1
- update from F19 gcc-4.8.0-1
  - GCC 4.8.0 release

* Wed Mar 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.18
- update from F19 gcc-4.8.0-0.18
- fix up libstdc++_nonshared.a on i?86
- package libasan_preinit.o

* Sat Mar 16 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.17
- update from F19 gcc-4.8.0-0.17

* Thu Mar 14 2013 Marek Polacek <polacek@redhat.com>
- add ar and ranlib symlinks for gcc-ar and gcc-ranlib (#917777)
- fix up symlinks for libatomic, libitm, libasan, and libtsan (#916175)

* Wed Feb 20 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.14
- sync from F19 gcc-4.8.0-0.14
- don't Requires: libquadmath in *-libquadmath-devel on RHEL 5 and 6 (#912765)

* Fri Feb 15 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.13
- sync from F19 gcc-4.8.0-0.13
- fix up a multilib file conflict in libstdc++-devel on RHEL 5
- use system libquadmath for RHEL 7, instead of static convenience
  library

* Thu Feb 14 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.12
- sync from F19 gcc-4.8.0-0.12

* Tue Jan 29 2013 Jakub Jelinek <jakub@redhat.com> 4.8.0-0.7
- new package
