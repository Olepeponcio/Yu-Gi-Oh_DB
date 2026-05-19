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
        card_ids = [card["id"] for card in tables["cards"]]

        affected = {
            "cards": load_cards(cursor, tables["cards"]),
            "deleted_child_rows": delete_replaceable_child_rows(cursor, card_ids),
            "card_sets": insert_many(cursor, card_sets_sql(), tables["card_sets"]),
            "card_images": load_card_images(cursor, tables["card_images"]),
            "card_prices": load_card_prices(cursor, tables["card_prices"]),
            "card_banlist": load_card_banlist(cursor, tables["card_banlist"]),
            "card_typelines": insert_many(cursor, card_typelines_sql(), tables["card_typelines"]),
            "card_linkmarkers": insert_many(cursor, card_linkmarkers_sql(), tables["card_linkmarkers"]),
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
        "card_sets",
        "card_images",
        "card_prices",
        "card_banlist",
        "card_typelines",
        "card_linkmarkers",
    )

    for table in tables:
        for ids in chunked(card_ids):
            placeholders = ", ".join(["%s"] * len(ids))
            cursor.execute(f"DELETE FROM {table} WHERE card_id IN ({placeholders})", ids)
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


def load_card_images(cursor, card_images):
    return insert_many(cursor, card_images_sql(), card_images)


def load_card_prices(cursor, card_prices):
    return insert_many(cursor, card_prices_sql(), card_prices)


def load_card_banlist(cursor, card_banlist):
    return insert_many(cursor, card_banlist_sql(), card_banlist)


def cards_sql():
    return """
        INSERT INTO cards (
            id,
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
            %(id)s,
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


def card_sets_sql():
    return """
        INSERT INTO card_sets (
            card_id,
            set_name,
            set_code,
            set_rarity,
            set_rarity_code,
            set_price
        ) VALUES (
            %(card_id)s,
            %(set_name)s,
            %(set_code)s,
            %(set_rarity)s,
            %(set_rarity_code)s,
            %(set_price)s
        )
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


def card_prices_sql():
    return """
        INSERT INTO card_prices (
            card_id,
            cardmarket_price,
            tcgplayer_price,
            ebay_price,
            amazon_price,
            coolstuffinc_price
        ) VALUES (
            %(card_id)s,
            %(cardmarket_price)s,
            %(tcgplayer_price)s,
            %(ebay_price)s,
            %(amazon_price)s,
            %(coolstuffinc_price)s
        )
        ON DUPLICATE KEY UPDATE
            cardmarket_price = VALUES(cardmarket_price),
            tcgplayer_price = VALUES(tcgplayer_price),
            ebay_price = VALUES(ebay_price),
            amazon_price = VALUES(amazon_price),
            coolstuffinc_price = VALUES(coolstuffinc_price)
    """


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
