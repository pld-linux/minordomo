Summary:	Minordomo - minimalistic mailing lise manager.
Summary(pl):	Minordomo - minimalny menad¿er list pocztowych.
Name:		minordomo
Version:	0.7
Release:	0.1
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
install -d $RPM_BUILD_ROOT/var/lib/minordomo

install minordomo.pl $RPM_BUILD_ROOT%{_sbindir}
install minordomo.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/minordomo.conf
install minorweb.pl $RPM_BUILD_ROOT%{_webdir}/cgi-bin/

gzip -9nf README CHANGELOG 

%post
if [ "`grep minordomo %{_sysconfdir}/aliases`" ="" ]; then
echo "#Minordomo mailing list manager" >>%{_sysconfdir}/aliases
echo "minordomo:	""|%{_sbindir}/minordimo.pl"">>%{_sysconfdir}/aliases
done

%postun
if [ "`grep minordomo /etc/aliases`" != "" ]; then
sed -e "s/minordomo/\#minordomo/" /etc/aliases >/tmp/.al
mv -f /tmp/.al /etc/aliases
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.bz2 CHANGELOG.bz2 
%attr(755,root,root) %{_sbindir}/minordomo.pl
%config %{_sysconfdir}/minordomo.conf
%attr(755,root,root) %{_webdir}/cgi-bin/minorweb.pl
