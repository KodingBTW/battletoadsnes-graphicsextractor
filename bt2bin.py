## Battletoads NES - Texts Graphics Extractor
## CR-32: 785DD088

import sys
import os

def decompress_rle(data, byte_flag_00, byte_flag_ff):
    decompressed_data = bytearray()
    i = 0
    while i < len(data):
        byte = data[i]
        i += 1
        if byte == byte_flag_00:  
            if i < len(data):
                repeat_count = data[i] 
                decompressed_data.extend([0x00] * repeat_count)
                i += 1
        elif byte == byte_flag_ff:  
            if i < len(data):
                repeat_count = data[i] 
                decompressed_data.extend([0xFF] * repeat_count)
                i += 1
        else:
            decompressed_data.append(byte)

    return decompressed_data

def compress_rle(data, byte_flag_00, byte_flag_ff):
    compressed_data = bytearray()
    i = 0
    while i < len(data):
        byte = data[i]
        if byte == 0x00:
            count = 1  
            while i + 1 < len(data) and data[i + 1] == 0x00:
                count += 1
                i += 1  
            if count > 1:
                compressed_data.append(byte_flag_00)  
                compressed_data.append(count) 
            else:
                compressed_data.append(byte)
        
        elif byte == 0xFF:
            count = 1  
            while i + 1 < len(data) and data[i + 1] == 0xFF:
                count += 1
                i += 1  
            if count > 1:
                compressed_data.append(byte_flag_ff) 
                compressed_data.append(count) 
            else:
                compressed_data.append(byte)
        
        else:
            compressed_data.append(byte)  
        
        i += 1

    return compressed_data

def decompress_fonts(data):
    decompressed_data = bytearray()
       
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        decompressed_data.extend(block)
    
    return decompressed_data

def compress_fonts(data):   
    compressed_data = bytearray()
    
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        compressed_data.extend(block)
    
    return compressed_data
    
def read_rom(rom_file, addr, size):
    with open(rom_file, 'rb') as f:
        f.seek(addr)
        data = f.read(size)
        return data

def export_data(out_file, data):
    with open(out_file, 'wb') as f:
        f.write(data)
        print(f"Decompressed {len(data)} bytes at file {out_file}.")

def import_data(file):
    with open(file, "rb") as f:
        data = f.read()
    return data

def write_rom(rom_file, data, addr, bank_size, file_name):
    if len(data) > bank_size:
        excess = len(data) - bank_size
        print(f"Error: file {file_name}, {excess} bytes exceed bank size.")
    else:
        free_space = bank_size - len(data)
        
        filled_data = data + b'\xFF' * free_space

        with open(rom_file, "r+b") as f:
            f.seek(addr)
            f.write(filled_data)
            print(f"File {file_name} inserted at {rom_file}.")
            print(f"Free space: {free_space} bytes filled with 0xFF.")

def main():
    if len(sys.argv) < 2:
        print("Usage: -d -decompress graphics")
        print("       -c -compress graphics")
        sys.exit(1)

    option = sys.argv[1]
    # Define the ROM PATCH
    rom_file = "Battletoads (USA).nes"
    # Fonts graphics
    fonts_output = "DecompressFonts.bin"
    fonts_bank = 0x83d6
    fonts_bank_size = 0x178
    # Map part1 graphic
    map1_output = "DecompressMap1.bin"
    map1_bank = 0x3b084
    map1_bank_size = 0xb4e
    # Map part2 graphic
    map2_output = "DecompressMap2.bin"
    map2_bank = 0x3bbc6
    map2_bank_size = 0xb01
    # Map part3 graphic
    map3_output = "DecompressMap3.bin"
    map3_bank = 0x3c689
    map3_bank_size = 0x88A
    # Map part4 graphic
    map4_output = "DecompressMap4.bin"
    map4_bank = 0x3cda7
    map4_bank_size = 0xb16
    
    if option == "-d":
        #read file
        fonts_compress = read_rom(rom_file, fonts_bank, fonts_bank_size)
        map1_compress = read_rom(rom_file, map1_bank, map1_bank_size)
        map2_compress = read_rom(rom_file, map2_bank, map2_bank_size)
        map3_compress = read_rom(rom_file, map3_bank, map3_bank_size)
        map4_compress = read_rom(rom_file, map4_bank, map4_bank_size)
        #decompress
        fonts_decompress = decompress_fonts(fonts_compress)
        map1_decompress = decompress_rle(map1_compress, 0x4D, 0x56)
        map2_decompress = decompress_rle(map2_compress, 0x72, 0x95)
        map3_decompress = decompress_rle(map3_compress, 0x17, 0x1D)
        map4_decompress = decompress_rle(map4_compress, 0x15, 0x28)
        #export bin
        export_data(fonts_output, fonts_decompress)
        export_data(map1_output, map1_decompress)
        export_data(map2_output, map2_decompress)
        export_data(map3_output, map3_decompress)
        export_data(map4_output, map4_decompress)
        
    elif option == "-c":

        #import bin
        fonts_decompress = import_data(fonts_output)
        map1_decompress = import_data(map1_output)
        map2_decompress = import_data(map2_output)
        map3_decompress = import_data(map3_output)
        map4_decompress = import_data(map4_output)
        #compress
        fonts_compress = compress_fonts(fonts_decompress)
        map1_compress = compress_rle(map1_decompress, 0x4D, 0x56)
        map2_compress = compress_rle(map2_decompress, 0x72, 0x95)
        map3_compress = compress_rle(map3_decompress, 0x17, 0x1D)
        map4_compress = compress_rle(map4_decompress, 0x15, 0x28)       
        #write rom
        write_rom(rom_file, fonts_compress, fonts_bank, fonts_bank_size, fonts_output)
        write_rom(rom_file, map1_compress, map1_bank, map1_bank_size, map1_output)
        write_rom(rom_file, map2_compress, map2_bank, map2_bank_size, map2_output)
        write_rom(rom_file, map3_compress, map3_bank, map3_bank_size, map3_output)
        write_rom(rom_file, map4_compress, map4_bank, map4_bank_size, map4_output)
         
    else:
        print("Usage: -d -decompress graphics")
        print("       -c -compress graphics")
        sys.exit(1)

if __name__ == "__main__":
    main()
