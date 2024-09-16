import sqlglot
from sqlglot.expressions import Select, Column, Identifier
def extract_fields_recursive(sql_query):
    """
    Recursively extracts field names from all SELECT and GROUP BY clauses in the SQL query,
    including those within subqueries, excluding functions/operators in SELECT clauses.

    Parameters:
    - sql_query (str): The SQL query string.

    Returns:
    - list: A list of dictionaries, each containing 'select_fields' and 'group_by_fields' for each SELECT clause.
    """


    # List to hold the results from all SELECT clauses
    results = []

    # Parse the SQL query
    parsed = sqlglot.parse_one(sql_query)

    # Define a recursive function to traverse the AST
    def traverse(node):
        if isinstance(node, Select):
            # Extract fields from the current SELECT and GROUP BY clauses
            select_fields = []
            for select_expr in node.selects:
                if isinstance(select_expr, (Column, Identifier)):
                    select_fields.append(select_expr.sql())
            group_by_fields = []
            group_by = node.args.get('group')
            if group_by:
                for group_expr in group_by.expressions:
                    group_by_fields.append(group_expr.sql())

            # Add the extracted fields to the results list
            results.append({
                'select_fields': select_fields,
                'group_by_fields': group_by_fields
            })

        # Recursively traverse child nodes
        for child in node.args.values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, sqlglot.Expression):
                        traverse(item)
            elif isinstance(child, sqlglot.Expression):
                traverse(child)

    # Start traversal from the root node
    traverse(parsed)

    return results