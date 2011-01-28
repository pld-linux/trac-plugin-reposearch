%define		trac_ver	0.12
%define		plugin		reposearch
Summary:	Plugin for searching the source repository in Trac
Name:		trac-plugin-%{plugin}
Version:	0.2
Release:	1
License:	BSD
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/reposearchplugin?old_path=/&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	8e2e52bfce53892409da7f9ef17f228d
URL:		http://trac-hacks.org/wiki/RepoSearchPlugin
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin allows users to search the source code repository.

%prep
%setup -q -n %{plugin}plugin
mv %{trac_ver}/* .

%{__sed} -i -e '1s,^#!.*python,#!%{__python},' update-index

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

# avoid random name conflicts
mv $RPM_BUILD_ROOT%{_bindir}/{,trac-reposearch-}update-index

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin "tracreposearch.search.*"

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/trac-reposearch-update-index
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/*-*.egg-info
