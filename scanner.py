import os
import csv
from base64 import b64decode

def detect_delimiter(file_path, sample_size=1024):
    """Detect the delimiter used in a CSV file"""
    common_delimiters = [',', ';', '\t', '|']
    
    with open(file_path, 'r', encoding='utf-8') as file:
        sample = file.read(sample_size)
        first_line = sample.split('\n')[0]
        counts = {d: first_line.count(d) for d in common_delimiters}
        return max(counts.items(), key=lambda x: x[1])[0] if max(counts.values()) > 0 else ','

def get_csv_headers(file_path):
    """Extract headers from a CSV file"""
    try:
        delimiter = detect_delimiter(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader([file.readline().strip()], delimiter=delimiter)
            return [h.strip().lower() for h in next(reader) if h.strip()]
    except Exception as e:
        print(f"Error reading headers from {file_path}: {str(e)}")
        return []

def find_and_process_csv_files(start_path, encoded_sets, min_matches=3):
    """Process CSV files and remove those matching forbidden patterns"""
    files_removed = files_processed = 0
    
    # Decode sets once at the start
    decoded_sets = [[b64decode(col).decode().lower() for col in set_cols] for set_cols in encoded_sets]

    for root, _, files in os.walk(start_path):
        for file in files:
            if file.lower().endswith('.csv'):
                file_path = os.path.join(root, file)
                files_processed += 1
                
                try:
                    headers = set(get_csv_headers(file_path))
                    
                    # Check each decoded set
                    for idx, decoded_set in enumerate(decoded_sets, 1):
                        matches = headers.intersection(decoded_set)
                        if len(matches) >= min_matches:
                            try:
                                os.remove(file_path)
                                print(f"Removed: {file_path} (matched set {idx} by {len(matches)} matches)")
                                files_removed += 1
                                break
                            except Exception as e:
                                print(f"Error removing {file_path}: {str(e)}")
                
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
    
    return files_processed, files_removed

def main():
    # Encoded forbidden sets using standard base64
    forbidden_sets = [['UElE', 'QWdl', 'R2VuZGVy', 'Qm9keWxlbmd0aA==', 'Ym9keXdlaWdodA==', 'Qk1J', 'T1BMRUlESU5H', 'TElWSU5H', 'U1BPUlRT', 'V09SSw==', 'RElBR0NBVA==', 'ZGlhZ25vc2lz', 'VEVWUkVERU4=', 'U0NSRUVO', 'R0FNSU5H', 'U09DSUFMTUVESUE=', 'UEFJTlZBUw==', 'UEFJTlZBU19OT04=', 'Q0hBUVRPVFJBVw==', 'Q0hBUVRPVERJU0lORA==', 'U0RRRW1vdGlvbkM=', 'U0RRQ09ORFVDVEM=', 'U0RRSFlQQw==', 'U0RRUEVFUkM=', 'U0RRUFJPU09DSUFMQw==', 'U0RRQ0hJTEQ=', 'UENTUlVN', 'UENTTUFH', 'UENTSEVMUA==', 'UENTVE9U', 'TEVFRkJBUk9UT1Q=', 'RkFUU1VCUg==', 'RkFUQ09OUg==', 'RkFUTU9UUg==', 'RkFUUEhZU1I=', 'RkFUVE9UUg==', 'Q1NJ', 'Q0Y=', 'UE9UUw==', 'RElB', 'Q09OUw==', 'R0k=', 'V0lERVNQUlA=', 'SEVBRE1JRw==', 'V0VBSw=='], ['aWQ=', 'aGF2ZW5iZWtrZW4=', 'YmVydGhfbmFtZQ==', 'YWN0dWVsZV9kaWVwZ2FuZw==', 'bGVuZ3RlX3NjaGlwX2h1aWRpZw==', 'dHlwZV9zY2hpcA==', 'c2NoaXBfc3ViX2NhdA==', 'YWFudGFsX2xvb2RzZW4=', 'YWFudGFsX3NsZXBlcnM=', 'dm9yaWdlX2hhdmVu', 'bW9vcmluZ19pbmZvX2NvZGU=', 'ZGlyZWN0X3p3YWFpZW4=', 'Z2V1bGVy', 'UEVD', 'bGVuZ3RlX2tsYXNzZV9rZXk=', 'c25lbGhlaWRza2xhc3Nl', 'ZGF0dW10aWpkX3N0YXJ0cHVudA==', 'c25lbGhlaWRza2xhc3NlX25hYW0=', 'd2luZHJpY2h0aW5n', 'd2luZHN0b3Rlbg==', 'd2luZHNuZWxoZWlk', 'ZHJ1a3RlX3plZXZhYXJ0', 'ZHJ1a3RlX2Jpbm5lbnZhYXJ0', 'cmVpc3RpamRfYQ==', 'cmVpc3RpamRfYg==', 'cmVpc3RpamRfYw==', 'cmVpc3RpamRfdG90YWFs', 'dmFhcmFmc3RhbmRfYV9pbl9rbQ==', 'dmFhcmFmc3RhbmRfYl9pbl9rbQ==', 'dmFhcmFmc3RhbmRfY19pbl9rbQ==', 'dmFhcmFmc3RhbmRfdG90YWFsX2luX2tt']]
    
    print(f"Starting CSV file search in: {os.path.abspath('.')}")
    total_files, removed_files = find_and_process_csv_files('.', forbidden_sets)
    
    print(f"\nProcessed: {total_files} files")
    print(f"Removed: {removed_files} files")

if __name__ == "__main__":
    main()
