# https://github.com/mongodb/mongo/wiki/Build-Mongodb-From-Source

Name:           unifi-mongodb
Version:        4.2.7
Release:        1%{?dist}
Summary:        Private MongoDB for UniFi
License:        SSPL
URL:            https://www.mongodb.org/

Source0:        https://github.com/mongodb/mongo/archive/r%{version}.tar.gz#/mongodb-%{version}.tar.gz

BuildRequires:  boost-devel >= 1.56
BuildRequires:  gcc-c++
BuildRequires:  gperftools-devel
BuildRequires:  libcurl-devel
BuildRequires:  libpcap-devel
BuildRequires:  libstemmer-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  python3-cheetah
BuildRequires:  python3-devel >= 3.7
BuildRequires:  python3-psutil
#BuildRequires:  python3-pymongo
#BuildRequires:  python3-PyYAML
BuildRequires:  python3-regex
BuildRequires:  python3-requests
BuildRequires:  python3-scons
#BuildRequires:  python3-typing
BuildRequires:  python3-yaml
BuildRequires:  snappy-devel
BuildRequires:  valgrind-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  zlib-devel

%description
Mongo (from "humongous") is a high-performance, open source, schema-free
document-oriented database. This package contains just the binaries
required to start a private copy of the database as part of the UniFi
controller.

%prep
%autosetup -n mongo-r%{version} -p1

%build
export LANG=C.UTF-8

# Prepare variables for building
cat > variables.list << EOF
#CCFLAGS="$(echo %{?optflags} | sed -e "s/-O. //" -e "s/-g //") -ffloat-store"
#LINKFLAGS="%{?__global_ldflags} -Wl,-z,noexecstack -Wl,--reduce-memory-overheads,--no-keep-memory"
CCFLAGS="%{optflags}"
VERBOSE=1
MONGO_VERSION="%{version}"
VARIANT_DIR="fedora"
EOF

scons core \
  %{?_smp_mflags} \
  --use-system-pcre \
  --use-system-boost \
  --use-system-snappy \
  --use-system-valgrind \
  --use-system-zlib \
  --use-system-stemmer \
  --use-system-tcmalloc \
  --use-system-yaml \
  --mmapv1=on \
  --wiredtiger=on \
  --ssl \
  --nostrip \
  --disable-warnings-as-errors \
  --variables-files=variables.list

%install
install -p -D -m 755 mongod %{buildroot}%{_libdir}/unifi/bin/mongod
install -p -D -m 755 mongos %{buildroot}%{_libdir}/unifi/bin/mongos
install -p -D -m 755 mongo %{buildroot}%{_libdir}/unifi/bin/mongo

%files
%license LICENSE-Community.txt
%{_libdir}/unifi/bin/mongo
%{_libdir}/unifi/bin/mongod
%{_libdir}/unifi/bin/mongos

%changelog
* Thu May 21 2020 Simone Caronni <negativo17@gmail.com> - 4.2.7-1
- Update to 4.2.7, use default system build flags.
- Switch to Python 3.

* Sun Feb 23 2020 Simone Caronni <negativo17@gmail.com> - 3.6.17-1
- Update to 3.6.17.

* Sun Oct 20 2019 Simone Caronni <negativo17@gmail.com> - 3.6.14-1
- First build.
