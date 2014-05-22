%define mysql_license   Commercial
%define python_version  %(python -c "import distutils.sysconfig as ds; print ds.get_python_version()")
%define name            mysql-utilities-commercial
%define version         %(python -c "import mysql.utilities as mu; print('{0}.{1}.{2}'.format(*mu.VERSION[0:3]))")
%define summary         MySQL Utilities contain a collection of scripts useful for managing and administering MySQL servers
%define vendor          Oracle
%define packager        Oracle and/or its affiliates Product Engineering Team <mysql-build@oss.oracle.com>
%define copyright       Copyright (c) 2010, 2014, Oracle and/or its affiliates. All rights reserved.

%global        product_suffix      -commercial
%global        doctrine             mysql-fabric-doctrine-1.4.0

# Following are given defined from the environment/command line:
#  version
#  release_info
#  _topdir

# Hack to use a pattern using %P in the find command
%define findpat %( echo "/%""P" )

# Prevent manual pages to be compressed (also does not strip binaries, etc.)
%global __os_install_post %{nil}

Name:           mysql-utilities%{product_suffix}
Version:        %{version}
Release:        1%{?dist}
Summary:        %{summary}

Group:          Development/Libraries
License:        %{copyright} Use is subject to license terms.  Under %{mysql_license} license as shown in the Description field.
Vendor:         %{vendor}
Packager:       %{packager}
URL:            http://dev.mysql.com/downloads/
Source0:        %{name}-commercial%{version}-py%{python_version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  python-devel > 2.6
Requires:       mysql-connector-python >= 1.2.1
AutoReq:        no

Prefix:			/usr

%description
%{release_info}

This is a release of MySQL Utilities. For the avoidance of
doubt, this particular copy of the software is released
under a commercial license and the GNU General Public
License does not apply.
MySQL Utilities is brought to you by Oracle.

%{copyright}

License information can be found in the COPYING file.

This distribution may include materials developed by third
parties. For license and attribution notices for these
materials, please refer to the documentation that accompanies
this distribution (see the "Licenses for Third-Party Components"
appendix) or view the online documentation at 
<http://dev.mysql.com/doc/>

%package       extra
Summary:       Additional files for mysql-utilities
Group:         Development/Libraries

%description   extra
This package contains additional files mysql-utilities such as a MySQL
Fabric support for Doctrine Object Relational Mapper.

%prep

%setup -q
unzip data/%{doctrine}*

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{python_sitelib}
mkdir -p %{buildroot}%{_mandir}
cp -a %{bdist_dir}mysql %{buildroot}%{python_sitelib}
cp -p %{bdist_dir}*.egg-info %{buildroot}%{python_sitelib}
cp -a %{bdist_dir}/usr/bin %{buildroot}%{_exec_prefix}/bin
cp -a %{bdist_dir}/docs %{buildroot}%{_mandir}

# Moved to sub package
rm  %{buildroot}%{_sysconfdir}/mysql/%{doctrine}*
cp -a %{doctrine} %{buildroot}%{_datadir}/%{name}/

rm %{buildroot}%{python_sitelib}/mysql/__init__.pyc


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{bdist_dir}README_com.txt
%doc %{bdist_dir}LICENSE_com.txt
%config(noreplace) %{_sysconfdir}/mysql/fabric.cfg
%dir %{_sysconfdir}/mysql
%{_bindir}/mysqlauditadmin
%{_bindir}/mysqlauditgrep
%{_bindir}/mysqldbcompare
%{_bindir}/mysqldbcopy
%{_bindir}/mysqldbexport
%{_bindir}/mysqldbimport
%{_bindir}/mysqldiff
%{_bindir}/mysqldiskusage
%{_bindir}/mysqlfailover
%{_bindir}/mysqlfabric
%{_bindir}/mysqlfrm
%{_bindir}/mysqlindexcheck
%{_bindir}/mysqlmetagrep
%{_bindir}/mysqlprocgrep
%{_bindir}/mysqlreplicate
%{_bindir}/mysqlrpladmin
%{_bindir}/mysqlrplcheck
%{_bindir}/mysqlrplshow
%{_bindir}/mysqlserverclone
%{_bindir}/mysqlserverinfo
%{_bindir}/mysqluc
%{_bindir}/mysqluserclone
%{_bindir}/mysqlrplms
%{_bindir}/mysqlrplsync
%{python_sitelib}/mysql
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
%{python_sitelib}/mysql_utilities-*.egg-info
%endif
%{_mandir}/man1/mysql*.1*

%files extra
%defattr(-, root, root, -)
%{_datadir}/%{name}

%post
touch %{python_sitelib}/mysql/__init__.py

%postun
if [ $1 == 0 ];
then
    # Try to remove the MySQL top package mysql/
    SUBPKGS=`ls --ignore=*.py{c,o} -m %{python_sitelib}/mysql`
    if [ "$SUBPKGS" == "__init__.py" ];
    then
        rm %{python_sitelib}/mysql/__init__.py* 2>/dev/null 1>&2
        # This should not fail, but show error if any
        rmdir %{python_sitelib}/mysql/
    fi
    exit 0
fi

%changelog
* Thu May 22 2014 Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.4.3-1
- Updated for commercial package

* Mon Jul 29 2013 Israel Gomez <israel.gomez@oracle.com> - 1.0.0

- Initial implementation, based on Geert Vanderkelen's implementation.
