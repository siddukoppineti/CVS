import csv

MONITOR_FILE = "fle_monitors.txt"
CSV_FILE = "Varun_list.csv"   # convert your xlsx to csv first
OUTPUT_FILE = "matched_monitors.csv"

def clean(v):
    return "" if v is None else str(v).strip()

def norm(v):
    return clean(v).lower()

def short_name(v):
    v = clean(v)
    return v.split(".", 1)[0].lower()

def find_col(headers, candidates):
    header_map = {norm(h): i for i, h in enumerate(headers)}
    for c in candidates:
        key = norm(c)
        if key in header_map:
            return header_map[key]
    return None

with open(MONITOR_FILE, "r", encoding="utf-8") as f:
    servers = [line.strip() for line in f if line.strip()]

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    rows = list(reader)

if not rows:
    raise SystemExit("CSV file is empty")

headers = rows[0]

name_idx = find_col(headers, ["Name"])
fqdn_idx = find_col(headers, ["Fully qualified domain name", "FQDN", "Fully Qualified Domain Name"])
app_idx = find_col(headers, ["Application Relationship"])
group_idx = find_col(headers, ["Support Group", "Assignment Group"])

lookup = {}

for row in rows[1:]:
    if not row:
        continue

    name_val = clean(row[name_idx]) if name_idx is not None and name_idx < len(row) else ""
    fqdn_val = clean(row[fqdn_idx]) if fqdn_idx is not None and fqdn_idx < len(row) else ""
    app_val = clean(row[app_idx]) if app_idx is not None and app_idx < len(row) else ""
    group_val = clean(row[group_idx]) if group_idx is not None and group_idx < len(row) else ""

    if name_val:
        lookup[norm(name_val)] = (app_val, group_val)
    if fqdn_val:
        lookup[norm(fqdn_val)] = (app_val, group_val)
        lookup[short_name(fqdn_val)] = (app_val, group_val)

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["monitor", "server_name", "application_name", "assignment_group"])

    for server in servers:
        app = "MISSING"
        group = "MISSING"

        key = norm(server)
        if key in lookup:
            app, group = lookup[key]
        else:
            sname = short_name(server)
            if sname in lookup:
                app, group = lookup[sname]

        writer.writerow(["file monitor", server, app or "MISSING", group or "MISSING"])

print(f"Created {OUTPUT_FILE}")
