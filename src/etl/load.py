from src.database.connection import get_connection

CHUNK_SIZE = 1000


def chunked(rows, size=CHUNK_SIZE):
    for index in range(0, len(rows), size):
        yield rows[index : index + size]


def load_all_tables(tables):
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        card_ids = [card["card_id"] for card in tables["cards"]]

        affected = {
            "cards": load_cards(cursor, tables["cards"]),
            "sets": load_sets(cursor, tables["sets"]),
            "rarity_types": load_rarity_types(cursor, tables["rarity_types"]),
            "deleted_child_rows": delete_replaceable_child_rows(cursor, card_ids),
            "card_printings": insert_many(cursor, card_printings_sql(), tables["card_printings"]),
            "card_images": load_card_images(cursor, tables["card_images"]),
            "card_price_history": load_card_price_history(
                cursor, tables["card_price_history"]
            ),
            "card_banlist": load_card_banlist(cursor, tables["card_banlist"]),
            "card_typelines": insert_many(
                cursor, card_typelines_sql(), tables["card_typelines"]
            ),
            "card_linkmarkers": insert_many(
                cursor, card_linkmarkers_sql(), tables["card_linkmarkers"]
            ),
        }

        connection.commit()
        return affected
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def delete_replaceable_child_rows(cursor, card_ids):
    if not card_ids:
        return 0

    total_deleted = 0
    tables = (
        "card_printings",
        "card_images",
        "card_banlist",
        "card_typelines",
        "card_linkmarkers",
    )

    for table in tables:
        for ids in chunked(card_ids):
            placeholders = ", ".join(["%s"] * len(ids))
            cursor.execute(
                f"DELETE FROM {table} WHERE card_id IN ({placeholders})", ids
            )
            total_deleted += cursor.rowcount

    return total_deleted


def insert_many(cursor, sql, rows):
    if not rows:
        return 0

    total = 0
    for chunk in chunked(rows):
        cursor.executemany(sql, chunk)
        total += cursor.rowcount

    return total


def load_cards(cursor, cards):
    return insert_many(cursor, cards_sql(), cards)


def load_sets(cursor, sets):
    return insert_many(cursor, sets_sql(), sets)


def load_rarity_types(cursor, rarities):
    return insert_many(cursor, rarity_types_sql(), rarities)


def load_card_images(cursor, card_images):
    return insert_many(cursor, card_images_sql(), card_images)


def load_card_price_history(cursor, card_price_history):
    return insert_many(cursor, card_price_history_sql(), card_price_history)


def load_card_banlist(cursor, card_banlist):
    return insert_many(cursor, card_banlist_sql(), card_banlist)


def cards_sql():
    return """
        INSERT INTO cards (
            card_id,
            name,
            card_type,
            human_readable_card_type,
            frame_type,
            description,
            race,
            archetype,
            ygoprodeck_url,
            atk,
            def,
            attribute,
            level,
            scale,
            pendulum_description,
            monster_description,
            link_value
        ) VALUES (
            %(card_id)s,
            %(name)s,
            %(card_type)s,
            %(human_readable_card_type)s,
            %(frame_type)s,
            %(description)s,
            %(race)s,
            %(archetype)s,
            %(ygoprodeck_url)s,
            %(atk)s,
            %(def)s,
            %(attribute)s,
            %(level)s,
            %(scale)s,
            %(pendulum_description)s,
            %(monster_description)s,
            %(link_value)s
        )
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            card_type = VALUES(card_type),
            human_readable_card_type = VALUES(human_readable_card_type),
            frame_type = VALUES(frame_type),
            description = VALUES(description),
            race = VALUES(race),
            archetype = VALUES(archetype),
            ygoprodeck_url = VALUES(ygoprodeck_url),
            atk = VALUES(atk),
            def = VALUES(def),
            attribute = VALUES(attribute),
            level = VALUES(level),
            scale = VALUES(scale),
            pendulum_description = VALUES(pendulum_description),
            monster_description = VALUES(monster_description),
            link_value = VALUES(link_value)
    """


def card_printings_sql():
    return """
        INSERT INTO card_printings (
            card_id,
            set_id,
            rarity_id,
            set_code,
            raw_rarity_name,
            raw_rarity_code,
            rarity_source_quality,
            set_price_usd
        ) VALUES (
            %(card_id)s,
            (SELECT set_id FROM sets WHERE set_name = %(set_name)s),
            (
                SELECT rarity_id
                FROM rarity_types
                WHERE rarity_name = %(rarity_name)s
                    AND rarity_code = %(rarity_code)s
            ),
            %(set_code)s,
            %(raw_rarity_name)s,
            %(raw_rarity_code)s,
            %(rarity_source_quality)s,
            %(set_price_usd)s
        )
    """


def sets_sql():
    return """
        INSERT INTO sets (
            set_name
        ) VALUES (
            %(set_name)s
        )
        ON DUPLICATE KEY UPDATE
            set_name = VALUES(set_name)
    """


def rarity_types_sql():
    return """
        INSERT INTO rarity_types (
            rarity_name,
            rarity_code
        ) VALUES (
            %(rarity_name)s,
            %(rarity_code)s
        )
        ON DUPLICATE KEY UPDATE
            rarity_name = VALUES(rarity_name),
            rarity_code = VALUES(rarity_code)
    """


def card_images_sql():
    return """
        INSERT INTO card_images (
            image_id,
            card_id,
            image_url,
            image_url_small,
            image_url_cropped
        ) VALUES (
            %(image_id)s,
            %(card_id)s,
            %(image_url)s,
            %(image_url_small)s,
            %(image_url_cropped)s
        )
        ON DUPLICATE KEY UPDATE
            card_id = VALUES(card_id),
            image_url = VALUES(image_url),
            image_url_small = VALUES(image_url_small),
            image_url_cropped = VALUES(image_url_cropped)
    """


def card_price_history_sql():
    return """
        INSERT INTO card_price_history (
            card_id,
            marketplace_id,
            currency_code,
            snapshot_at,
            price,
            price_origin,
            exchange_rate
        ) VALUES (
            %(card_id)s,
            %(marketplace_id)s,
            %(currency_code)s,
            %(snapshot_at)s,
            %(price)s,
            %(price_origin)s,
            %(exchange_rate)s
        )
        ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            price_origin = VALUES(price_origin),
            exchange_rate = VALUES(exchange_rate)
    """


# Compatibilidad de imports durante la transicion de consumidores Python.
card_sets_sql = card_printings_sql
rarities_sql = rarity_types_sql


def card_banlist_sql():
    return """
        INSERT INTO card_banlist (
            card_id,
            ban_tcg,
            ban_ocg,
            ban_goat
        ) VALUES (
            %(card_id)s,
            %(ban_tcg)s,
            %(ban_ocg)s,
            %(ban_goat)s
        )
        ON DUPLICATE KEY UPDATE
            ban_tcg = VALUES(ban_tcg),
            ban_ocg = VALUES(ban_ocg),
            ban_goat = VALUES(ban_goat)
    """


def card_typelines_sql():
    return """
        INSERT INTO card_typelines (
            card_id,
            typeline,
            position
        ) VALUES (
            %(card_id)s,
            %(typeline)s,
            %(position)s
        )
    """


def card_linkmarkers_sql():
    return """
        INSERT INTO card_linkmarkers (
            card_id,
            linkmarker,
            position
        ) VALUES (
            %(card_id)s,
            %(linkmarker)s,
            %(position)s
        )
    """
