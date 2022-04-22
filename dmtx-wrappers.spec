# TODO
# - fix PHP bindings
# - java bindings
# - .Net bindings
#
# Conditional build:
%bcond_with	dotnet	# .NET binding
%bcond_with	java	# Java binding
%bcond_with	php	# PHP binding (not ready for 7+)
%bcond_without	python	# Python binding
%bcond_without	ruby	# Ruby binding
%bcond_without	vala	# Vala binding

Summary:	libdmtx wrappers
Summary(pl.UTF-8):	Przejściówki do libdmtx
Name:		dmtx-wrappers
Version:	0.7.3
%define	gitref	61072c30ebbc7bb11a54fbc8869af3e868879a40
%define	snap	20141125
Release:	0.%{snap}.1
License:	LGPL v2.1+, GPL v2+
Group:		Libraries
Source0:	https://github.com/dmtx/dmtx-wrappers/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	cb19f1ead190d8183cc36f41f4919224
URL:		https://github.com/dmtx/dmtx-wrappers
BuildRequires:	libdmtx-devel >= 0.7.3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.410
%if %{with php}
BuildRequires:	%{php_name}-devel
%endif
%if %{with python}
BuildRequires:	python-devel >= 1:2.5
%endif
%if %{with ruby}
BuildRequires:	ruby
BuildRequires:	ruby-devel
%endif
%if %{with vala}
BuildRequires:	pkgconfig
BuildRequires:	vala
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdmtx wrappers.

%description -l pl.UTF-8
Przejściówki do libdmtx.

%package -n %{php_name}-dmtx
Summary:	PHP bindings for libdmtx
Summary(pl.UTF-8):	Wiązania PHP do libdmtx
License:	GPL v2+
Group:		Development/Languages/PHP
Requires:	libdmtx >= 0.7.3
%{?requires_php_extension}
Provides:	php(dmtx) = %{version}
Obsoletes:	php-libdmtx < 0.7.2-4

%description -n %{php_name}-dmtx
This package contains bindings for using libdmtx from PHP.

%description -n %{php_name}-dmtx -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie biblioteki libdmtx
z poziomu PHP.

%package -n python-pydmtx
Summary:	Python bindings for libdmtx
Summary(pl.UTF-8):	Wiązania Pyhona do libdmtx
License:	LGPL v2.1+
Group:		Libraries/Python
Requires:	libdmtx >= 0.7.3
Obsoletes:	python-libdmtx < 0.7.2-4

%description -n python-pydmtx
This package contains bindings for using libdmtx from Python.

%description -n python-pydmtx -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie biblioteki libdmtx
z poziomu Pythona.

%package -n ruby-Rdmtx
Summary:	Ruby bindings for libdmtx
Summary(pl.UTF-8):	Wiązania języka Ruby do libdmtx
License:	LGPL v2.1+
Group:		Libraries
Requires:	libdmtx >= 0.7.3
Obsoletes:	ruby-libdmtx < 0.7.3

%description -n ruby-Rdmtx
This package contains bindings for using libdmtx from Ruby.

%description -n ruby-Rdmtx -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie biblioteki libdmtx
z poziomu języka Ruby.

%package -n vala-libdmtx
Summary:	Vala bindings for libdmtx
Summary(pl.UTF-8):	Wiązania języka Vala do libdmtx
License:	LGPL v2.1+
Group:		Libraries
Requires:	libdmtx-devel >= 0.7.3
Requires:	vala
BuildArch:	noarch

%description -n vala-libdmtx
This package contains bindings for using libdmtx from Vala.

%description -n vala-libdmtx -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie biblioteki libdmtx
z poziomu języka Vala.

%prep
%setup -q -n %{name}-%{gitref}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_java:--enable-java} \
	%{?with_dotnet:--enable-net} \
	%{?with_vala:--enable-vala}

%{__make}

%if %{with php}
cd php
phpize
%configure \
       --disable-static

%{__make}
cd ..
%endif

%if %{with python}
cd python
%py_build

# not ready for py3 currently
cd ..
%endif

%if %{with ruby}
cd ruby
%{__ruby} extconf.rb
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with php}
%{__make} -C php install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/dmtx.ini
; Enable dmtx extension module
extension=dmtx.so
EOF
%endif

%if %{with python}
cd python
%py_install

%py_postclean
cd ..
%endif

%if %{with ruby}
%{__make} -C ruby install \
	DESTDIR=$RPM_BUILD_ROOT \
	RUBYARCHDIR=$RPM_BUILD_ROOT%{ruby_vendorarchdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with php}
%files -n %{php_name}-dmtx
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog KNOWNBUG NEWS TODO php/README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/dmtx.ini
%attr(755,root,root) %{php_extensiondir}/dmtx.so
%endif

%if %{with python}
%files -n python-pydmtx
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog KNOWNBUG NEWS TODO python/README
%{py_sitedir}/pydmtx.py[co]
%attr(755,root,root) %{py_sitedir}/_pydmtx.so
%{py_sitedir}/pydmtx-0.1-py*.egg-info
%endif

%if %{with ruby}
%files -n ruby-Rdmtx
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog KNOWNBUG NEWS TODO ruby/README
%attr(755,root,root) %{ruby_vendorarchdir}/Rdmtx.so
%endif

%if %{with vala}
%files -n vala-libdmtx
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog KNOWNBUG NEWS TODO vala/README
%{_datadir}/vala/vapi/libdmtx.vapi
%endif
