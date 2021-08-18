Name: {{{ git_name name="devlog" }}}
# Workaround til first tagged release
Version: 0.0.0
# Version: %(git tag | sed -n 's/^v//p' | sort --version-sort -r | head -n1)
Release: 1%{?dist}
Summary: Log your development process

License: MIT
URL: https://github.com/jcrd/devlog
VCS: {{{ git_vcs }}}
Source0: {{{ git_pack }}}

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%global debug_package %{nil}

%description
Log your development process.

%prep
{{{ git_setup_macro }}}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{_bindir}/devlog

%changelog
{{{ git_changelog }}}
