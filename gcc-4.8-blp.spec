Name:           gcc-4.8-blp
Version:        1.0.0
Release:        1%{?dist}
Summary:        Custom gcc/gfortran compiler

License:        GPLv3
URL:            https://github.com/CodethinkLabs/gcc/tree/jmac/legacy-support-4_8-I
Source0:        https://github.com/CodethinkLabs/gcc/archive/jmac/gcc-4.8-blp-1.0.0.tar.gz

BuildRequires: binutils >= 2.20.51.0.2-12
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gdb
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
Requires: cpp
Requires: binutils >= 2.20.51.0.2-12
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
Requires: libgcc
Requires: libgomp
Requires: libgfortran
Requires: libquadmath
Requires: libquadmath-devel
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
This gcc package provides support for compiling Fortran
programs and includes Bloomberg's custom libraries.

%prep
%setup -q


%build
%configure --enable-languages=fortran
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
