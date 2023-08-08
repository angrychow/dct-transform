import heapq
from collections import Counter

#encode a bytes type message with huffman encoding
def huffman_encoding(message):
    #get the frequency of each character in the message
    freq = Counter(message)
    #build a huffman tree
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    #get the encoding dictionary
    encoding_dict = dict(heapq.heappop(heap)[1:])
    #encode the message
    encoded_message = "".join(encoding_dict[character] for character in message)
    return encoding_dict, encoded_message


#decode a message with huffman encoding to bytes type
def huffman_decoding(encoding_dict, encoded_message):
    decoding_dict = {code: symbol.to_bytes(1, 'big') for symbol, code in encoding_dict.items()}
    current_code = ""
    decoded_message = b""
    for bit in encoded_message:
        current_code += bit
        if current_code in decoding_dict:
            symbol = decoding_dict[current_code]
            decoded_message += symbol
            current_code = ""
    return decoded_message




#比特填充、标志序列111111

def pad_bits(data):
    padded_data = ""
    count = 0
    for bit in data:
        padded_data += bit
        if bit == "1":
            count += 1
            if count == 5:
                padded_data += "0"
                count = 0
        else:
            count = 0
    return padded_data

def unpad_bits(data):
    unpadded_data = ""
    count = 0
    for bit in data:
        if bit == "1":
            count += 1
            unpadded_data += bit
        else:
            if(count != 5):
                unpadded_data += bit
            count = 0
    return unpadded_data


# #binary string to bytes
# def bits_to_bytes(data):
#     bytes_data = b""
#     for i in range(0, len(data), 8):
#         byte = data[i:i+8]
#         bytes_data += int(byte, 2).to_bytes(len(byte) // 8, byteorder="big")
#     return bytes_data

#message to binary string
def msg_to_bits(message):
    #DICT_NUM(8) (KEY 01111110 VAL 01111110)*DICT_NUM DATA
    encoding_dict, encoded_data = huffman_encoding(message.encode('utf-8'))
    #decode dec num len(encoding_dict) to bit
    bitstr = ''.join(format(byte, '08b') for byte in len(encoding_dict).to_bytes(4,'big'))
    for k,v in encoding_dict.items():
        bitstr = bitstr + pad_bits(''.join(format(byte, '08b') for byte in k.to_bytes(1,'big'))) + "01111110" +pad_bits(v) + "01111110"
    return bitstr + encoded_data

#binary string to message
def bits_to_msg(bits):
    dict_num = int(bits[:32],2)
    bits = bits[32:]
    encoding_dict = {}
    for i in range(dict_num):
        key = int(unpad_bits(bits[:bits.find("01111110")]),2)
        bits = bits[bits.find("01111110")+8:]
        val = unpad_bits(bits[:bits.find("01111110")])
        bits = bits[bits.find("01111110")+8:]
        encoding_dict[key] = val
    return huffman_decoding(encoding_dict, bits).decode('utf-8')

data = " Modern literature in most countries deals with social issues. For example, many contemporary novels of Africa depict the lives of ordinary people struggling against adversity. Further-more, poetry from America speaks out against social and economic oppression. In still another instance, modern European drama enacts the fate of the working man in his drab confrontation with life. Even films, popular songs, and folk dramas from all around the world, tell the story of the little man and his battle against the giants of impersonal corporations, remote governments, or aggressive neighboring nations."
bits = msg_to_bits(data)

print(len(bytes(data, 'utf-8'))*8)
print(len(bits))
decoded_data = bits_to_msg(bits)
print("Decoded Data:", decoded_data)



from difflib import SequenceMatcher

def find_string_diff(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    for opcode, start1, end1, start2, end2 in matcher.get_opcodes():
        if opcode == 'equal':
            print("相同: ", str1[start1:end1])
        elif opcode == 'insert':
            print("插入: ", str2[start2:end2])
        elif opcode == 'delete':
            print("删除: ", str1[start1:end1])
        elif opcode == 'replace':
            print("替换: ", str1[start1:end1], " -> ", str2[start2:end2])

# 示例用法
find_string_diff(data, decoded_data)