# rocm-compilersupport

The rocm-compilersupport package

Please note that this package is built from forked source code maintained by the
package maintainer (mystro256):
https://github.com/Mystro256/ROCm-CompilerSupport

This is because upstream targets bleeding edge LLVM (upstream "main" branch).

In order to reduce the need to bundle LLVM for ROCm use and reduce over all
complexity of ROCm in Fedora, it's easier just to branch the development tree of
this component when LLVM branches, and then backport fixes from newer ROCm
releases.

This fork will contain tags in the format of %{llvm_maj_ver}.%{bugfix_version},
where llvm_maj_ver is the target LLVM version, and bugfix_version is the bugfix
revision if patches are backported to the forked branch. When updating LLVM, we
should reset bugfix_version to 0, as the %{llvm_maj_ver}.0 tag will be created
well before Fedora updates LLVM.
