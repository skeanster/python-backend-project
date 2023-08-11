from sqlalchemy.orm import class_mapper


def row2dict(row):
    return {col.name: getattr(row, col.name) for col in class_mapper(row.__class__).mapped_table.c}
