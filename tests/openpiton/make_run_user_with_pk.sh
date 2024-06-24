user_prog=$1
echo running user program: $1.c
cd ../software
export PATH=${PITON_ROOT}/../tools/riscv_gcc/bin:$PATH
riscv64-unknown-elf-gcc -fno-builtin-printf ariane_api.c syscalls.c $1.c -o user_program.elf
cd ../pk
./make_embedded.bash
cp build/pk ../build/diag.exe
cd ../build
rv64_img
$PITON_ROOT/build/manycore/rel-0.1/obj_dir/Vcmp_top +wait_cycle_to_kill=10 +dowarningfinish +doerrorfinish +spc_pipe=0 +vcs+dumpvarsoff +TIMEOUT=10000000 +tg_seed=0  +good_trap0=000000008fffffff +bad_trap0=000000008fffffff +asm_diag_name=user_program.c +dv_root=$PITON_ROOT/piton
cd $PITON_ROOT/build
