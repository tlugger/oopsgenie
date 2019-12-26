def get_valid_colum_indices(full_cols, specified_cols):
    indices = []
    for column in specified_cols:
            # Validate columns to extract
            if column not in full_cols:
                return None
            indices.append(full_cols.index(column))
    return indices