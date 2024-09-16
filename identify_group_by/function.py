import sqlglot

def has_group_by(sql):
    try:
        parsed = sqlglot.parse_one(sql)
        return any(isinstance(node, sqlglot.exp.Group) for node in parsed.walk())
    except Exception:
        return False