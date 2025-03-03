import csv
from varint import encode, decode_stream
import struct

def float_to_fixed_point(value):
    return int(value * 1000)

def fixed_point_to_float(value):
    return value / 1000

def delta_encode(values, prev_values):
    return [values[i] - prev_values[i] for i in range(len(values))]

def delta_decode(deltas, prev_values):
    return [prev_values[i] + deltas[i] for i in range(len(deltas))]

def process_csv_to_binary(input_csv, output_bin):
    with open(input_csv, 'r') as csvfile, open(output_bin, 'wb') as binfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        num_columns = len(header) - 1

        binfile.write(struct.pack(f"<{len(header)}s", " ".join(header).encode('utf-8')))
        binfile.write(b'\n')

        prev_values = [0] * num_columns

        for row in reader:
            timestamp = row[0]
            float_values = [float(value) for value in row[1:]]
            fixed_values = [float_to_fixed_point(value) for value in float_values]
            deltas = delta_encode(fixed_values, prev_values)

            timestamp_encoded = struct.pack('<d', float(timestamp))
            binfile.write(timestamp_encoded)

            for delta in deltas:
                encoded_value = encode((delta << 1) ^ (delta >> 31))
                binfile.write(encoded_value)

            prev_values = fixed_values

def decode_binary_to_csv(input_bin, output_csv):
    with open(input_bin, 'rb') as binfile, open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        header_bytes = bytearray()
        while True:
            byte = binfile.read(1)
            if byte == b'\n' or not byte:
                break
            header_bytes.extend(byte)
        header = header_bytes.decode('utf-8').split()
        writer.writerow(header)

        num_columns = len(header) - 1
        prev_values = [0] * num_columns

        while True:
            timestamp_bytes = binfile.read(8)
            if not timestamp_bytes:
                break
            timestamp = struct.unpack('<d', timestamp_bytes)[0]

            deltas = []
            for _ in range(num_columns):
                byte = binfile.read(1)
                if not byte:
                    break
                binfile.seek(-1, 1)
                decoded_value = decode_stream(binfile)
                delta = (decoded_value >> 1) ^ -(decoded_value & 1)
                deltas.append(delta)

            if not deltas:
                break

            current_values = delta_decode(deltas, prev_values)
            float_values = [fixed_point_to_float(value) for value in current_values]
            writer.writerow([timestamp] + float_values)
            prev_values = current_values


if __name__ == "__main__":
    process_csv_to_binary('input.csv', 'output.bin')
    decode_binary_to_csv('output.bin', 'decoded.csv')
