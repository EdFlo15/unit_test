import sqlglot

def has_subquery(sql):
    try:
        parsed = sqlglot.parse_one(sql)
        return any(isinstance(node, sqlglot.exp.Subquery) for node in parsed.walk())
    except Exception:
        return False