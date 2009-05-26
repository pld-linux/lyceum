Summary:	Lyceum - Enterprise Class Multi-User Blogging
Name:		lyceum
Version:	1.0.3
Release:	0.1
License:	GPL
Group:		Applications/Publishing
Source0:	http://lyceum.ibiblio.org/wp-content/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	f7297c7a1d7329a5d384962fcb215ebc
URL:		http://lyceum.ibiblio.org/
Requires:	php-gettext
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-xml
Requires:	php-xmlrpc
Requires:	webapps
Requires:	webserver(php) >= 5.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Lyceum is a stand-alone mutli-user blogging application, designed for
the enterprise. Utilizing the fantastic, intuitive WordPress blogging
engine at its core, Lyceum enables stand-alone, multi-user blog
services for small and high-volume environments.

%package setup
Summary:	Lyceum setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Lyceum
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Lyceum installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Lyceum po
pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q

find '(' -name '*.php' -o -name '*.js' -o -name '*.html' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_sysconfdir},%{_appdir}/wp-content/languages}
cp -a src/* $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	To finish your configuration DO NOT FORGET to:

	1) Create some MySQL database owned by some user
	2) Edit the file: %{_sysconfdir}/wp-config.php
	3) Install %{name}-setup
	4) Run a browser and visit: http://`hostname`/wordpress/wp-admin/install.php
EOF
fi

%post setup
chmod 660 %{_sysconfdir}/wp-config.php
chown root:http %{_sysconfdir}/wp-config.php

%postun setup
if [ "$1" = "0" ]; then
	chmod 640 %{_sysconfdir}/wp-config.php
	chown root:http %{_sysconfdir}/wp-config.php
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
#%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wp-config.php
%{_appdir}

%if 0
%files setup
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wp-secure
%attr(755,root,root) %{_bindir}/wp-setup
%{_appdir}/wp-secure.sh
%{_appdir}/wp-setup.sh
%{_appdir}/wp-admin
%endif
