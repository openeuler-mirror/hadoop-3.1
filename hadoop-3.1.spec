%global _hardened_build 1

%global hadoop_version %{version}
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service hadoop-journalnode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service hadoop-timelineserver.service

# Filter out undesired provides and requires
%global __requires_exclude_from ^%{_libdir}/%{real_name}/libhadoop.so$
%global __provides_exclude_from ^%{_libdir}/%{real_name}/.*$
%define real_name hadoop
Name:   hadoop-3.1
Version: 3.1.4
Release: 1
Summary: A software platform for processing vast amounts of data
# The BSD license file is missing
# https://issues.apache.org/jira/browse/HADOOP-9849
License: Apache-2.0 and MIT and BSD-2-Clause and EPL and Zlib and MPL-2.0
URL:     https://%{real_name}.apache.org
Source0: https://www.apache.org/dist/%{real_name}/core/%{real_name}-%{version}/%{real_name}-%{version}-src.tar.gz
Source1: %{real_name}-layout.sh
Source2: %{real_name}-hdfs.service.template
Source3: %{real_name}-mapreduce.service.template
Source4: %{real_name}-yarn.service.template
Source5: context.xml
Source6: %{real_name}.logrotate
Source7: %{real_name}-httpfs.sysconfig
Source8: hdfs-create-dirs
Source9: %{real_name}-tomcat-users.xml

BuildRoot: %{_tmppath}/%{real_name}-%{version}-%{release}-root
BuildRequires: java-1.8.0-openjdk-devel maven hostname maven-local tomcat cmake snappy openssl-devel 
BuildRequires: cyrus-sasl-devel chrpath systemd protobuf2-compiler protobuf2-devel protobuf2-java protobuf2
Requires: java-1.8.0-openjdk

%description
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

%package client
Summary: Libraries for Apache Hadoop clients
BuildArch: noarch
Requires: %{real_name}-common = %{version}-%{release}
Requires: %{real_name}-hdfs = %{version}-%{release}
Requires: %{real_name}-mapreduce = %{version}-%{release}
Requires: %{real_name}-yarn = %{version}-%{release}

%description client
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides libraries for Apache Hadoop clients.

%package common
Summary: Common files needed by Apache Hadoop daemons
BuildArch: noarch
Requires(pre): /usr/sbin/useradd
Obsoletes: %{real_name}-javadoc < 2.4.1-22%{?dist}

# These are required to meet the symlinks for the classpath
Requires: antlr-tool
Requires: apache-commons-beanutils
Requires: avalon-framework
Requires: avalon-logkit
Requires: checkstyle
Requires: coreutils
Requires: geronimo-jms
Requires: glassfish-jaxb
Requires: glassfish-jsp
Requires: glassfish-jsp-api
Requires: istack-commons
Requires: jakarta-commons-httpclient
Requires: java-base64
Requires: java-xmlbuilder
Requires: javamail
Requires: jettison
Requires: jetty8
Requires: jsr-311
Requires: mockito
Requires: objectweb-asm
Requires: objenesis
Requires: paranamer
Requires: relaxngDatatype
Requires: servlet3
Requires: snappy-java
Requires: txw2
Requires: which

%description common
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains common files and utilities needed by other Apache
Hadoop modules.

%package common-native
Summary: The native Apache Hadoop library file
Requires: %{real_name}-common = %{version}-%{release}

%description common-native
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains the native-hadoop library

%package devel
Summary: Headers for Apache Hadoop
Requires: libhdfs%{?_isa} = %{version}-%{release}

%description devel
Header files for Apache Hadoop's hdfs library and other utilities

