%global upstreamname ROCm-CompilerSupport
%global rocm_release 5.2
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

Name:           rocm-compilersupport
Version:        %{rocm_version}
Release:        2%{?dist}
Summary:        Various AMD ROCm LLVM related services

Url:            https://github.com/RadeonOpenCompute/ROCm-CompilerSupport
License:        NCSA
Source0:        https://github.com/RadeonOpenCompute/%{upstreamname}/archive/refs/tags/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

#https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/commit/5495595234e8fb7b1715429cfa41fe6d9c0e710c
Patch0:         0001-Detect-if-clang-is-static-or-shared.patch

#Revert one patch to avoid compilation issue:
# gfx1036 defines are not present in llvm 14 (should be in 15)
Patch100:       0001-Revert-Add-gfx1036.patch

BuildRequires:  cmake
BuildRequires:  clang-devel >= 14.0.0
BuildRequires:  lld-devel
BuildRequires:  llvm-devel >= 14.0.0
BuildRequires:  rocm-device-libs >= %(echo %{version} | sed 's/\.[0-9]*$/.0/')
BuildRequires:  zlib-devel

#Only the following architectures are useful for ROCm packages:
ExclusiveArch:  x86_64 aarch64 ppc64le

%description
This package currently contains one library, the Code Object Manager (Comgr)

%package -n rocm-comgr
Summary:        AMD ROCm LLVM Code Object Manager
Provides:       comgr(rocm) = %{rocm_release}

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
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

#These tests rely on features not present in upstream llvm:
sed -i -e "/compile_test/d" \
    -e "/compile_minimal_test/d" \
    -e "/compile_device_libs_test/d" \
    -e "/compile_source_with_device_libs_to_bc_test/d" \
    lib/comgr/test/CMakeLists.txt

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
%{_libdir}/libamd_comgr.so.2{,.*}
#Files already included:
%exclude %{_docdir}/amd_comgr/comgr/LICENSE.txt
%exclude %{_datadir}/amd_comgr/LICENSE.txt
%exclude %{_datadir}/amd_comgr/NOTICES.txt
%exclude %{_datadir}/amd_comgr/README.md

%files -n rocm-comgr-devel
%{_includedir}/amd_comgr.h
%{_libdir}/libamd_comgr.so
%{_libdir}/cmake/amd_comgr

%changelog
* Mon Sep 26 2022 Jeremy Newton <alexjnewt at hotmail dot com> - 5.2.0-2
- Fix HIP related issue

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
