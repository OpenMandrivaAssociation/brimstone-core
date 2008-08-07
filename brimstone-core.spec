%define section         free
%define gcj_support     1

Name:           brimstone-core
Version:        0.2.9
Release:        %mkrel 5.0.4
Epoch:          0
Summary:        org.freecompany.brimstone
License:        MIT
Group:          Development/Java
URL:            http://www.freecompany.org/
# svn export https://svn.freecompany.org/public/brimstone/tags/brimstone-core-0.2.9 | yes t
# zip -9r brimstone-core-src-0.2.9.zip brimstone-core-0.2.9
Source0:        http://repository.freecompany.org/org/freecompany/brimstone/zips/brimstone-core-src-%{version}.zip
Source1:        brimstone-core-0.2.9-build.xml
Requires:       java >= 1.6
Requires:       util-services
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
BuildRequires:  util-services
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
org.freecompany.brimstone

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} build.xml
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit util-services)
export OPT_JAR_LIST="ant/ant-junit"
%ant jar javadoc test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%create_jar_links

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
