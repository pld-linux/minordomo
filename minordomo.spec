Summary:	Minordomo - minimalistic mailing lise manager.
Summary(pl):	Minordomo - minimalny menad¿er list pocztowych.
Name:		minordomo
Version:	0.7
Release:	1
License:	GPL
Group:		System/Listserver
Group(pl):	System/Serwery List Pocztowych
Source:		ftp://ftp.nodomainname.net/pub/%name/current/%name-%version.tar.gz
#Patch:		
Requires:	perl
Buildroot:	/tmp/%{name}-%{version}-root

%define	_prefix	/usr
%define	_sysconfdir	/etc
%define	_webdir	/home/httpd

%description


%description -l pl


%prep
%setup -q
%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_webdir}/cgi-bin,%{_sysconfdir}}
install -d $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist

install minordomo.pl $RPM_BUILD_ROOT%{_sbindir}
install minordomo.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/minordomo.conf
install minorweb.pl $RPM_BUILD_ROOT%{_webdir}/cgi-bin/

install libdir/sample-list/config $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist/
install libdir/sample-list/info $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist/
install libdir/sample-list/footer $RPM_BUILD_ROOT/var/lib/minordomo/defaultmailinglist/

gzip -9nf README CHANGELOG 

%post
if [ "`grep minordomo /etc/aliases`" = "" ]; then
echo "#Minordomo mailing list manager" >>/etc/aliases
echo -e "minordomo:	\042|/usr/sbin/minordimo.pl\042">>/etc/aliases
fi
if [ "`grep minordomo /etc/aliases`" = "" ]; then
echo " " >>/etc/aliases
echo "#Minordomo default mailing list " >>/etc/aliases
echo -e "defaultmailinglist:	\042|/usr/sbin/minordimo.pl defaultmailinglist\042">>/etc/aliases
fi

%postun
if [ "`grep minordomo /etc/aliases`" != "" ]; then
sed -e "s/minordomo/\#minordomo/" /etc/aliases >/tmp/.al
mv -f /tmp/.al /etc/aliases
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,CHANGELOG}.gz 
%attr(755,root,root) %{_sbindir}/minordomo.pl
%config %{_sysconfdir}/minordomo.conf
%attr(755,root,root) %{_webdir}/cgi-bin/minorweb.pl
%attr(644, mail,mail) /var/lib/minordomo/defaultmailinglist/*
