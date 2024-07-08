import base64

with open("edge-impulse-standalone.wasm", "rb") as wasm_file:
    wasm_base64 = base64.b64encode(wasm_file.read()).decode("utf-8")

with open("wasm_base64.txt", "w") as out_file:
    out_file.write(wasm_base64)
