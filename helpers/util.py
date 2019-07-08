# helper functions


def format_show_info(show):
    empty_placeholder = "—"
    star_emoji = "★"
    empty_star_emoji = "☆"

    text = "_{name} ({start} - {end})_\
            \nRating: {rating}\
            \nGenres: _{genres}_\
            \nRuntime: _{runtime}_\
            \nStatus: _{status}_"

    name = getattr(show, "name", None)
    start = getattr(show, "premiered", None)
    end = getattr(getattr(show, "previous_episode", None), "airdate", None)
    rating = getattr(show, "rating", {}).get("average")
    genres = getattr(show, "genres", None)
    runtime = getattr(show, "runtime", None)
    status = getattr(show, "status", None)

    # some of these could've been done with the getattr call
    # but None is an acceptable return value for gettattr

    name = name if name else empty_placeholder
    start = start[:4] if start else ""
    genres = ", ".join(genres) if genres else empty_placeholder
    runtime = str(runtime) + " minutes" if runtime else empty_placeholder
    status = status if status else empty_placeholder

    # only show end if show has ended
    if status == "Ended":
        end = end[:4]
    else:
        end = ""

    # star rating out of five
    if rating:
        r = int(rating)//2
        rating = star_emoji * r + empty_star_emoji * (5-r)
    else:
        rating = empty_placeholder

    formatted_text = text.format(
            name=name,
            start=start,
            end=end,
            rating=rating,
            genres=genres,
            runtime=runtime,
            status=status
            )

    return formatted_text
