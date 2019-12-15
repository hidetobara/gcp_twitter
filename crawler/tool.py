
def strdt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")
def strd(dt):
    return dt.strftime("%Y-%m-%d")
def strpt(dt):
    return dt.year * 100 + dt.month


def insert_rows(client, rows, name="my_timeline"):
    if len(rows) == 0:
        return
    dataset_ref = client.dataset("source")
    table_ref = dataset_ref.table(name)
    table = client.get_table(table_ref)
    r = client.insert_rows_json(table, rows)
    print("insert_logs=", r, "table=", name)
