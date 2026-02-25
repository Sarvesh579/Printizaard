from printer import PrinterManager

pm = PrinterManager()

print("Default printer:")
print(pm.get_default_printer())

print("\nPrinters:\n")

for p in pm.printers:
    print(p["name"], "→", p["status"])

print("\nEdge found at:")
print(pm.edge_path)