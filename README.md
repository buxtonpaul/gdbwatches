# gdbwatches
GDB Tui extension to provide Locals and Expressions windows

Add it to your gdb session by enabling tui and sourceing the script e.g.
```gdb
tui enable
source gdbwatches.py```

It will automatically add windows called watches and locals, as well as a layout called watchvars. The layout will be switched to automatically.

Adding watches is done by the function addwatch to add an expression to watch
Removing watches uses the removewatch function, passing the index to use.

![Screenshot](/Screenshot.png)

This requires a recent version of GDB compiled with Python support
Current released version (10.1) is broken with custom layouts, but the version in git has been fixed and you can pull in the fix from tui-layout.c from the gdb-10-branch