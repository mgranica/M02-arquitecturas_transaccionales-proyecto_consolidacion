from sqlalchemy import create_engine, text


def connect_db(
    host: str, database: str, user: str, password: str
):
    # create SQLalchemy engine
    return  create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

def insert_pictures_values(engine, file_id, file_path, size, date):
    ## TODO: reformulate insertion
    insert_stmt = f"INSERT INTO pictures (id, path, size, date) VALUES ('{file_id}', '{file_path}', '{size}', '{date}');"
    with engine.connect() as conn:
        conn.execute(text(insert_stmt))
        conn.commit()
        
def insert_tags_values(engine, file_id, tags, date):
    ## TODO: reformulate insertion
    for tag in tags:
        tag, confidence = tag["tag"], tag["confidence"]
        insert_stmt = f"INSERT INTO tags (tag, picture_id, confidence, date) VALUES ('{tag}', '{file_id}', '{confidence}', '{date}');"
        with engine.connect() as conn:
            conn.execute(text(insert_stmt))
            conn.commit()
            
def select_images(engine, min_date=None, max_date=None , tags=None):
    sql_query = """
        SELECT p.id, p.size, p.date,
            GROUP_CONCAT(t.tag) AS tags,
            GROUP_CONCAT(t.confidence) AS confidences
        FROM pictures p
        JOIN tags t ON p.id = t.picture_id
        WHERE 1=1
    """

    # Conditionally filters based on parameters
    params = {}
    if min_date is not None:
        sql_query += " AND p.date > :min_date"
        params["min_date"] = min_date
    if max_date is not None:
        sql_query += " AND p.date < :max_date"
        params["max_date"] = max_date
    if tags is not None:
        sql_query += " AND t.tags IN :tags"
        params["tags"]: ", ".join(tags)

    # Group by id, date, and size
    sql_query += " GROUP BY p.id, p.date, p.size"

    # Execute the query and return the results
    with engine.connect() as conn:
        result = conn.execute(text(sql_query), params)
        
    return result

def select_image(engine, picture_id):
    sql_query = """
        SELECT p.id, p.size, p.date,
            GROUP_CONCAT(t.tag) AS tags,
            GROUP_CONCAT(t.confidence) AS confidences
        FROM pictures p
        JOIN tags t ON p.id = t.picture_id
        WHERE p.id = :picture_id
    """
    # set params
    params = dict(picture_id=picture_id)
    # Execute the query and return the results
    with engine.connect() as conn:
        result = conn.execute(text(sql_query), params)
    columns = result.keys()
    
    return result

def select_tags(engine, min_date=None, max_date=None):
    sql_query = """
        SELECT t.tag tag,
            COUNT(DISTINCT(t.picture_id)) n_images,
            MIN(t.confidence) min_confidence,
            MAX(t.confidence) max_confidence,
            AVG(t.confidence) mean_confidence
        FROM tags t
        WHERE 1=1
    """

    # Conditionally filters based on parameters
    params = {}
    if min_date is not None:
        sql_query += " AND t.date > :min_date"
        params["min_date"] = min_date
    if max_date is not None:
        sql_query += " AND t.date < :max_date"
        params["max_date"] = max_date

    # Group by id, date, and size
    sql_query += " GROUP BY t.tag"

    # Execute the query and return the results
    with engine.connect() as conn:
        result = conn.execute(text(sql_query), params)

    return result