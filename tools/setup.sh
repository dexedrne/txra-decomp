#!/usr/bin/env bash
set -euo pipefail
prefix="${TXRA_TOOLS:-$HOME/opt}"
mkdir -p "$prefix"
archive=arm-gnu-toolchain-14.3.rel1.tar.xz
folder=arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi
if ! test -x "$prefix/$folder/bin/arm-none-eabi-gcc"; then
  curl -fL --retry 2 "https://developer.arm.com/-/media/Files/downloads/gnu/14.3.rel1/binrel/$folder.tar.xz" -o "$prefix/$archive"
  (cd "$prefix"; echo "8f6903f8ceb084d9227b9ef991490413014d991874a1e34074443c2a72b14dbd  $archive" | sha256sum -c -)
  tar -xJf "$prefix/$archive" -C "$prefix"
fi
python3 -m venv --without-pip "$prefix/txra-venv"
if ! "$prefix/txra-venv/bin/python" -m pip --version >/dev/null 2>&1; then
  curl -fL https://bootstrap.pypa.io/get-pip.py -o "$prefix/get-pip.py"
  "$prefix/txra-venv/bin/python" "$prefix/get-pip.py" 'pip==26.2.2'
fi
"$prefix/txra-venv/bin/python" -m pip install 'capstone==5.0.6'
revision=da598c1d918402c42c0c0d7128ba14567f3175e9
if ! test -d "$prefix/agbcc/.git"; then
  git clone https://github.com/pret/agbcc.git "$prefix/agbcc"
fi
if test "$(git -C "$prefix/agbcc" rev-parse HEAD)" != "$revision"; then
  git -C "$prefix/agbcc" checkout --detach "$revision"
fi
if ! test -x "$prefix/agbcc/old_agbcc"; then
  make -C "$prefix/agbcc/gcc" clean
  make -C "$prefix/agbcc/gcc" old -j1
  mv "$prefix/agbcc/gcc/old_agbcc" "$prefix/agbcc/old_agbcc"
fi
if ! test -x "$prefix/agbcc/agbcc_arm"; then
  # Keep configuration and host objects out of the shared compiler sources.
  arm_build=$(mktemp -d)
  trap 'rm -rf "$arm_build"' EXIT
  cp -a "$prefix/agbcc/gcc_arm" "$arm_build/gcc_arm"
  cp -a "$prefix/agbcc/include" "$arm_build/include"
  cp -a "$prefix/agbcc/libiberty" "$arm_build/libiberty"
  cp "$prefix/agbcc/config.if" "$prefix/agbcc/config.sub" "$prefix/agbcc/install.sh" "$arm_build/"
  (
    cd "$arm_build/gcc_arm"
    nice -n 15 ./configure --target=arm-elf --host=i386-linux-gnu
    nice -n 15 make -j4 cc1
  )
  cp "$arm_build/gcc_arm/cc1" "$prefix/agbcc/agbcc_arm"
  rm -rf "$arm_build"
  trap - EXIT
fi
if ! test -x "$prefix/agbcc/agbcc"; then
  # Some installed replacements require the standard compiler variant.
  make -C "$prefix/agbcc/gcc" clean
  make -C "$prefix/agbcc/gcc" normal -j1
  mv "$prefix/agbcc/gcc/agbcc" "$prefix/agbcc/agbcc"
fi
