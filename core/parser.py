def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        raw_data = f.read()
    return {"raw": raw_data} # this is just a stub for now, need to update.. 
