Summary:	Minordomo - minimalistic mailing lise manager
Summary(pl):	Minordomo - minimalny zarz±dca list pocztowych
Name:		minordomo
Version:	0.7.6.2
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.ndn.net/pub/minorfish/old/%{name}-%{version}.tar.gz
# Source0-md5:	395bf2164c89e4e016d4582250fb5bfc
PreReq:		smtpdaemon
Requires:	perl-base
Requires(post,postun):	grep
Requires(postun):	fileutils
Requires(postun):	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webdir		/home/services/httpd

%description
Minordomo is a minimalist mailing list manager. It can be considered a
feature limited replacement of majordomo.

%description -l pl
Minordomo jest minimalnym zarz±dc± list pocztowych. Mo¿e byæ uwa¿any
za zamiennik majordomo o ograniczonych mo¿liwo¶ciach.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_webdir}/cgi-bin,%{_sysconfdir}}
install -d $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist

install minordomo.pl $RPM_BUILD_ROOT%{_sbindir}
install minordomo.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/minordomo.conf
install minorweb.pl $RPM_BUILD_ROOT%{_webdir}/cgi-bin/

install sample-list/config $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist/
install sample-list/info $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist/
install sample-list/footer $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist/

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "`grep minordomo /etc/mail/aliases`" = "" ]; then
	umask 022
	echo "#Minordomo mailing list manager" >>/etc/mail/aliases
	echo -e "minordomo:	\042|/usr/sbin/minordimo.pl\042">>/etc/mail/aliases
	echo " " >>/etc/mail/aliases
	echo "#Minordomo default mailing list " >>/etc/mail/aliases
	echo -e "defaultmailinglist:	\042|/usr/sbin/minordimo.pl defaultmailinglist\042">>/etc/mail/aliases
fi

%postun
if [ "`grep minordomo /etc/aliases`" != "" ]; then
	umask 022
	sed -e "s/minordomo/\#minordomo/" /etc/mail/aliases >/etc/mail/aliases.rpmtmp
	mv -f /etc/mail/aliases.rpmtmp /etc/mail/aliases
fi

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_sbindir}/minordomo.pl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/minordomo.conf
%attr(755,root,root) %{_webdir}/cgi-bin/minorweb.pl
%dir /var/lib/minordomo
%dir /var/lib/minordomo/defaultmailinglist
%attr(644,mail,mail) /var/lib/minordomo/defaultmailinglist/*
