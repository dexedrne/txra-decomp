ENTRY(_start)
SECTIONS
{
    . = 0x08000000;
    .text : { build/rom.o(.text) }
}