%package hdfs
Summary: The Apache Hadoop Distributed File System
BuildArch: noarch
Requires: apache-commons-daemon-jsvc
Requires: %{real_name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description hdfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

The Hadoop Distributed File System (HDFS) is the primary storage system
used by Apache Hadoop applications.


%package httpfs
Summary: Provides web access to HDFS
BuildArch: noarch
Requires: apache-commons-dbcp
Requires: ecj >= 1:4.2.1-6
Requires: json_simple
Requires: tomcat
Requires: tomcat-lib
Requires: tomcat-native
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description httpfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides a server that provides HTTP REST API support for
the complete FileSystem/FileContext interface in HDFS.

%package -n libhdfs
Summary: The Apache Hadoop Filesystem Library
Requires: %{real_name}-hdfs = %{version}-%{release}
Requires: lzo

%description -n libhdfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides the Apache Hadoop Filesystem Library.

%package mapreduce
Summary: Apache Hadoop MapReduce (MRv2)
BuildArch: noarch
Requires: %{real_name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description mapreduce
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides Apache Hadoop MapReduce (MRv2).

%package mapreduce-examples
Summary: Apache Hadoop MapReduce (MRv2) examples
BuildArch: noarch
Requires: hsqldb

%description mapreduce-examples
This package contains mapreduce examples.

%package maven-plugin
Summary: Apache Hadoop maven plugin
BuildArch: noarch
Requires: maven

%description maven-plugin
The Apache Hadoop maven plugin

%package tests
Summary: Apache Hadoop test resources
BuildArch: noarch
Requires: %{real_name}-common = %{version}-%{release}
Requires: %{real_name}-hdfs = %{version}-%{release}
Requires: %{real_name}-mapreduce = %{version}-%{release}
Requires: %{real_name}-yarn = %{version}-%{release}

%description tests
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains test related resources for Apache Hadoop.

%package yarn
Summary: Apache Hadoop YARN
Requires: %{real_name}-common = %{version}-%{release}
Requires: %{real_name}-mapreduce = %{version}-%{release}
Requires: aopalliance
Requires: atinject
Requires: hamcrest
Requires: hawtjni
Requires: leveldbjni
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description yarn
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains Apache Hadoop YARN.

%package yarn-security
Summary: The ability to run Apache Hadoop YARN in secure mode
Requires: %{real_name}-yarn = %{version}-%{release}

%description yarn-security
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains files needed to run Apache Hadoop YARN in secure mode.

%prep
%autosetup -p1 -n %{real_name}-%{version}-src
mvn install:install-file -DgroupId=com.google.protobuf -DartifactId=protoc -Dversion=2.5.0 -Dclassifier=linux-aarch_64 -Dpackaging=exe -Dfile=/usr/bin/protoc

%pom_disable_module hadoop-minikdc hadoop-common-project
%pom_disable_module hadoop-pipes hadoop-tools
%pom_disable_module hadoop-azure hadoop-tools
%pom_disable_module hadoop-yarn-server-timelineservice-hbase-tests hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/pom.xml


# War files we don't want
%mvn_package :%{real_name}-auth-examples __noinstall
%mvn_package :%{real_name}-hdfs-httpfs __noinstall

# Parts we don't want to distribute
%mvn_package :%{real_name}-assemblies __noinstall

# Workaround for bz1012059
%mvn_package :%{real_name}-project-dist __noinstall

# Create separate file lists for packaging
%mvn_package :::tests: %{real_name}-tests
%mvn_package :%{real_name}-*-tests::{}: %{real_name}-tests
%mvn_package :%{real_name}-client*::{}: %{real_name}-client
%mvn_package :%{real_name}-hdfs*::{}: %{real_name}-hdfs
%mvn_package :%{real_name}-mapreduce-examples*::{}: %{real_name}-mapreduce-examples
%mvn_package :%{real_name}-mapreduce*::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-archives::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-datajoin::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-distcp::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-extras::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-gridmix::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-openstack::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-rumen::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-sls::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-streaming::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-tools*::{}: %{real_name}-mapreduce
%mvn_package :%{real_name}-maven-plugins::{}: %{real_name}-maven-plugin
%mvn_package :%{real_name}-minicluster::{}: %{real_name}-tests
%mvn_package :%{real_name}-yarn*::{}: %{real_name}-yarn

# Jar files that need to be overridden due to installation location
%mvn_file :%{real_name}-common::tests: %{real_name}/%{real_name}-common

%build
mvn -Dsnappy.lib=/usr/lib64 -Dbundle.snappy -Dcontainer-executor.conf.dir=%{_sysconfdir}/%{real_name} -Pdist,native -DskipTests -DskipIT -Dmaven.javadoc.skip=true package

%install
# Copy all jar files except those generated by the build
# $1 the src directory
# $2 the dest directory
copy_dep_jars()
{
  find $1 ! -name "hadoop-*.jar" -name "*.jar" | xargs install -m 0644 -t $2
  rm -f $2/tools-*.jar
}

# Create symlinks for jars from the build
# $1 the location to create the symlink
link_hadoop_jars()
{
  for f in `ls hadoop-* | grep -v tests | grep -v examples`
  do
    n=`echo $f | sed "s/-%{version}//"`
    if [ -L $1/$n ]
    then
      continue
    elif [ -e $1/$f ]
    then
      rm -f $1/$f $1/$n
    fi
    p=`find %{buildroot}/%{_jnidir} %{buildroot}/%{_javadir}/%{real_name} -name $n | sed "s#%{buildroot}##"`
    %{__ln_s} $p $1/$n
  done
}

%mvn_install

install -d -m 0755 %{buildroot}/%{_libdir}/%{real_name}
install -d -m 0755 %{buildroot}/%{_includedir}/%{real_name}
install -d -m 0755 %{buildroot}/%{_jnidir}/%{real_name}

install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/client/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/common/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/hdfs/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/hdfs/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps
install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/mapreduce/lib
install -d -m 0755 %{buildroot}/%{_datadir}/%{real_name}/yarn/lib
install -d -m 0755 %{buildroot}/%{_sysconfdir}/%{real_name}/tomcat/Catalina/localhost
install -d -m 0755 %{buildroot}/%{_sysconfdir}/logrotate.d
install -d -m 0755 %{buildroot}/%{_sysconfdir}/sysconfig
install -d -m 0755 %{buildroot}/%{_tmpfilesdir}
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/%{real_name}-hdfs
install -d -m 0755 %{buildroot}/%{_sharedstatedir}/tomcats/httpfs
install -d -m 0755 %{buildroot}/%{_var}/cache/%{real_name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/cache/%{real_name}-httpfs/temp
install -d -m 0755 %{buildroot}/%{_var}/cache/%{real_name}-httpfs/work
install -d -m 0755 %{buildroot}/%{_var}/cache/%{real_name}-mapreduce
install -d -m 0755 %{buildroot}/%{_var}/log/%{real_name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/log/%{real_name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/log/%{real_name}-httpfs
install -d -m 0755 %{buildroot}/%{_var}/log/%{real_name}-mapreduce
install -d -m 0755 %{buildroot}/%{_var}/run/%{real_name}-yarn
install -d -m 0755 %{buildroot}/%{_var}/run/%{real_name}-hdfs
install -d -m 0755 %{buildroot}/%{_var}/run/%{real_name}-mapreduce

basedir='%{real_name}-common-project/%{real_name}-common/target/%{real_name}-common-%{hadoop_version}'
hdfsdir='%{real_name}-hdfs-project/%{real_name}-hdfs/target/%{real_name}-hdfs-%{hadoop_version}'
httpfsdir='%{real_name}-hdfs-project/%{real_name}-hdfs-httpfs/target/%{real_name}-hdfs-httpfs-%{hadoop_version}'
mapreddir='%{real_name}-mapreduce-project/target/%{real_name}-mapreduce-%{hadoop_version}'
yarndir='%{real_name}-yarn-project/target/%{real_name}-yarn-project-%{hadoop_version}'

# copy jar package
install -d -m 0755 %{buildroot}/%{_datadir}/java/%{real_name}
install -d -m 0755 %{buildroot}/%{_datadir}/maven-poms/%{real_name}
# client
install -m 0755 %{real_name}-client-modules/%{real_name}-client/target/hadoop-client-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-client.jar >> .mfiles-hadoop-client 
install -m 0755 %{real_name}-client-modules/%{real_name}-client/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-client.pom 
echo %{_datadir}/maven-poms/%{real_name}/hadoop-client.pom >> .mfiles-hadoop-client
# common
install -m 0755 %{real_name}-common-project/%{real_name}-annotations/target/hadoop-annotations-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-annotations.jar
echo %{_datadir}/java/%{real_name}/hadoop-annotations.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-auth/target/hadoop-auth-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-auth.jar
echo %{_datadir}/java/%{real_name}/hadoop-auth.jar >> .mfiles
install -m 0755 %{real_name}-tools/%{real_name}-aws/target/hadoop-aws-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-aws.jar
echo %{_datadir}/java/%{real_name}/hadoop-aws.jar >> .mfiles
install -m 0755 %{real_name}-build-tools/target/hadoop-build-tools-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-build-tools.jar
echo %{_datadir}/java/%{real_name}/hadoop-build-tools.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-nfs/target/hadoop-nfs-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-nfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-nfs.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-common/target/hadoop-common-%{version}.jar %{buildroot}/%{_prefix}/lib/java/hadoop/hadoop-common.jar
echo %{_prefix}/lib/java/hadoop/hadoop-common.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-annotations/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-annotations.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-annotations.pom >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-auth/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-auth.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-auth.pom >> .mfiles
install -m 0755 %{real_name}-tools/%{real_name}-aws/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-aws.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-aws.pom >> .mfiles
install -m 0755 %{real_name}-build-tools/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-build-tools.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-build-tools.pom >> .mfiles
install -m 0755 %{real_name}-common-project/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-common-project.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-common-project.pom >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-common/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-common.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-common.pom >> .mfiles
install -m 0755 %{real_name}-dist/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-dist.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-dist.pom >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-nfs/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-nfs.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-nfs.pom >> .mfiles
install -m 0755 %{real_name}-project/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-project.pom 
echo %{_datadir}/maven-poms/%{real_name}/hadoop-project.pom >> .mfiles
echo %{_sysconfdir}/%{real_name}/hadoop-user-functions.sh.example >> .mfiles
echo %{_sysconfdir}/%{real_name}/shellprofile.d/example.sh >> .mfiles
echo %{_sysconfdir}/%{real_name}/workers >> .mfiles
echo %{_prefix}/libexec/hadoop-functions.sh >> .mfiles
echo %{_prefix}/libexec/hadoop-layout.sh.example >> .mfiles
echo %{_prefix}/sbin/workers.sh >> .mfiles
echo %{_datadir}/%{real_name}/common/hadoop-common.jar >> .mfiles
# hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-nfs/target/hadoop-hdfs-nfs-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-hdfs-nfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-nfs.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs/target/hadoop-hdfs-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-hdfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-nfs/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-hdfs-nfs.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-hdfs-nfs.pom >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-hdfs-project.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-hdfs-project.pom >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-hdfs.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-hdfs.pom >> .mfiles-hadoop-hdfs
echo %{_prefix}/libexec/shellprofile.d/hadoop-hdfs.sh >> .mfiles-hadoop-hdfs
# mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-archives/target/hadoop-archives-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-archives.jar
echo %{_datadir}/java/%{real_name}/hadoop-archives.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-datajoin/target/hadoop-datajoin-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-datajoin.jar
echo %{_datadir}/java/%{real_name}/hadoop-datajoin.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-distcp/target/hadoop-distcp-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-distcp.jar
echo %{_datadir}/java/%{real_name}/hadoop-distcp.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-extras/target/hadoop-extras-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-extras.jar
echo %{_datadir}/java/%{real_name}/hadoop-extras.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-gridmix/target/hadoop-gridmix-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-gridmix.jar
echo %{_datadir}/java/%{real_name}/hadoop-gridmix.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-app/target/hadoop-mapreduce-client-app-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-common/target/hadoop-mapreduce-client-common-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-common.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-core/target/hadoop-mapreduce-client-core-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-core.jar 
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-core.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-hs-plugins/target/hadoop-mapreduce-client-hs-plugins-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs-plugins.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs-plugins.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-hs/target/hadoop-mapreduce-client-hs-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-jobclient/target/hadoop-mapreduce-client-jobclient-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-shuffle/target/hadoop-mapreduce-client-shuffle-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-shuffle.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-shuffle.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-openstack/target/hadoop-openstack-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-openstack.jar
echo %{_datadir}/java/%{real_name}/hadoop-openstack.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-rumen/target/hadoop-rumen-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-rumen.jar
echo %{_datadir}/java/%{real_name}/hadoop-rumen.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-sls/target/hadoop-sls-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-sls.jar
echo %{_datadir}/java/%{real_name}/hadoop-sls.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-streaming/target/hadoop-streaming-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-streaming.jar
echo %{_datadir}/java/%{real_name}/hadoop-streaming.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-tools-dist/target/hadoop-tools-dist-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-tools-dist.jar
echo %{_datadir}/java/%{real_name}/hadoop-tools-dist.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-archives/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-archives.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-archives.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-datajoin/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-datajoin.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-datajoin.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-distcp/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-distcp.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-distcp.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-extras/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-extras.pom 
echo %{_datadir}/maven-poms/%{real_name}/hadoop-extras.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-gridmix/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-gridmix.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-gridmix.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-app/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-app.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-app.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-common/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-common.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-common.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-core/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-core.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-core.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-hs-plugins/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-hs-plugins.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-hs-plugins.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-hs/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-hs.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-hs.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-jobclient/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-jobclient.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-jobclient.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-shuffle/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-shuffle.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-client-shuffle.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-openstack/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-openstack.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-openstack.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-rumen/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-rumen.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-rumen.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-sls/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-sls.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-sls.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-streaming/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-streaming.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-streaming.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-tools-dist/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-tools-dist.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-tools-dist.pom >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-tools.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-tools.pom >> .mfiles-hadoop-mapreduce
echo %{_prefix}/libexec/shellprofile.d/hadoop-mapreduce.sh >> .mfiles-hadoop-mapreduce
# mapreduce-examples
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-examples/target/hadoop-mapreduce-examples-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-examples.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-examples.jar >> .mfiles-hadoop-mapreduce-examples
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-examples/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-examples.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-examples.pom >> .mfiles-hadoop-mapreduce-examples
# maven-plugin
install -m 0755 %{real_name}-maven-plugins/target/hadoop-maven-plugins-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-maven-plugins.jar
echo %{_datadir}/java/%{real_name}/hadoop-maven-plugins.jar >> .mfiles-hadoop-maven-plugin
install -m 0755 %{real_name}-maven-plugins/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-maven-plugins.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-maven-plugins.pom >> .mfiles-hadoop-maven-plugin
# tests
install -m 0755 %{real_name}-client-modules/%{real_name}-client/target/hadoop-client-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-client-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-client-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-common-project/%{real_name}-common/target/hadoop-common-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-common-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-common-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs/target/hadoop-hdfs-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-hdfs-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-app/target/hadoop-mapreduce-client-app-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-jobclient/target/hadoop-mapreduce-client-jobclient-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-minicluster/target/hadoop-minicluster-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-minicluster.jar
echo %{_datadir}/java/%{real_name}/hadoop-minicluster.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-tools/%{real_name}-tools-dist/target/hadoop-tools-dist-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-tools-dist-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-tools-dist-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-common/target/hadoop-yarn-common-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-common-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-common-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-registry/target/hadoop-yarn-registry-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-registry-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-registry-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-sharedcachemanager/target/hadoop-yarn-server-sharedcachemanager-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-tests/target/hadoop-yarn-server-tests-%{version}-tests.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-tests-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-tests-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-tests/target/hadoop-yarn-server-tests-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-minicluster/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-minicluster.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-minicluster.pom >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-tests/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-tests.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-tests.pom >> .mfiles-hadoop-tests
# yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-api/target/hadoop-yarn-api-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-api.jar 
echo %{_datadir}/java/%{real_name}/hadoop-yarn-api.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-applications-distributedshell/target/hadoop-yarn-applications-distributedshell-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-applications-distributedshell.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-applications-distributedshell.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-applications-unmanaged-am-launcher/target/hadoop-yarn-applications-unmanaged-am-launcher-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-applications-unmanaged-am-launcher.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-applications-unmanaged-am-launcher.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-client/target/hadoop-yarn-client-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-client.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-common/target/hadoop-yarn-common-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-common.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-registry/target/hadoop-yarn-registry-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-registry.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-registry.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-applicationhistoryservice/target/hadoop-yarn-server-applicationhistoryservice-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-applicationhistoryservice.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-applicationhistoryservice.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-common/target/hadoop-yarn-server-common-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-common.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-sharedcachemanager/target/hadoop-yarn-server-sharedcachemanager-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-web-proxy/target/hadoop-yarn-server-web-proxy-%{version}.jar %{buildroot}/%{_datadir}/java/%{real_name}/hadoop-yarn-server-web-proxy.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-web-proxy.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-api/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-api.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-api.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/hadoop-yarn-applications-distributedshell/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-applications-distributedshell.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-applications-distributedshell.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/hadoop-yarn-applications-unmanaged-am-launcher/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-applications-unmanaged-am-launcher.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-applications-unmanaged-am-launcher.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-applications.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-applications.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-client/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-client.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-client.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-common/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-common.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-common.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-registry/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-registry.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-registry.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/hadoop-yarn-server-applicationhistoryservice/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-applicationhistoryservice.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-applicationhistoryservice.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/hadoop-yarn-server-common/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-common.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-common.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/hadoop-yarn-server-nodemanager/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-nodemanager.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-nodemanager.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/hadoop-yarn-server-resourcemanager/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-resourcemanager.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-resourcemanager.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/hadoop-yarn-server-sharedcachemanager/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-sharedcachemanager.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-sharedcachemanager.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/hadoop-yarn-server-web-proxy/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-web-proxy.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server-web-proxy.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-server.pom >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-site/pom.xml %{buildroot}/%{_datadir}/maven-poms/%{real_name}/hadoop-yarn-site.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-yarn-site.pom >> .mfiles-hadoop-yarn
echo %{_sysconfdir}/%{real_name}/yarnservice-log4j.properties >> .mfiles-hadoop-yarn
echo %{_prefix}/bin/container-executor >> .mfiles-hadoop-yarn
echo %{_prefix}/bin/test-container-executor >> .mfiles-hadoop-yarn
echo %{_prefix}/libexec/shellprofile.d/hadoop-yarn.sh >> .mfiles-hadoop-yarn
echo %{_prefix}/sbin/FederationStateStore/* >> .mfiles-hadoop-yarn
# copy script folders
for dir in bin libexec sbin
do
  cp -arf $basedir/$dir %{buildroot}/%{_prefix}
  cp -arf $hdfsdir/$dir %{buildroot}/%{_prefix}
  cp -arf $mapreddir/$dir %{buildroot}/%{_prefix}
  cp -arf $yarndir/$dir %{buildroot}/%{_prefix}
done

# This binary is obsoleted and causes a conflict with qt-devel
rm -rf %{buildroot}/%{_bindir}/rcc

# Duplicate files
rm -f %{buildroot}/%{_sbindir}/hdfs-config.sh

# copy config files
cp -arf $basedir/etc/* %{buildroot}/%{_sysconfdir}
cp -arf $httpfsdir/etc/* %{buildroot}/%{_sysconfdir}
cp -arf $mapreddir/etc/* %{buildroot}/%{_sysconfdir}
cp -arf $yarndir/etc/* %{buildroot}/%{_sysconfdir}

# copy binaries
cp -arf $basedir/lib/native/libhadoop.so* %{buildroot}/%{_libdir}/%{real_name}
chrpath --delete %{buildroot}/%{_libdir}/%{real_name}/*
cp -arf ./hadoop-hdfs-project/hadoop-hdfs-native-client/target/hadoop-hdfs-native-client-%{version}/include/hdfs.h %{buildroot}/%{_includedir}/%{real_name}
cp -arf ./hadoop-hdfs-project/hadoop-hdfs-native-client/target/hadoop-hdfs-native-client-%{version}/lib/native/libhdfs.so* %{buildroot}/%{_libdir}
chrpath --delete %{buildroot}/%{_libdir}/libhdfs*

# Not needed since httpfs is deployed with existing systemd setup
rm -f %{buildroot}/%{_sbindir}/httpfs.sh
rm -f %{buildroot}/%{_libexecdir}/httpfs-config.sh
rm -f %{buildroot}/%{_bindir}/httpfs-env.sh

# Remove files with .cmd extension
find %{buildroot} -name *.cmd | xargs rm -f 

# Modify hadoop-env.sh to point to correct locations for JAVA_HOME
# and JSVC_HOME.
sed -i "s|\${JAVA_HOME}|/usr/lib/jvm/jre|" %{buildroot}/%{_sysconfdir}/%{real_name}/%{real_name}-env.sh
sed -i "s|\${JSVC_HOME}|/usr/bin|" %{buildroot}/%{_sysconfdir}/%{real_name}/%{real_name}-env.sh

# Ensure the java provided DocumentBuilderFactory is used
sed -i "s|\(HADOOP_OPTS.*=.*\)\$HADOOP_CLIENT_OPTS|\1 -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl \$HADOOP_CLIENT_OPTS|" %{buildroot}/%{_sysconfdir}/%{real_name}/%{real_name}-env.sh
echo "export YARN_OPTS=\"\$YARN_OPTS -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl\"" >> %{buildroot}/%{_sysconfdir}/%{real_name}/yarn-env.sh

# Workaround for bz1012059
install -d -m 0755 %{buildroot}/%{_mavenpomdir}/
install -pm 644 hadoop-project-dist/pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{real_name}-%{real_name}-project-dist.pom
%{__ln_s} %{_jnidir}/%{real_name}/hadoop-common.jar %{buildroot}/%{_datadir}/%{real_name}/common
%{__ln_s} %{_javadir}/%{real_name}/hadoop-hdfs.jar %{buildroot}/%{_datadir}/%{real_name}/hdfs
%{__ln_s} %{_javadir}/%{real_name}/hadoop-client.jar %{buildroot}/%{_datadir}/%{real_name}/client

# client jar depenencies
copy_dep_jars hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib %{buildroot}/%{_datadir}/%{real_name}/client/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{real_name}/client/lib
pushd  hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/client/lib
popd
pushd  hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/client
popd

# common jar depenencies
copy_dep_jars $basedir/share/%{real_name}/common/lib %{buildroot}/%{_datadir}/%{real_name}/common/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{real_name}/common/lib
pushd $basedir/share/%{real_name}/common
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/common
popd
pushd $basedir/share/%{real_name}/common/lib
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/common/lib
popd

# hdfs jar dependencies
copy_dep_jars $hdfsdir/share/%{real_name}/hdfs/lib %{buildroot}/%{_datadir}/%{real_name}/hdfs/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{real_name}/hdfs/lib
%{__ln_s} %{_jnidir}/%{real_name}/%{real_name}-hdfs-bkjournal.jar %{buildroot}/%{_datadir}/%{real_name}/hdfs/lib
pushd $hdfsdir/share/%{real_name}/hdfs
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/hdfs
popd

# httpfs
# Create the webapp directory structure
pushd %{buildroot}/%{_sharedstatedir}/tomcats/httpfs
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/conf conf
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/lib lib
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/logs logs
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/temp temp
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/webapps webapps
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/work work
popd

# Copy the tomcat configuration and overlay with specific configuration bits.
# This is needed so the httpfs instance won't collide with a system running
# tomcat
for cfgfile in catalina.policy catalina.properties context.xml \
  tomcat.conf web.xml server.xml logging.properties;
do
  cp -a %{_sysconfdir}/tomcat/$cfgfile %{buildroot}/%{_sysconfdir}/%{real_name}/tomcat
done

# Replace, in place, the Tomcat configuration files delivered with the current
# Fedora release. See BZ#1295968 for some reason.
sed -i -e 's/8005/${httpfs.admin.port}/g' -e 's/8080/${httpfs.http.port}/g' %{buildroot}/%{_sysconfdir}/%{real_name}/tomcat/server.xml
sed -i -e 's/catalina.base/httpfs.log.dir/g' %{buildroot}/%{_sysconfdir}/%{real_name}/tomcat/logging.properties
# Given the permission, only the root and tomcat users can access to that file,
# not the build user. So, the build would fail here.
install -m 660 %{SOURCE9} %{buildroot}/%{_sysconfdir}/%{real_name}/tomcat/tomcat-users.xml

# Copy the httpfs webapp
cp -arf %{real_name}-hdfs-project/%{real_name}-hdfs-httpfs/target/classes/webapps/webhdfs %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps

# Tell tomcat to follow symlinks
install -d -m 0766 %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/META-INF/
cp %{SOURCE5} %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/META-INF/

# Remove the jars included in the webapp and create symlinks
rm -f %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib/tools*.jar
rm -f %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib/tomcat-*.jar
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib

pushd %{buildroot}/%{_datadir}/%{real_name}/httpfs/tomcat
  %{__ln_s} %{_datadir}/tomcat/bin bin
  %{__ln_s} %{_sysconfdir}/%{real_name}/tomcat conf
  %{__ln_s} %{_datadir}/tomcat/lib lib
  %{__ln_s} %{_var}/cache/%{real_name}-httpfs/temp temp
  %{__ln_s} %{_var}/cache/%{real_name}-httpfs/work work
  %{__ln_s} %{_var}/log/%{real_name}-httpfs logs
popd

# mapreduce jar dependencies
mrdir='%{real_name}-mapreduce-project/target/%{real_name}-mapreduce-%{hadoop_version}'
copy_dep_jars $mrdir/share/%{real_name}/mapreduce/lib %{buildroot}/%{_datadir}/%{real_name}/mapreduce/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{real_name}/mapreduce/lib
%{__ln_s} %{_javadir}/%{real_name}/%{real_name}-annotations.jar %{buildroot}/%{_datadir}/%{real_name}/mapreduce/lib
pushd $mrdir/share/%{real_name}/mapreduce
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/mapreduce
popd

# yarn jar dependencies
yarndir='%{real_name}-yarn-project/target/%{real_name}-yarn-project-%{hadoop_version}'
copy_dep_jars $yarndir/share/%{real_name}/yarn/lib %{buildroot}/%{_datadir}/%{real_name}/yarn/lib
%{_bindir}/xmvn-subst %{buildroot}/%{_datadir}/%{real_name}/yarn/lib
%{__ln_s} %{_javadir}/%{real_name}/%{real_name}-annotations.jar %{buildroot}/%{_datadir}/%{real_name}/yarn/lib
pushd $yarndir/share/%{real_name}/yarn
  link_hadoop_jars %{buildroot}/%{_datadir}/%{real_name}/yarn
popd

# Install hdfs webapp bits
cp -arf hadoop-hdfs-project/hadoop-hdfs/target/webapps/* %{buildroot}/%{_datadir}/%{real_name}/hdfs/webapps

# hadoop layout. Convert to appropriate lib location for 32 and 64 bit archs
lib=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$lib" = "%_libdir" ]; then
  echo "_libdir is not located in /usr.  Lib location is wrong"
  exit 1
fi
sed -e "s|HADOOP_COMMON_LIB_NATIVE_DIR\s*=.*|HADOOP_COMMON_LIB_NATIVE_DIR=$lib/%{real_name}|" %{SOURCE1} > %{buildroot}/%{_libexecdir}/%{real_name}-layout.sh

# systemd configuration
install -d -m 0755 %{buildroot}/%{_unitdir}/
for service in %{hdfs_services} %{mapreduce_services} %{yarn_services}
do
  s=`echo $service | cut -d'-' -f 2 | cut -d'.' -f 1`
  daemon=$s
  if [[ "%{hdfs_services}" == *$service* ]]
  then
    src=%{SOURCE2}
  elif [[ "%{mapreduce_services}" == *$service* ]]
  then
    src=%{SOURCE3}
  elif [[ "%{yarn_services}" == *$service* ]]
  then
    if [[ "$s" == "timelineserver" ]]
    then
      daemon='historyserver'
    fi
    src=%{SOURCE4}
  else
    echo "Failed to determine type of service for %service"
    exit 1
  fi
  sed -e "s|DAEMON|$daemon|g" $src > %{buildroot}/%{_unitdir}/%{real_name}-$s.service
done

cp -f %{SOURCE7} %{buildroot}/%{_sysconfdir}/sysconfig/tomcat@httpfs

# Ensure /var/run directories are recreated on boot
echo "d %{_var}/run/%{real_name}-yarn 0775 yarn hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{real_name}-yarn.conf
echo "d %{_var}/run/%{real_name}-hdfs 0775 hdfs hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{real_name}-hdfs.conf
echo "d %{_var}/run/%{real_name}-mapreduce 0775 mapred hadoop -" > %{buildroot}/%{_tmpfilesdir}/%{real_name}-mapreduce.conf

# logrotate config
for type in hdfs httpfs yarn mapreduce
do
  sed -e "s|NAME|$type|" %{SOURCE6} > %{buildroot}/%{_sysconfdir}/logrotate.d/%{real_name}-$type
done
sed -i "s|{|%{_var}/log/hadoop-hdfs/*.audit\n{|" %{buildroot}/%{_sysconfdir}/logrotate.d/%{real_name}-hdfs

# hdfs init script
install -m 755 %{SOURCE8} %{buildroot}/%{_sbindir}

%pretrans -p <lua> hdfs
path = "%{_datadir}/%{real_name}/hdfs/webapps"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%pre common
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop HDFS" --shell /sbin/nologin -M -r -g hdfs -G hadoop --home %{_sharedstatedir}/%{real_name}-hdfs hdfs

%pre mapreduce
getent group mapred >/dev/null || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop MapReduce" --shell /sbin/nologin -M -r -g mapred -G hadoop --home %{_var}/cache/%{real_name}-mapreduce mapred

%pre yarn
getent group yarn >/dev/null || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop Yarn" --shell /sbin/nologin -M -r -g yarn -G hadoop --home %{_var}/cache/%{real_name}-yarn yarn

%preun hdfs
%systemd_preun %{hdfs_services}

%preun mapreduce
%systemd_preun %{mapreduce_services}

%preun yarn
%systemd_preun %{yarn_services}

%post common-native -p /sbin/ldconfig

%post hdfs
# Change the home directory for the hdfs user
if [[ `getent passwd hdfs | cut -d: -f 6` != "%{_sharedstatedir}/%{real_name}-hdfs" ]]
then
  /usr/sbin/usermod -d %{_sharedstatedir}/%{real_name}-hdfs hdfs
fi

if [ $1 -gt 1 ]
then
  if [ -d %{_var}/cache/%{real_name}-hdfs ] && [ ! -L %{_var}/cache/%{real_name}-hdfs ]
  then
    # Move the existing hdfs data to the new location
    mv -f %{_var}/cache/%{real_name}-hdfs/* %{_sharedstatedir}/%{real_name}-hdfs/
  fi
fi
%systemd_post %{hdfs_services}

%post -n libhdfs -p /sbin/ldconfig

%post mapreduce
%systemd_post %{mapreduce_services}

%post yarn
%systemd_post %{yarn_services}

%postun common-native -p /sbin/ldconfig

%postun hdfs
%systemd_postun_with_restart %{hdfs_services}

if [ $1 -lt 1 ]
then
  # Remove the compatibility symlink
  rm -f %{_var}/cache/%{real_name}-hdfs
fi

%postun -n libhdfs -p /sbin/ldconfig

%postun mapreduce
%systemd_postun_with_restart %{mapreduce_services}

%postun yarn
%systemd_postun_with_restart %{yarn_services}

%posttrans hdfs
# Create a symlink to the new location for hdfs data in case the user changed
# the configuration file and the new one isn't in place to point to the
# correct location
if [ ! -e %{_var}/cache/%{real_name}-hdfs ]
then
  %{__ln_s} %{_sharedstatedir}/%{real_name}-hdfs %{_var}/cache
fi

%files -f .mfiles-%{real_name}-client client
%{_datadir}/%{real_name}/client

%files -f .mfiles common
%doc LICENSE.txt
%doc NOTICE.txt
%doc README.txt
%config(noreplace) %{_sysconfdir}/%{real_name}/core-site.xml
%config(noreplace) %{_sysconfdir}/%{real_name}/%{real_name}-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/%{real_name}-metrics2.properties
%config(noreplace) %{_sysconfdir}/%{real_name}/%{real_name}-policy.xml
%config(noreplace) %{_sysconfdir}/%{real_name}/log4j.properties
%config(noreplace) %{_sysconfdir}/%{real_name}/ssl-client.xml.example
%config(noreplace) %{_sysconfdir}/%{real_name}/ssl-server.xml.example
%config(noreplace) %{_sysconfdir}/%{real_name}/configuration.xsl

%dir %{_datadir}/%{real_name}
%dir %{_datadir}/%{real_name}/common
%{_datadir}/%{real_name}/common/lib
%{_libexecdir}/%{real_name}-config.sh
%{_libexecdir}/%{real_name}-layout.sh

# Workaround for bz1012059
%{_mavenpomdir}/JPP.%{real_name}-%{real_name}-project-dist.pom

%{_bindir}/%{real_name}
%{_sbindir}/%{real_name}-daemon.sh
%{_sbindir}/%{real_name}-daemons.sh
%{_sbindir}/start-all.sh
%{_sbindir}/start-balancer.sh
%{_sbindir}/start-dfs.sh
%{_sbindir}/start-secure-dns.sh
%{_sbindir}/stop-all.sh
%{_sbindir}/stop-balancer.sh
%{_sbindir}/stop-dfs.sh
%{_sbindir}/stop-secure-dns.sh

%files common-native
%{_libdir}/%{real_name}/libhadoop.*

%files devel
%{_includedir}/%{real_name}
%{_libdir}/libhdfs.so

%files -f .mfiles-%{real_name}-hdfs hdfs
%{_datadir}/%{real_name}/hdfs
%{_unitdir}/%{real_name}-datanode.service
%{_unitdir}/%{real_name}-namenode.service
%{_unitdir}/%{real_name}-journalnode.service
%{_unitdir}/%{real_name}-secondarynamenode.service
%{_unitdir}/%{real_name}-zkfc.service
%{_libexecdir}/hdfs-config.sh
%{_bindir}/hdfs
%{_sbindir}/distribute-exclude.sh
%{_sbindir}/refresh-namenodes.sh
%{_sbindir}/hdfs-create-dirs
%{_tmpfilesdir}/%{real_name}-hdfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/run/%{real_name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/log/%{real_name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_sharedstatedir}/%{real_name}-hdfs


%files httpfs
%config(noreplace) %{_sysconfdir}/sysconfig/tomcat@httpfs
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-log4j.properties
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-signature.secret
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-site.xml
%attr(-,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{real_name}/tomcat/*.*
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{real_name}/tomcat
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{real_name}/tomcat/Catalina
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{real_name}/tomcat/Catalina/localhost
%{_datadir}/%{real_name}/httpfs
%{_sharedstatedir}/tomcats/httpfs
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/log/%{real_name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/cache/%{real_name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/cache/%{real_name}-httpfs/temp
%attr(0775,root,tomcat) %dir %{_var}/cache/%{real_name}-httpfs/work

%files -n libhdfs
%{_libdir}/libhdfs.so.*

%files -f .mfiles-%{real_name}-mapreduce mapreduce
%config(noreplace) %{_sysconfdir}/%{real_name}/mapred-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{real_name}/mapred-site.xml
%{_datadir}/%{real_name}/mapreduce
%{_libexecdir}/mapred-config.sh
%{_unitdir}/%{real_name}-historyserver.service
%{_bindir}/mapred
%{_sbindir}/mr-jobhistory-daemon.sh
%{_tmpfilesdir}/%{real_name}-mapreduce.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/run/%{real_name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/log/%{real_name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/cache/%{real_name}-mapreduce

%files -f .mfiles-%{real_name}-mapreduce-examples mapreduce-examples

%files -f .mfiles-%{real_name}-maven-plugin maven-plugin

%files -f .mfiles-%{real_name}-tests tests

%files -f .mfiles-%{real_name}-yarn yarn
%config(noreplace) %{_sysconfdir}/%{real_name}/capacity-scheduler.xml
%config(noreplace) %{_sysconfdir}/%{real_name}/yarn-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/yarn-site.xml
%{_unitdir}/%{real_name}-nodemanager.service
%{_unitdir}/%{real_name}-proxyserver.service
%{_unitdir}/%{real_name}-resourcemanager.service
%{_unitdir}/%{real_name}-timelineserver.service
%{_libexecdir}/yarn-config.sh
%{_datadir}/%{real_name}/yarn
%{_bindir}/yarn
%{_sbindir}/yarn-daemon.sh
%{_sbindir}/yarn-daemons.sh
%{_sbindir}/start-yarn.sh
%{_sbindir}/stop-yarn.sh
%{_tmpfilesdir}/%{real_name}-yarn.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/run/%{real_name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/log/%{real_name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/cache/%{real_name}-yarn

%files yarn-security
%config(noreplace) %{_sysconfdir}/%{real_name}/container-executor.cfg

%changelog
* Fri Mar 12 2021 Ge Wang <wangge20@huawei.com> - 3.1.4-1
- Init package
