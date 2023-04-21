# The package follows LLVM's major version, but API version is still important:
%global comgr_maj_api_ver 2
%global comgr_full_api_ver %{comgr_maj_api_ver}.4.0
# LLVM information:
%global llvm_maj_ver 15
# If you bump LLVM, please reset bugfix_version to 0; I fork upstream sources,
# but I prepare the initial *.0 tag long before Fedora/EL picks up new LLVM.
# An LLVM update will require uploading new sources, contact mystro256 if FTBFS.
%global bugfix_version 1
%global upstreamname ROCm-CompilerSupport

Name:           rocm-compilersupport
Version:        %{llvm_maj_ver}.%{bugfix_version}
Release:        1%{?dist}
Summary:        Various AMD ROCm LLVM related services

Url:            https://github.com/RadeonOpenCompute/ROCm-CompilerSupport
License:        NCSA
# I fork upstream sources because they don't target stable LLVM, but rather the
# bleeding edge LLVM branch. My fork is a snapshot with bugfixes backported:
Source0:        https://github.com/Mystro256/%{upstreamname}/archive/refs/tags/%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  clang-devel >= %{llvm_maj_ver}
BuildRequires:  clang(major) = %{llvm_maj_ver}
BuildRequires:  lld-devel
BuildRequires:  llvm-devel(major) = %{llvm_maj_ver}
BuildRequires:  rocm-device-libs >= %{llvm_maj_ver}
BuildRequires:  zlib-devel

#Only the following architectures are useful for ROCm packages:
ExclusiveArch:  x86_64 aarch64 ppc64le

%description
This package currently contains one library, the Code Object Manager (Comgr)

%package -n rocm-comgr
Summary:        AMD ROCm LLVM Code Object Manager
Provides:       comgr(major) = %{comgr_maj_api_ver}
Provides:       rocm-comgr = %{comgr_full_api_ver}-%{release}

%description -n rocm-comgr
The AMD Code Object Manager (Comgr) is a shared library which provides
operations for creating and inspecting code objects.

%package -n rocm-comgr-devel
Summary:        AMD ROCm LLVM Code Object Manager
Requires:       rocm-comgr%{?_isa} = %{version}-%{release}

%description -n rocm-comgr-devel
The AMD Code Object Manager (Comgr) development package.

The API is documented in the header file:
"%{_includedir}/amd_comgr.h"

%prep
%autosetup -p1 -n %{upstreamname}-%{version}

##Fix issue wit HIP, where compilation flags are incorrect, see issue:
#https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/issues/49
#Remove redundant includes:
sed -i '/Args.push_back(HIPIncludePath/,+1d' lib/comgr/src/comgr-compiler.cpp
sed -i '/Args.push_back(ROCMIncludePath/,+1d' lib/comgr/src/comgr-compiler.cpp
#Source hard codes the libdir too:
sed -i 's/lib\(\/clang\)/%{_lib}\1/' lib/comgr/src/comgr-compiler.cpp

%build
%cmake -S lib/comgr -DCMAKE_BUILD_TYPE="RELEASE" -DBUILD_TESTING=ON
%cmake_build

%check
%cmake_build --target test

%install
%cmake_install

%files -n rocm-comgr
%license LICENSE.txt lib/comgr/NOTICES.txt
%doc lib/comgr/README.md
%{_libdir}/libamd_comgr.so.%{comgr_full_api_ver}
%{_libdir}/libamd_comgr.so.%{comgr_maj_api_ver}
#Files already included:
%exclude %{_docdir}/amd_comgr/LICENSE.txt
%exclude %{_docdir}/amd_comgr/NOTICES.txt
%exclude %{_docdir}/amd_comgr/README.md

%files -n rocm-comgr-devel
%{_includedir}/amd_comgr/amd_comgr.h
%{_libdir}/libamd_comgr.so
%{_libdir}/cmake/amd_comgr
#This header are deprecated and will be removed soon:
%{_includedir}/amd_comgr.h

%changelog
* Fri Apr 21 2023 Jeremy Newton <alexjnewt at hotmail dot com> - 15.1-1
- Update to 15.1 (forked sources for Fedora)

* Fri Jan 13 2023 Nikita Popov <npopov@redhat.com> - 5.4.1-2
- Rebuild against Clang 15.0.7

* Sun Dec 18 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.4.1-1
- Update to 5.4.1

* Tue Oct 04 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.3.0-1
- Update to 5.3.0

* Mon Sep 19 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.2.0-3
- Rebuilt against LLVM 15

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 03 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.2.0-1
- Update to 5.2.0

* Fri Jun 10 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.1.0-3
- Add comgr(rocm) provide

* Tue Apr 05 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.1.0-2
- Enable ppc64le

* Tue Mar 29 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.1.0-1
- Update to 5.1.0

* Fri Feb 11 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0.0-1
- Update to 5.0.0

* Mon Jan 24 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 4.5.2-1
- Initial package
