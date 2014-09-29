Summary:        IprediaOS package repositories
Name:           iprediaos-repos
Version:        2
Release:        0.2
License:        MIT
Group:          System Environment/Base
URL:            http://git.ipredia.org/cgit/iprediaos-repos.git/
# tarball is created by running make archive in the git checkout
Source:         %{name}-%{version}.tar.bz2
Provides:       iprediaos-repos(%{version})
Requires:       system-release(%{version})
Requires:       iprediaos-repos-rawhide = %{version}-%{release}
BuildArch:      noarch

%description
IprediaOS package repository files for yum and dnf along with gpg public keys

%package anaconda
Summary:        IprediaOS product repo definitions for anaconda
Requires:       iprediaos-repos = %{version}-%{release}

%description anaconda
This package provides the product repo definitions for anaconda.

%package rawhide
Summary:        Rawhide repo definitions
Requires:       iprediaos-repos = %{version}-%{release}
Obsoletes:      iprediaos-release-rawhide <= 1

%description rawhide
This package provides the rawhide repo definitions.


%prep
%setup -q

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-iprediaos-1-primary, and archmap
#     says "iprediaos-1-primary: i386 x86_64",
#     RPM-GPG-KEY-iprediaos-1-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'iprediaos-1-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (iprediaos-1-primary -> iprediaos-1-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-iprediaos-%{version}-primary RPM-GPG-KEY-%{version}-iprediaos
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in iprediaos*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done


%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/iprediaos.repo
%config(noreplace) /etc/yum.repos.d/iprediaos-updates*.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%files anaconda
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/iprediaos-cloud.repo
%config(noreplace) /etc/yum.repos.d/iprediaos-server.repo
%config(noreplace) /etc/yum.repos.d/iprediaos-workstation.repo

%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/iprediaos-rawhide.repo

%changelog
* Wed Sep 10 2014 Dennis Gilmore <dennis@ausil.us> 22-0.2
- add repo files for the products

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 22-0.1
- setup for rawhide targeting f22

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.4
- Require fedora-repos-rawhide from main package
- have fedora-repos-rawhide obsolete fedora-release-rawhide

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.3
- remove %%clean and rm in %%install
- Provides:       fedora-repos(%%{version})
- Requires:       system-release(%%{version})
- change url to git repo
- add note on how to make a tarball

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.2
- use %%{version} not %%{dist_version} in symlink command

* Tue Jul 08 2014 Dennis Gilmore <dennis@ausil.us> 21-0.1
- Initial setup for fedora-repos
