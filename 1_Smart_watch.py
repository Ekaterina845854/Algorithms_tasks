import csv
from varint import encode, decode_stream

def float_to_fixed_point(value):
    return round((value) * 1000)  

def fixed_point_to_float(value):
    return round((value / 1000), 3)

def delta_encode(values, prev_values):
    return [values[i] - prev_values[i] for i in range(len(values))]

def delta_decode(deltas, prev_values):
    return [prev_values[i] + deltas[i] for i in range(len(deltas))]

def process_csv_to_binary(input_csv, output_bin):
    with open(input_csv, 'r') as csvfile, open(output_bin, 'wb') as binfile:
        reader = csv.reader(csvfile)
        header = next(reader) 
        prev_values = [0, 0, 0]
        
        for row in reader:
            timestamp = row[0] 
            float_values = [float(value) for value in row[1:]] 
            fixed_values = [float_to_fixed_point(value) for value in float_values]
            deltas = delta_encode(fixed_values, prev_values)
            
            binfile.write(timestamp.encode('utf-8') + b'\n') 
            
            for delta in deltas:
                encoded_value = encode((delta << 1) ^ (delta >> 31)) 
                binfile.write(encoded_value)
            
            prev_values = fixed_values 

def decode_binary_to_csv(input_bin, output_csv):
    with open(input_bin, 'rb') as binfile, open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'x', 'y', 'z'])
        prev_values = [0, 0, 0]
        
        while True:
            timestamp_bytes = bytearray()
            while True:
                byte = binfile.read(1)
                if byte == b'\n' or not byte:
                    break
                timestamp_bytes.extend(byte)
            if not timestamp_bytes:
                return 
            
            timestamp = timestamp_bytes.decode('utf-8') 
            
            deltas = []
            for _ in range(3):
                byte = binfile.read(1)
                if not byte:
                    return  
                binfile.seek(-1, 1) 
                decoded_value = decode_stream(binfile)
                delta = (decoded_value >> 1) ^ -(decoded_value & 1) 
                deltas.append(delta)
            
            current_values = delta_decode(deltas, prev_values)
            float_values = [fixed_point_to_float(value) for value in current_values]
            writer.writerow([timestamp] + float_values) 
            prev_values = current_values 

process_csv_to_binary('input.csv', 'output.bin')
decode_binary_to_csv('output.bin', 'decoded.csv')

